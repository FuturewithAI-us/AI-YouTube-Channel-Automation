import os
import time
import logging
import json
from pytrends.request import TrendReq
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from requests.exceptions import RequestException
import jsonschema
from jsonschema import validate
import asyncio
from aiohttp import ClientSession


class GoogleTrendsFetcher:
    """
    GoogleTrendsFetcher - Retrieves Google Trends data for a specific topic and saves the results to a file.
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

    def __init__(self, proxies: Optional[List[str]] = None):
        load_dotenv()
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.proxies = proxies
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    async def fetch_data(self, topic: str) -> Dict[str, Any]:
        """
        Fetches interest over time data for a given topic.
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
                else:
                    logging.warning('No data retrieved for the topic: %s', topic)
                    return {}
            except RequestException as e:
                logging.error('Request failed: %s. Attempt %d of %d.', str(e), attempt + 1, retries)
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except jsonschema.ValidationError as e:
                logging.error('Data validation failed: %s', str(e))
                return {}

        logging.error('Failed to retrieve data after %d attempts.', retries)
        return {}

    def save_to_file(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Saves the fetched data to a file.
        """
        file_name = f'{topic}_trends.json'
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info('Data saved successfully to %s', file_name)
        except Exception as e:
            logging.error('Failed to save data: %s', str(e))

    async def fetch_and_save(self, topic: str) -> None:
        """
        Fetches and saves Google Trends data for a given topic asynchronously.
        """
        data = await self.fetch_data(topic)
        if data:
            self.save_to_file(topic, data)


async def main(topics: List[str]) -> None:
    fetcher = GoogleTrendsFetcher()
    tasks = [fetcher.fetch_and_save(topic) for topic in topics]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    topics = ['Python Programming', 'Machine Learning', 'Artificial Intelligence']
    asyncio.run(main(topics))
