"""
Content Research Agent - Retrieves Google Trends data for a specific topic and saves the results to a file.
"""

import time  # Standard library import should be placed first
from pytrends.request import TrendReq  # Third-party library import

TOPIC = "Your Topic Here"  # Example of an appropriately named constant


def fetch_trends_data(topic):
    """
    Fetches Google Trends data for a given topic.
    
    Args:
        topic (str): The topic to search trends for.

    Returns:
        dict: The retrieved trends data.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [topic]
        pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d', geo='', gprop='')

        data = pytrends.interest_over_time()
        return data

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None


def save_trends_data(data, filename):
    """
    Saves the trends data to a file.

    Args:
        data (dict): The data to be saved.
        filename (str): The name of the file to save the data to.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:  # Specify encoding
            file.write(data.to_csv())
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


if __name__ == "__main__":
    trends_data = fetch_trends_data(TOPIC)
    if trends_data is not None:
        save_trends_data(trends_data, "trends_data.csv")
    else:
        print("Failed to retrieve trends data.")

