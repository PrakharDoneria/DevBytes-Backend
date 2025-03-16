import requests
import feedparser
from datetime import datetime, timezone, timedelta

def is_recent(published_date):
    """Check if the article was published within the last 2 days (UTC)."""
    if not published_date:
        return False

    try:
        article_date = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %z")  
    except ValueError:
        return False

    today_utc = datetime.now(timezone.utc).date()
    two_days_ago = today_utc - timedelta(days=2)

    return two_days_ago <= article_date.date() <= today_utc

def fetch_hacker_news():
    """Fetch recent tech news from Hacker News."""
    url = "http://hn.algolia.com/api/v1/search_by_date?query=technology&tags=story"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    articles = response.json().get("hits", [])
    return [
        {"title": article["title"], "content": article.get("story_text") or article["url"], "published_at": article["created_at"]}
        for article in articles if "created_at" in article and is_recent(article["created_at"])
    ]

def fetch_rss_news(source_name, rss_url):
    """Fetch recent tech news from an RSS feed."""
    feed = feedparser.parse(rss_url)
    return [
        {"title": entry.title, "content": entry.summary, "published_at": entry.published}
        for entry in feed.entries if "published" in entry and is_recent(entry.published)
    ]

def fetch_all_tech_news():
    """Aggregate recent news from multiple sources."""
    sources = {
        "TechCrunch": "https://techcrunch.com/feed/",
        "Reddit Technology": "https://www.reddit.com/r/technology/.rss",
        "The Verge": "https://www.theverge.com/rss/index.xml",
        "Wired": "https://www.wired.com/feed/rss",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "Mashable Tech": "https://mashable.com/feeds/rss/tech",
        "MIT Technology Review": "https://www.technologyreview.com/feed/",
        "BBC Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "Google News Tech": "https://news.google.com/rss/search?q=technology"
    }

    all_news = fetch_hacker_news()  # Start with Hacker News
    for source, url in sources.items():
        all_news.extend(fetch_rss_news(source, url))  # Add RSS sources

    return all_news  # Return only recent news
