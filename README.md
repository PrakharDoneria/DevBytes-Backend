# Tech News Summarizer API

## **Sample Usage**

### **Fetch Summarized Tech News**
**Endpoint:**
```http
GET /summarise-tech-news/?page=1&page_size=10
```

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/summarise-tech-news/?page=1&page_size=10" -H "Accept: application/json"
```

---

## **Sample Response**
### **1️⃣ Successful Response (Paginated Tech News Summaries)**
```json
{
  "page": 1,
  "page_size": 10,
  "total_articles": 50,
  "total_pages": 5,
  "summarized_news": [
    {
      "title": "Wired - AI Evolution",
      "summary": "A new AI algorithm improves neural network efficiency by 300%."
    },
    {
      "title": "BBC Tech - Quantum Computing",
      "summary": "Google announces a new quantum processor that can handle complex calculations faster."
    }
  ]
}
```

### **2️⃣ No News Available**
```json
{
  "message": "No recent tech news available. Check back later!"
}
```

### **3️⃣ Requesting a Page with No More News**
```json
{
  "detail": "No more news available"
}
```