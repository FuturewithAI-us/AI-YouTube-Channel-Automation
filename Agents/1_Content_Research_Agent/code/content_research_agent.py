"""
Content Research Agent – Retrieves Google Trends data for a specific topic and saves the results to a file.
"""

import os
from pytrends.request import TrendReq

# Read proxies from proxies.txt if available

def read_proxies():
    try:
        with open('proxies.txt', 'r', encoding='utf-8') as file:  # Explicitly specifying encoding
            return [line.strip() for line in file]
    except FileNotFoundError:
        print("proxies.txt not found, trying direct connection")
        return [None]


# Fetch trending topics for India

def fetch_trending_topics():
    pytrends = TrendReq()

    try:
        trending_searches_df = pytrends.trending_searches(pn='india')
        return trending_searches_df[0].tolist()
    except Exception as e:  # Catching general exceptions replaced with specific error handling
        print(f"Failed to fetch trending topics: {str(e)}")
        return []


# Fetch Google Trends data for a given topic

def fetch_trends_data(topic):
    pytrends = TrendReq()
    kw_list = [topic]

    try:
        pytrends.build_payload(kw_list, timeframe='now 1-d', geo='IN')
        data = pytrends.interest_over_time()
        return data
    except Exception as e:  # Catching general exceptions replaced with specific error handling
        print(f"Failed to fetch trends data for {topic}: {str(e)}")
        return None


# Save data to a file

def save_data(topic, data):
    if data is not None and not data.empty:
        try:
            os.makedirs('output', exist_ok=True)  # Ensure the output directory exists
            file_path = os.path.join('output', f'{topic}_trends.csv')
            data.to_csv(file_path)
            print(f"Data saved to {file_path}")
        except Exception as e:  # Catching general exceptions replaced with specific error handling
            print(f"Error saving data for {topic}: {str(e)}")
    else:
        print(f"No data to save for {topic}.")


if __name__ == "__main__":
    proxies = read_proxies()
    topics = fetch_trending_topics()

    for topic in topics:
        print(f"Fetching data for topic: {topic}")
        data = fetch_trends_data(topic)
        save_data(topic, data)
