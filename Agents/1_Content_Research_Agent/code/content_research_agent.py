"""
Content Research Agent - Fetches Google Trends data for given topics and saves the results to files.
This script uses pytrends to fetch Google Trends data asynchronously,
validates it, and saves it as JSON files.
"""

import asyncio
import json
import logging
from typing import List, Dict, Any

import jsonschema
from jsonschema import validate
from pytrends.request import TrendReq
from requests.exceptions import RequestException


class GoogleTrendsFetcher:
    """
    A class to fetch Google Trends data for specific topics and save the results as JSON files.
    """

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
        """
        Initializes the GoogleTrendsFetcher with a pytrends instance and logging configuration.
        """
        self.pytrends = TrendReq(hl='en-US', tz=360)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def sanitize_filename(topic: str) -> str:
        """
        Sanitizes a topic name to create a valid filename.

        Args:
            topic (str): The topic name to sanitize.

        Returns:
            str: A sanitized filename-safe string.
        """
        return ''.join(c for c in topic if c.isalnum() or c in (' ', '_')).replace(' ', '_')

    async def fetch_data(self, topic: str) -> Dict[str, Any]:
        """
        Fetches interest-over-time data for a topic from Google Trends with retry logic.

        Args:
            topic (str): The topic to fetch data for.

        Returns:
            Dict[str, Any]: The fetched data as a dictionary, or an empty dict if fetching fails.
        """
        self.pytrends.build_payload([topic], cat=0, timeframe='now 1-d', geo='IN', gprop='')
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
            except RequestException as e:
                logging.error(
                    'Request failed: %s. Attempt %d of %d.',
                    str(e),
                    attempt + 1,
                    retries
                )
                await asyncio.sleep(2 ** attempt)
            except jsonschema.ValidationError as e:
                logging.error('Data validation failed: %s', str(e))
                return {}
        logging.error('Failed to retrieve data for topic %s after %d attempts.', topic, retries)
        return {}

    def save_to_file(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Saves the fetched data to a JSON file with a sanitized filename.

        Args:
            topic (str): The topic name used to generate the filename.
            data (Dict[str, Any]): The data to save.
        """
        sanitized_topic = self.sanitize_filename(topic)
        file_name = f'{sanitized_topic}_trends.json'
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info('Data saved successfully to %s', file_name)
        except OSError as e:
            logging.error('Failed to save data to %s: %s', file_name, str(e))

    async def fetch_and_save(self, topic_name: str) -> None:
        """
        Fetches Google Trends data for a topic and saves it to a file asynchronously.

        Args:
            topic_name (str): The topic to fetch and save data for.
        """
        data = await self.fetch_data(topic_name)
        if data:
            self.save_to_file(topic_name, data)


async def main(topic_list: List[str]) -> None:
    """
    Main function to fetch data for multiple topics concurrently.

    Args:
        topic_list (List[str]): List of topics to fetch data for.
    """
    fetcher = GoogleTrendsFetcher()
    tasks = [fetcher.fetch_and_save(topic_name) for topic_name in topic_list]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    topics = ['Python Programming', 'Machine Learning', 'Artificial Intelligence']
    asyncio.run(main(topics))
