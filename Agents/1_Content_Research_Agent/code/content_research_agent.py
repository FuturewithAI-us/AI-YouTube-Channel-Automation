from pytrends.request import TrendReq
import time

# Read proxies
try:
    with open('proxies.txt', 'r') as file:
        proxies = [line.strip() for line in file]
except FileNotFoundError:
    print("proxies.txt not found, trying direct connection")
    proxies = [None]

# Fetch trending topics for India
for proxy in proxies:
    try:
        pytrends = TrendReq(hl='en-IN', tz=330, timeout=(15,30), proxies=[proxy] if proxy else None, retries=3, backoff_factor=0.5)
        topics = pytrends.trending_searches(pn='india')
        topic = topics[0][0]
        print(f"Found trending topic: {topic}")
        break
    except Exception as e:
        print(f"Proxy {proxy if proxy else 'Direct'} failed: {e}")
        time.sleep(2)
else:
    topic = "Understanding Artificial Intelligence in India"
    print("All attempts failed, using default topic:", topic)

# Save topic
with open('trending_topics.txt', 'w') as file:
    file.write(topic)
