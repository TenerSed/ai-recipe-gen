import praw
import requests
import os

# --- Step 1: Setup PRAW (Reddit API) ---
# Create an app at https://www.reddit.com/prefs/apps to get these values
reddit = praw.Reddit(
    client_id="mgBRZUB4Ia9nObsT5vxRxw",
    client_secret="VliiPzBy2xZvwwOQHvmn87Tbo5T8lQ",
    user_agent="fridge_scraper"
)

# --- Step 2: Target subreddit ---
subreddit = reddit.subreddit("FridgeDetective")

# --- Step 3: Create folder for images ---
save_path = r"C:\Users\siddheshwin006\ml_training\ai-recipe-gen\data\FridgeScraper"  # or your preferred path
os.makedirs(save_path, exist_ok=True)



# --- Step 4: Scrape posts ---
count = 0
for submission in subreddit.hot(limit=5000):  # you can change hot/top/new and the limit
    url = submission.url
    if url.endswith((".jpg", ".jpeg", ".png")):
        try:
            response = requests.get(url, stream=True)
            filename = os.path.join(save_path, f"fridge_{count}.jpg")
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Saved {filename}")
            count += 1
        except Exception as e:
            print(f"Failed to download {url}: {e}")

print(f"Downloaded {count} images!")
