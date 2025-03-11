"""Module to fetch Google Trends data asynchronously for multiple topics
and save results to JSON files with validation and error handling."""

import json
import logging
from typing import Dict, Any

from pytrends.request import TrendReq
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()]
)

class ContentResearchAgent:
    """Fetches Google Trends data for topics and saves results as JSON files."""

    def __init__(self):
        """Initializes the TrendReq client."""
        self.pytrends = TrendReq(hl="en-US", tz=360)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def fetch_trends(self, search_topic: str) -> Dict[str, Any]:
        """Fetches interest-over-time data with retry logic.

        Args:
            search_topic (str): The topic to fetch data for.

        Returns:
            Dict[str, Any]: The fetched data as a dictionary.

        Raises:
            RequestException: If the API request fails after retries.
        """
        try:
            self.pytrends.build_payload(
                [search_topic], cat=0, timeframe="now 1-d", geo="IN", gprop=""
            )
            data = self.pytrends.interest_over_time()
            if not data.empty:
                return data.reset_index().to_dict(orient="records")
            logging.warning("No data retrieved for topic: %s", search_topic)
            return {}
        except RequestException as request_error:
            logging.error("Request failed: %s", str(request_error))
            raise
        except KeyError as key_error:
            logging.error("Data format error: %s", str(key_error))
            return {}

    def save_to_file(self, file_topic: str, data: Dict[str, Any]) -> None:
        """Saves data to a JSON file.

        Args:
            file_topic (str): The topic name used to generate the filename.
            data (Dict[str, Any]): The data to save.

        Raises:
            OSError: If the file cannot be saved.
        """
        file_name = f"{file_topic}_research.json"
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump({"topic": file_topic, "trends": data}, file, ensure_ascii=False, indent=4)
            logging.info("Data saved successfully to %s", file_name)
        except OSError as file_error:
            logging.error("Failed to save data to %s: %s", file_name, str(file_error))
            raise

# Example usage
if __name__ == "__main__":
    agent = ContentResearchAgent()
    TOPIC = "Artificial Intelligence"
    try:
        trends = agent.fetch_trends(TOPIC)
        if trends:
            agent.save_to_file(TOPIC, trends)
    except (RequestException, OSError) as specific_error:
        logging.error("Critical error: %s", str(specific_error))
