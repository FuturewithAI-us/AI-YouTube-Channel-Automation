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
    format="%(asctime)s - %(levelname)s - %(message)s"
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
    def fetch_trends(self, topic: str) -> Dict[str, Any]:
        """Fetches interest-over-time data with retry logic.

        Args:
            topic (str): The topic to fetch data for.

        Returns:
            Dict[str, Any]: The fetched data as a dictionary.

        Raises:
            RequestException: If the API request fails after retries.
        """
        try:
            self.pytrends.build_payload([topic], cat=0, timeframe="now 1-d", geo="IN", gprop="")
            data = self.pytrends.interest_over_time()
            if not data.empty:
                return data.reset_index().to_dict(orient="records")
            logging.warning("No data retrieved for topic: %s", topic)
            return {}
        except RequestException as error:
            logging.error("Request failed: %s", str(error))
            raise

    def save_to_file(self, topic: str, data: Dict[str, Any]) -> None:
        """Saves data to a JSON file.

        Args:
            topic (str): The topic name used to generate the filename.
            data (Dict[str, Any]): The data to save.

        Raises:
            OSError: If the file cannot be saved.
        """
        file_name = f"{topic}_research.json"
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump({"topic": topic, "trends": data}, file, ensure_ascii=False, indent=4)
            logging.info("Data saved successfully to %s", file_name)
        except OSError as error:
            logging.error("Failed to save data to %s: %s", file_name, str(error))
            raise


# Example usage
if __name__ == "__main__":
    agent = ContentResearchAgent()
    topic = "Artificial Intelligence"
    try:
        trends = agent.fetch_trends(topic)
        if trends:
            agent.save_to_file(topic, trends)
    except Exception as error:
        logging.error("An error occurred: %s", str(error))
