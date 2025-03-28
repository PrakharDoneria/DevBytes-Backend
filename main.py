from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from summarise.summariser import summarise
from news_fetcher.fetch_news import fetch_all_tech_news
import uvicorn
import os

app = FastAPI()

# Add CORSMiddleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; you can specify a list of domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/summarise-tech-news/")
async def summarise_tech_news(page: int = Query(1, ge=1), page_size: int = Query(10, le=50)):
    """
    Fetch paginated recent tech news (up to 2 days old) and summarize it.

    Query Parameters:
    - page (int): The page number (default = 1)
    - page_size (int): Number of articles per page (default = 10, max = 50)

    Returns:
    - JSON with summarized news and pagination info.
    """
    news_articles = fetch_all_tech_news()
    total_articles = len(news_articles)

    if total_articles == 0:
        return {"message": "No recent tech news available. Check back later!"}

    # Sort by most recent date
    news_articles = sorted(news_articles, key=lambda x: x["published_at"], reverse=True)

    # Paginate
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_news = news_articles[start_idx:end_idx]

    if not paginated_news:
        raise HTTPException(status_code=404, detail="No more news available")

    # Summarize the paginated news
    summarized_news = [
        {"title": article["title"], "summary": summarise(article["content"])}
        for article in paginated_news
    ]

    return {
        "page": page,
        "page_size": page_size,
        "total_articles": total_articles,
        "total_pages": (total_articles // page_size) + (1 if total_articles % page_size != 0 else 0),
        "summarized_news": summarized_news
    }

@app.get("/")
async def root():
    return {"message": "Tech News Summarizer API is running!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
