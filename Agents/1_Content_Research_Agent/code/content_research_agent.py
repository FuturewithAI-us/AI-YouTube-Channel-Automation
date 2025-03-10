"""
Content Research Agent – Retrieves Google Trends data for a specific topic and saves the results to a file.
"""

import time  # Standard library import should be placed first
from pytrends.request import TrendReq  # Third-party library import


def fetch_trending_topics(topic):
    """
    Fetch trending topics for India from Google Trends for a specified topic.

    Args:
        topic (str): The search topic to retrieve trending data for.

    Returns:
        dict: A dictionary containing the trending data.
    """
    pytrends = TrendReq(hl='en-US', tz=330)

    try:
        with open('proxies.txt', 'r', encoding='utf-8') as file:  # Specify encoding
            proxies = [line.strip() for line in file]
    except FileNotFoundError:
        print("proxies.txt not found, trying direct connection")
        proxies = [None]

    for proxy in proxies:
        if proxy:
            pytrends.PROXIES = {'http': proxy, 'https': proxy}

        try:
            pytrends.build_payload([topic], cat=0, timeframe='now 1-d', geo='IN', gprop='')
            trends_data = pytrends.interest_over_time().to_dict()

            if trends_data:
                return trends_data

        except Exception as e:  # Broad exception caught, but necessary to handle proxy issues
            print(f"Error with proxy {proxy}: {e}")

    print("No trending data found or unable to connect.")
    return {}


def save_trending_data(topic, data):
    """
    Save the trending data to a text file.

    Args:
        topic (str): The search topic.
        data (dict): The trending data to save.
    """
    filename = f'{topic}_trending_data.txt'

    try:
        with open(filename, 'w', encoding='utf-8') as file:  # Specify encoding
            for date, trend_value in data.items():
                file.write(f'{date}: {trend_value}\n')
        print(f"Trending data for '{topic}' saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")


def main():
    """
    Main function to prompt user for a topic and save trending data.
    """
    topic = input("Enter the topic you want to fetch trending data for: ")
    trends_data = fetch_trending_topics(topic)

    if trends_data:
        save_trending_data(topic, trends_data)
    else:
        print("No data to save.")


if __name__ == "__main__":
    main()
