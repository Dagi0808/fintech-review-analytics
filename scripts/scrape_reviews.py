from google_play_scraper import reviews, Sort
import pandas as pd
import time

# -----------------------------
# CONFIG
# -----------------------------
APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "DASHEN": "com.dashen.dashensuperapp"
}

TARGET_REVIEWS = 500  # buffer above 400 requirement


# -----------------------------
# SCRAPER FUNCTION
# -----------------------------
def scrape_app(app_name, app_id):
    print(f"\n🔄 Scraping {app_name} ...")

    all_reviews = []
    continuation_token = None

    while len(all_reviews) < TARGET_REVIEWS:
        result, continuation_token = reviews(
            app_id,
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=200,
            continuation_token=continuation_token
        )

        for r in result:
            all_reviews.append({
                "review": r.get("content"),
                "rating": r.get("score"),
                "date": r.get("at").date(),
                "bank": app_name,
                "source": "Google Play"
            })

        print(f"Collected {len(all_reviews)} reviews so far for {app_name}")

        if not continuation_token:
            break

        time.sleep(1)  # avoid rate limit

    return all_reviews


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():
    dataset = []

    for app_name, app_id in APPS.items():
        data = scrape_app(app_name, app_id)
        dataset.extend(data)

    df = pd.DataFrame(dataset)

    # Save RAW data
    df.to_csv("data/raw/reviews_raw.csv", index=False)

    print("\n✅ Scraping completed!")
    print(f"Total reviews collected: {len(df)}")


if __name__ == "__main__":
    main()