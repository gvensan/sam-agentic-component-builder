# News Snapshot Agent - API Reference

## Overview

The News Snapshot Agent provides comprehensive news information from Google News RSS feeds with advanced filtering, analysis, and trending topic extraction capabilities. This agent can fetch location-based news, filter by date ranges, search by keywords, and analyze trending topics.

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- SAM framework
- Required dependencies (see `requirements.txt`)

### Installation
```bash
# Install agent-specific dependencies
pip install -r requirements.txt

# Or install individual packages
pip install httpx python-dateutil pytest pytest-asyncio
```

### Dependencies
This agent requires the following custom packages:
- **httpx**: Async HTTP client for RSS feed retrieval
- **python-dateutil**: Date parsing and manipulation for filtering
- **pytest & pytest-asyncio**: Testing framework
- **xml.etree.ElementTree**: Built-in XML parsing for RSS feeds
- **re**: Built-in regular expressions for text processing

## 📰 Available Tools

### 1. Basic News Retrieval
**Tool**: `get_news_for_location`

Retrieves news articles for a specific location from Google News RSS feed.

**Parameters**:
- `location` (str): The location to search for (city, state, country, etc.)
- `max_results` (int, optional): Maximum number of articles to return (default: 20)

**Returns**:
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

**Example Usage**:
```
User: "Get news for New York"
Agent: Uses get_news_for_location("New York") to retrieve latest news articles.
```

### 2. Date Filtered News
**Tool**: `get_news_with_date_filter`

Retrieves news articles with date range filtering using multiple date formats.

**Parameters**:
- `location` (str): The location to search for
- `start_date` (str, optional): Start date in various formats
- `end_date` (str, optional): End date in various formats
- `max_results` (int, optional): Maximum number of articles to return (default: 20)

**Supported Date Formats**:
- ISO format: `"2024-01-01"` or `"2024-01-01T10:00:00Z"`
- Relative format: `"7d"` (7 days ago), `"24h"` (24 hours ago), `"1w"` (1 week ago), `"1m"` (1 month ago), `"1y"` (1 year ago)
- Keywords: `"now"` (current time)

**Returns**:
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

**Example Usage**:
```
User: "Show me news from San Francisco from the last 7 days"
Agent: Uses get_news_with_date_filter("San Francisco", "7d", "now") to get filtered news.
```

### 3. Comprehensive News Snapshot
**Tool**: `get_news_snapshot`

Generates a comprehensive news snapshot with summary and analysis.

**Parameters**:
- `location` (str): The location to search for
- `days_back` (int, optional): Number of days to look back (default: 7)
- `max_results` (int, optional): Maximum number of articles to return (default: 15)
- `include_summary` (bool, optional): Whether to include summary (default: True)

**Returns**:
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

**Example Usage**:
```
User: "Give me a news snapshot for Chicago from the last 3 days"
Agent: Uses get_news_snapshot("Chicago", days_back=3, include_summary=True) to create comprehensive snapshot.
```

### 4. Keyword Search
**Tool**: `search_news_by_keywords`

Searches for news articles containing specific keywords within a location.

**Parameters**:
- `location` (str): The location to search for
- `keywords` (List[str]): List of keywords to search for
- `max_results` (int, optional): Maximum number of articles to return (default: 15)

**Returns**:
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

**Example Usage**:
```
User: "Search for technology news in Seattle"
Agent: Uses search_news_by_keywords("Seattle", ["technology"]) to find relevant articles.
```

### 5. Weather News Retrieval
**Tool**: `get_weather_news`

Fetches weather-related news articles for a location with categorization.

**Parameters**:
- `location` (str): The location to search for weather news
- `weather_attributes` (List[str], optional): List of weather attributes to search for
- `max_results` (int, optional): Maximum number of articles to return (default: 15)

**Supported Weather Attributes**:
- Temperature: "temperature", "heat", "cold", "freeze", "warm"
- Storms: "storm", "hurricane", "tornado", "thunder", "lightning"
- Precipitation: "rain", "snow", "precipitation", "flood", "drought"
- Climate: "climate", "global warming", "climate change"
- Warnings: "warning", "alert", "advisory", "emergency"
- General: "weather", "forecast", "humidity", "wind", "sunny", "cloudy"

**Returns**:
```json
{
  "status": "success",
  "location": "Miami",
  "weather_attributes": ["temperature", "storm", "rain", "weather"],
  "articles_count": 12,
  "total_articles_searched": 30,
  "articles": [...],
  "weather_categories": {
    "temperature": 3,
    "storms": 5,
    "precipitation": 2,
    "climate": 1,
    "warnings": 2,
    "general": 1
  },
  "category_breakdown": {
    "temperature": [...],
    "storms": [...],
    "precipitation": [...],
    "climate": [...],
    "warnings": [...],
    "general": [...]
  },
  "feed_info": {...},
  "timestamp": "2024-01-01T10:00:00Z",
  "source": "google-news-rss-weather"
}
```

**Example Usage**:
```
User: "Get weather news for Miami"
Agent: Uses get_weather_news("Miami") to fetch and categorize weather-related articles.
```

### 6. Trending Topics Analysis
**Tool**: `get_trending_topics`

Extracts trending topics from news articles for a location.

**Parameters**:
- `location` (str): The location to analyze
- `max_results` (int, optional): Maximum number of trending topics to return (default: 10)

**Returns**:
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

**Example Usage**:
```
User: "What are the trending topics in Austin?"
Agent: Uses get_trending_topics("Austin") to analyze and extract trending topics.
```

## 🎯 Natural Language Queries

The agent understands various natural language patterns:

### Basic News Retrieval
- "Get news for New York"
- "Show me the latest news from London"
- "What's happening in Tokyo?"

### Date Filtered News
- "Get news from San Francisco from the last 7 days"
- "Show me Austin news from yesterday"
- "What happened in Chicago between January 1st and January 7th?"

### Keyword Search
- "Search for technology news in Seattle"
- "Find business articles about startups in Austin"
- "Look for sports news in Miami"

### Weather News
- "Get weather news for Miami"
- "Show me storm-related news in Houston"
- "Find temperature news for Phoenix"
- "Get weather warnings for Florida"

### Trending Analysis
- "What are the trending topics in Boston?"
- "Show me the most discussed topics in Denver"
- "Analyze trending topics in Phoenix"

### Comprehensive Snapshots
- "Give me a news snapshot for Chicago from the last 3 days"
- "Create a comprehensive news summary for Los Angeles"
- "Show me a news overview for Dallas with trending topics"

## 🔧 Configuration

### Agent Configuration
The agent is configured via `configs/agents/news_snapshot_agent.yaml`:

- **Model Configuration**: LLM model settings for natural language processing
- **Tool Configuration**: Available tools and their descriptions
- **Lifecycle Functions**: Initialization and cleanup functions
- **Agent Instructions**: Natural language instructions for the agent

### Environment Variables
- `NAMESPACE`: Required namespace for SAM deployment

## 📊 Data Sources

### Google News RSS Feeds
- **URL Pattern**: `https://news.google.com/rss/search?q={location}&hl=en-US&gl=US&ceid=US:en`
- **Update Frequency**: Real-time (as Google News updates)
- **Geographic Coverage**: Global
- **Language**: English (en-US)

### RSS Feed Structure
The agent parses standard RSS 2.0 feeds with the following structure:
```xml
<rss>
  <channel>
    <title>Google News</title>
    <description>News feed description</description>
    <item>
      <title>Article Title</title>
      <link>Article URL</link>
      <description>Article description</description>
      <pubDate>Publication date</pubDate>
      <source>News source</source>
    </item>
  </channel>
</rss>
```

## 🚨 Error Handling

The agent provides comprehensive error handling with consistent response formats:

### Error Response Format
```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": "2024-01-01T10:00:00Z",
  "error_type": "error_category"
}
```

### Common Error Types
- `network_error`: Network connectivity issues
- `http_error`: HTTP status code errors
- `parsing_error`: XML/RSS parsing issues
- `date_filter_error`: Date format parsing errors
- `unknown_error`: Unexpected errors

## 📈 Performance & Best Practices

### Optimization Tips
1. **Use Specific Locations**: More specific locations return more relevant results
2. **Leverage Date Filtering**: Use date filters to reduce data volume
3. **Implement Caching**: Cache results for repeated requests
4. **Handle Errors Gracefully**: Always check the `status` field in responses

### Rate Limiting
- Respect Google News RSS feed rate limits
- Implement appropriate delays between requests
- Use caching for frequently requested data

### Monitoring
The agent provides built-in statistics:
- Total requests processed
- Success/failure rates
- Unique locations searched
- Performance metrics

## 🔒 Security & Privacy

### Data Handling
- No personal data is stored or processed
- All requests are made to public RSS feeds
- No authentication required for basic functionality

### Privacy Considerations
- RSS feeds are publicly available
- No user data is collected or stored
- All processing is done in-memory

## 🛠️ Development

### Project Structure
```
src/news_snapshot_agent/
├── __init__.py                 # Module initialization
├── tools.py                    # Core functionality and tools
├── lifecycle.py                # Agent lifecycle management
├── README.md                   # This documentation
└── tests/
    ├── __init__.py
    └── test_news_agent.py     # Comprehensive test suite
```

### Running Tests
```bash
# Run all tests
python -m pytest src/news_snapshot_agent/tests/

# Run specific test file
python src/news_snapshot_agent/tests/test_news_agent.py

# Run with verbose output
python -m pytest src/news_snapshot_agent/tests/ -v
```

### Adding New Features

1. **Add New Tool Function**
   ```python
   async def new_tool_function(
       param1: str,
       param2: int = 10,
       tool_context: Optional[ToolContext] = None,
       tool_config: Optional[Dict[str, Any]] = None
   ) -> Dict[str, Any]:
       """Description of the new tool."""
       # Implementation here
       pass
   ```

2. **Update Configuration**
   Add the tool to `configs/agents/news_snapshot_agent.yaml`:
   ```yaml
   - tool_type: python
     component_module: "src.news_snapshot_agent.tools"
     component_base_path: .
     function_name: "new_tool_function"
     tool_description: "Description of the new tool"
   ```

3. **Add Tests**
   Create corresponding tests in `tests/test_news_agent.py`

## 🆘 Troubleshooting

### Common Issues
1. **Network Errors**: Check internet connectivity and firewall settings
2. **Date Parsing Errors**: Verify date format compatibility
3. **Empty Results**: Try different location names or date ranges
4. **Deployment Issues**: Ensure SAM CLI is properly configured

### Getting Help
- Check this API reference documentation
- Review the test files for usage examples
- Run the demo script: `python demo_news_agent.py`
- Examine the error messages for specific issues
- Consult the SAM documentation for deployment issues

## 📄 License

This agent follows the same license as the parent SAM project.

---

**Happy News Snapshotting! 📰✨**
