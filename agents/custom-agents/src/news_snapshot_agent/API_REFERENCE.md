# News Snapshot Agent API Reference

## Overview

The News Snapshot Agent provides comprehensive news information from Google News RSS feeds with advanced filtering and analysis capabilities. It supports location-based news retrieval, date filtering, keyword search, and trending topic extraction.

## Core Features

- **Location-based News**: Get news for any city, state, or country
- **Date Filtering**: Filter news by date ranges using multiple formats
- **Keyword Search**: Search for specific topics within location-based news
- **Weather News**: Fetch weather-related news with categorization
- **Trending Topics**: Extract and analyze trending topics from news articles
- **News Snapshots**: Generate comprehensive summaries with metadata
- **Real-time Data**: Fetch fresh news from Google News RSS feeds

## Tools Reference

### 1. get_news_for_location

Retrieves news articles for a specific location from Google News RSS feed.

**Parameters:**
- `location` (str): The location to search for (city, state, country, etc.)
- `max_results` (int, optional): Maximum number of articles to return (default: 20)

**Returns:**
```json
{
  "status": "success",
  "location": "New York",
  "articles_count": 15,
  "articles": [
    {
      "title": "Article Title",
      "link": "https://example.com/article",
      "description": "Article description",
      "published_date": "2024-01-01T10:00:00Z",
      "source": "News Source",
      "raw_pub_date": "Mon, 01 Jan 2024 10:00:00 GMT"
    }
  ],
  "feed_info": {
    "title": "Google News",
    "description": "News feed description",
    "language": "en-US",
    "last_build_date": "Mon, 01 Jan 2024 10:00:00 GMT"
  },
  "timestamp": "2024-01-01T10:00:00Z",
  "source": "google-news-rss",
  "url": "https://news.google.com/rss/search?q=New%20York&hl=en-US&gl=US&ceid=US:en"
}
```

### 2. get_news_with_date_filter

Retrieves news articles with date range filtering.

**Parameters:**
- `location` (str): The location to search for
- `start_date` (str, optional): Start date in various formats
- `end_date` (str, optional): End date in various formats
- `max_results` (int, optional): Maximum number of articles to return (default: 20)

**Supported Date Formats:**
- ISO format: `"2024-01-01"` or `"2024-01-01T10:00:00Z"`
- Relative format: `"7d"` (7 days ago), `"24h"` (24 hours ago), `"1w"` (1 week ago), `"1m"` (1 month ago), `"1y"` (1 year ago)
- Keywords: `"now"` (current time)

**Returns:**
```json
{
  "status": "success",
  "location": "San Francisco",
  "date_filter": {
    "start_date": "7d",
    "end_date": "now",
    "start_datetime": "2023-12-25T10:00:00Z",
    "end_datetime": "2024-01-01T10:00:00Z"
  },
  "articles_count": 12,
  "total_articles_found": 20,
  "articles": [...],
  "feed_info": {...},
  "timestamp": "2024-01-01T10:00:00Z",
  "source": "google-news-rss-filtered"
}
```

### 3. get_news_snapshot

Generates a comprehensive news snapshot with summary and analysis.

**Parameters:**
- `location` (str): The location to search for
- `days_back` (int, optional): Number of days to look back (default: 7)
- `max_results` (int, optional): Maximum number of articles to return (default: 15)
- `include_summary` (bool, optional): Whether to include summary (default: True)

**Returns:**
```json
{
  "status": "success",
  "location": "Austin",
  "snapshot_info": {
    "period_days": 7,
    "start_date": "2023-12-25T10:00:00Z",
    "end_date": "2024-01-01T10:00:00Z",
    "articles_count": 15,
    "summary_included": true
  },
  "articles": [...],
  "summary": {
    "location": "Austin",
    "total_articles": 15,
    "top_stories": [
      {
        "title": "Top Story Title",
        "source": "News Source",
        "published_date": "2024-01-01T10:00:00Z"
      }
    ],
    "top_sources": [
      ["News Source 1", 5],
      ["News Source 2", 3]
    ],
    "trending_topics": [
      {"topic": "technology", "count": 8},
      {"topic": "business", "count": 5}
    ],
    "summary_text": "Found 15 news articles for Austin. Top sources include News Source 1, News Source 2."
  },
  "feed_info": {...},
  "timestamp": "2024-01-01T10:00:00Z",
  "source": "google-news-rss-snapshot"
}
```

### 4. search_news_by_keywords

Searches for news articles containing specific keywords within a location.

**Parameters:**
- `location` (str): The location to search for
- `keywords` (List[str]): List of keywords to search for
- `max_results` (int, optional): Maximum number of articles to return (default: 15)

**Returns:**
```json
{
  "status": "success",
  "location": "Chicago",
  "keywords": ["technology", "business"],
  "articles_count": 8,
  "total_articles_searched": 20,
  "articles": [...],
  "feed_info": {...},
  "timestamp": "2024-01-01T10:00:00Z",
  "source": "google-news-rss-keyword-search"
}
```

### 5. get_trending_topics

Extracts trending topics from news articles for a location.

**Parameters:**
- `location` (str): The location to analyze
- `max_results` (int, optional): Maximum number of trending topics to return (default: 10)

**Returns:**
```json
{
  "status": "success",
  "location": "Miami",
  "trending_topics": [
    {
      "topic": "economy",
      "frequency": 15,
      "percentage": 30.0
    },
    {
      "topic": "sports",
      "frequency": 8,
      "percentage": 16.0
    }
  ],
  "total_articles_analyzed": 50,
  "timestamp": "2024-01-01T10:00:00Z",
  "source": "google-news-rss-trending"
}
```

## Usage Examples

### Basic News Retrieval
```python
# Get latest news for New York
result = await get_news_for_location("New York", max_results=10)
```

### Date Filtered News
```python
# Get news from last 7 days
result = await get_news_with_date_filter(
    "San Francisco", 
    start_date="7d", 
    end_date="now"
)

# Get news from specific date range
result = await get_news_with_date_filter(
    "Austin", 
    start_date="2024-01-01", 
    end_date="2024-01-07"
)
```

### News Snapshot
```python
# Get comprehensive snapshot for last 3 days
result = await get_news_snapshot(
    "Chicago", 
    days_back=3, 
    include_summary=True
)
```

### Keyword Search
```python
# Search for technology news
result = await search_news_by_keywords(
    "Seattle", 
    keywords=["technology", "startup", "innovation"]
)
```

### Trending Topics
```python
# Get trending topics
result = await get_trending_topics("Boston", max_results=10)
```

## Error Handling

All functions return consistent error responses:

```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": "2024-01-01T10:00:00Z",
  "error_type": "error_category"
}
```

**Common Error Types:**
- `network_error`: Network connectivity issues
- `http_error`: HTTP status code errors
- `parsing_error`: XML/RSS parsing issues
- `date_filter_error`: Date format parsing errors
- `unknown_error`: Unexpected errors

## Rate Limiting and Best Practices

- **Respectful Usage**: The agent uses Google News RSS feeds, which are publicly available
- **Caching**: Consider implementing caching for repeated requests
- **Error Handling**: Always check the `status` field in responses
- **Date Formats**: Use relative dates (`7d`, `24h`) for better user experience
- **Location Specificity**: More specific locations may return fewer but more relevant results

## Data Sources

- **Primary Source**: Google News RSS feeds
- **URL Pattern**: `https://news.google.com/rss/search?q={location}&hl=en-US&gl=US&ceid=US:en`
- **Update Frequency**: Real-time (as Google News updates)
- **Geographic Coverage**: Global (location-based filtering)

## Limitations

- **RSS Feed Limitations**: Dependent on Google News RSS feed availability
- **Content Filtering**: Limited to what Google News indexes
- **Language**: Currently optimized for English (en-US)
- **Rate Limits**: Subject to Google News RSS feed rate limits
- **Content Types**: Limited to news articles (no images, videos, etc.)
