import praw
import requests
import os
import time

# --- Step 1: Setup PRAW ---
reddit = praw.Reddit(
    client_id="mgBRZUB4Ia9nObsT5vxRxw",
    client_secret="VliiPzBy2xZvwwOQHvmn87Tbo5T8lQ",
    user_agent="fridge_scraper"
)

# --- Step 2: Target subreddit & save path ---
subreddit = reddit.subreddit("FridgeDetective")
save_path = r"C:\Users\siddheshwin006\ml_training\ai-recipe-gen\data\FridgeScraper2.0"
os.makedirs(save_path, exist_ok=True)

count = 0
scrape_count = 0
posts_to_scrape = 5000  # total posts you want
batch_size = 100        # posts per request
after = None

while scrape_count < posts_to_scrape:
    # Fetch a batch of submissions
    submissions = list(subreddit.new(limit=batch_size) if not after else subreddit.new(limit=batch_size, params={'after': after}))

    if not submissions:
        break  # no more posts

    for submission in submissions:
        try:
            # Direct image
            if submission.url.endswith((".jpg", ".jpeg", ".png")):
                response = requests.get(submission.url, stream=True)
                filename = os.path.join(save_path, f"fridge_{count}.jpg")
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Saved {filename} from post {scrape_count}")
                count += 1

            # Reddit gallery
            elif submission.is_gallery:
                for item in submission.media_metadata.values():
                    img_url = item["s"]["u"].split("?")[0].replace("preview", "i")
                    response = requests.get(img_url, stream=True)
                    filename = os.path.join(save_path, f"fridge_{count}.jpg")
                    with open(filename, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print(f"Saved {filename} from post {scrape_count}")
                    count += 1

            time.sleep(0.1)  # avoid rate limits
        except Exception as e:
            print(f"Failed for {submission.id}: {e}")
        scrape_count += 1

    # Update 'after' to last submission id
    after = submissions[-1].id

print(f"Downloaded {count} images!")
