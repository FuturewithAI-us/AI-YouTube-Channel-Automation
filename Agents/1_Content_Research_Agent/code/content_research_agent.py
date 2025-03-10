"""Module to fetch Google Trends data asynchronously for multiple topics
and save results to JSON files with validation and error handling."""


import asyncio
import json
import logging
from typing import List, Dict, Any

import jsonschema
from jsonschema import validate
from pytrends.request import TrendReq
from requests.exceptions import RequestException


class GoogleTrendsFetcher:
    """Fetches Google Trends data for topics and saves results as JSON files."""

    SCHEMA = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "date": {"type": "string"},
                "value": {"type": "integer"}
            },
            "required": ["date", "value"]
        }
    }

    def __init__(self):
        """Initializes the fetcher with TrendReq client and logging config."""
        self.pytrends = TrendReq(hl='en-US', tz=360)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def sanitize_filename(topic: str) -> str:
        """Sanitizes topic name to create valid filename."""
        return ''.join(c for c in topic if c.isalnum() or c in (' ', '_')
                      ).replace(' ', '_')

    async def fetch_data(self, topic: str) -> Dict[str, Any]:
        """Fetches interest-over-time data with retry logic and validation."""
        self.pytrends.build_payload(
            [topic], cat=0, timeframe='now 1-d', geo='IN', gprop=''
        )
        retries = 3
        for attempt in range(retries):
            try:
                data = self.pytrends.interest_over_time()
                if not data.empty:
                    data_dict = data.reset_index().to_dict(orient='records')
                    validate(instance=data_dict, schema=self.SCHEMA)
                    return data_dict
                logging.warning('No data retrieved for topic: %s', topic)
                return {}
            except RequestException as error:
            logging.error(
            'Request failed: %s. Attempt %d of %d.',
        str(error),
        attempt + 1,
        retries
        )
                await asyncio.sleep(2 ** attempt)
           except jsonschema.ValidationError as validation_error:
    logging.error('Data validation failed: %s', str(validation_error))
                return {}
        logging.error(
            'Failed to retrieve data for topic %s after %d attempts.',
            topic,
            retries
        )
        return {}

    def save_to_file(self, topic: str, data: Dict[str, Any]) -> None:
        """Saves data to JSON file with sanitized filename."""
        sanitized_topic = self.sanitize_filename(topic)
        file_name = f'{sanitized_topic}_trends.json'
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info('Data saved successfully to %s', file_name)
        except OSError as file_error:
    logging.error('Failed to save data to %s: %s', file_name, str(file_error))

    async def fetch_and_save(self, topic_name: str) -> None:
        """Orchestrates data fetching and saving process for a topic."""
        data = await self.fetch_data(topic_name)
        if data:
            self.save_to_file(topic_name, data)


async def main(topic_list: List[str]) -> None:
    """Main function to process multiple topics concurrently."""
    fetcher = GoogleTrendsFetcher()
    tasks = [
        fetcher.fetch_and_save(topic_name)
        for topic_name in topic_list
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    topics = [
        'Python Programming',
        'Machine Learning',
        'Artificial Intelligence'
    ]
    asyncio.run(main(topics))
