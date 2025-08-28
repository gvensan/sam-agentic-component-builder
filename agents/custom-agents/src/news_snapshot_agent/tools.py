"""
News Snapshot Agent Tools

This module contains the tools for the News Snapshot Agent following SAM patterns.
"""

import httpx
import xml.etree.ElementTree as ET
import re
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser
from google.adk.tools import ToolContext
from solace_ai_connector.common.log import log


async def get_news_for_location(
    location: str,
    max_results: int = 20,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get news for a specific location from Google News RSS feed.
    
    Args:
        location: The location to search for (city, state, country, etc.)
        max_results: Maximum number of news articles to return (default: 20)
    
    Returns:
        Dict containing news articles and metadata
    """
    log.info(f"[GetNewsForLocation] Getting news for location: {location}")
    
    # Construct Google News RSS URL
    base_url = "https://news.google.com/rss/search"
    params = {
        "q": location,
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en"
    }
    
    # Build URL with parameters
    url = f"{base_url}?q={location}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={
                    'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                    'Accept': 'application/rss+xml, application/xml, text/xml'
                },
                timeout=15.0
            )
            response.raise_for_status()
            
            # Parse RSS XML
            root = ET.fromstring(response.text)
            
            # Extract channel information
            channel = root.find('channel')
            if channel is None:
                raise ValueError("Invalid RSS feed: no channel element found")
            
            # Parse articles
            articles = []
            for item in channel.findall('item')[:max_results]:
                article = parse_news_item(item)
                if article:
                    articles.append(article)
            
            result = {
                "status": "success",
                "location": location,
                "articles_count": len(articles),
                "articles": articles,
                "feed_info": {
                    "title": get_text(channel.find('title')),
                    "description": get_text(channel.find('description')),
                    "language": get_text(channel.find('language')),
                    "last_build_date": get_text(channel.find('lastBuildDate'))
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "google-news-rss",
                "url": url
            }
            
            log.info(f"[GetNewsForLocation] Successfully retrieved {len(articles)} articles for {location}")
            return result
            
    except httpx.RequestError as e:
        log.error(f"[GetNewsForLocation] Network error: {e}")
        return {
            "status": "error",
            "message": f"Network error: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": "network_error"
        }
    except httpx.HTTPStatusError as e:
        log.error(f"[GetNewsForLocation] HTTP error {e.response.status_code}: {e}")
        return {
            "status": "error",
            "message": f"HTTP error {e.response.status_code}: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": "http_error"
        }
    except (ValueError, ET.ParseError) as e:
        log.error(f"[GetNewsForLocation] XML parsing error: {e}")
        return {
            "status": "error",
            "message": f"XML parsing error: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": "parsing_error"
        }
    except Exception as e:
        log.error(f"[GetNewsForLocation] Unexpected error: {e}")
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": "unknown_error"
        }


async def get_news_with_date_filter(
    location: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    max_results: int = 20,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get news for a location with date range filtering.
    
    Args:
        location: The location to search for
        start_date: Start date in ISO format (YYYY-MM-DD) or relative format (e.g., "7d" for 7 days ago)
        end_date: End date in ISO format (YYYY-MM-DD) or "now" for current date
        max_results: Maximum number of news articles to return (default: 20)
    
    Returns:
        Dict containing filtered news articles
    """
    log.info(f"[GetNewsWithDateFilter] Getting news for {location} with date filter: {start_date} to {end_date}")
    
    # Get all news first
    news_result = await get_news_for_location(location, max_results * 2, tool_context, tool_config)
    
    if news_result["status"] != "success":
        return news_result
    
    # Parse date filters
    try:
        start_dt = parse_date_filter(start_date) if start_date else None
        end_dt = parse_date_filter(end_date) if end_date else datetime.now(timezone.utc)
        
        # Filter articles by date
        filtered_articles = []
        for article in news_result["articles"]:
            article_date = article.get("published_date")
            if article_date:
                try:
                    article_dt = date_parser.parse(article_date)
                    if start_dt and article_dt < start_dt:
                        continue
                    if end_dt and article_dt > end_dt:
                        continue
                    filtered_articles.append(article)
                except (ValueError, TypeError):
                    # If we can't parse the date, include the article
                    filtered_articles.append(article)
            else:
                # If no date, include the article
                filtered_articles.append(article)
        
        result = {
            "status": "success",
            "location": location,
            "date_filter": {
                "start_date": start_date,
                "end_date": end_date,
                "start_datetime": start_dt.isoformat() if start_dt else None,
                "end_datetime": end_dt.isoformat() if end_dt else None
            },
            "articles_count": len(filtered_articles),
            "total_articles_found": len(news_result["articles"]),
            "articles": filtered_articles[:max_results],
            "feed_info": news_result["feed_info"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "google-news-rss-filtered"
        }
        
        log.info(f"[GetNewsWithDateFilter] Filtered to {len(filtered_articles)} articles for {location}")
        return result
        
    except Exception as e:
        log.error(f"[GetNewsWithDateFilter] Date filtering error: {e}")
        return {
            "status": "error",
            "message": f"Date filtering error: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": "date_filter_error"
        }


async def get_news_snapshot(
    location: str,
    days_back: int = 7,
    max_results: int = 15,
    include_summary: bool = True,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get a comprehensive news snapshot for a location.
    
    Args:
        location: The location to search for
        days_back: Number of days to look back (default: 7)
        max_results: Maximum number of news articles to return (default: 15)
        include_summary: Whether to include a summary of the news (default: True)
    
    Returns:
        Dict containing news snapshot with summary
    """
    log.info(f"[GetNewsSnapshot] Getting news snapshot for {location} (last {days_back} days)")
    
    # Calculate date range
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days_back)
    
    # Get filtered news
    news_result = await get_news_with_date_filter(
        location, 
        start_date.isoformat(), 
        end_date.isoformat(), 
        max_results, 
        tool_context, 
        tool_config
    )
    
    if news_result["status"] != "success":
        return news_result
    
    # Generate summary if requested
    summary = None
    if include_summary and news_result["articles"]:
        summary = generate_news_summary(news_result["articles"], location)
    
    result = {
        "status": "success",
        "location": location,
        "snapshot_info": {
            "period_days": days_back,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "articles_count": len(news_result["articles"]),
            "summary_included": include_summary
        },
        "articles": news_result["articles"],
        "summary": summary,
        "feed_info": news_result["feed_info"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "google-news-rss-snapshot"
    }
    
    log.info(f"[GetNewsSnapshot] Generated snapshot with {len(news_result['articles'])} articles for {location}")
    return result


async def search_news_by_keywords(
    location: str,
    keywords: List[str],
    max_results: int = 15,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Search for news articles containing specific keywords in a location.
    
    Args:
        location: The location to search for
        keywords: List of keywords to search for
        max_results: Maximum number of news articles to return (default: 15)
    
    Returns:
        Dict containing filtered news articles matching keywords
    """
    log.info(f"[SearchNewsByKeywords] Searching for keywords {keywords} in {location}")
    
    # Get news for location
    news_result = await get_news_for_location(location, max_results * 2, tool_context, tool_config)
    
    if news_result["status"] != "success":
        return news_result
    
    # Filter articles by keywords
    keyword_patterns = [re.compile(keyword, re.IGNORECASE) for keyword in keywords]
    matching_articles = []
    
    for article in news_result["articles"]:
        title = article.get("title", "")
        description = article.get("description", "")
        content = f"{title} {description}"
        
        # Check if any keyword matches
        for pattern in keyword_patterns:
            if pattern.search(content):
                matching_articles.append(article)
                break
    
    result = {
        "status": "success",
        "location": location,
        "keywords": keywords,
        "articles_count": len(matching_articles),
        "total_articles_searched": len(news_result["articles"]),
        "articles": matching_articles[:max_results],
        "feed_info": news_result["feed_info"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "google-news-rss-keyword-search"
    }
    
    log.info(f"[SearchNewsByKeywords] Found {len(matching_articles)} articles matching keywords in {location}")
    return result


async def get_weather_news(
    location: str,
    weather_attributes: Optional[List[str]] = None,
    max_results: int = 15,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetch weather-related news articles for a location.
    
    Args:
        location: The location to search for weather news
        weather_attributes: List of weather attributes to search for (optional)
        max_results: Maximum number of news articles to return (default: 15)
    
    Returns:
        Dict containing weather-related news articles
    """
    log.info(f"[GetWeatherNews] Getting weather news for {location}")
    
    # Default weather attributes if none specified
    if not weather_attributes:
        weather_attributes = [
            "temperature", "weather", "climate", "forecast", "storm", "rain", "snow", 
            "heat", "cold", "hurricane", "tornado", "flood", "drought", "heatwave",
            "precipitation", "humidity", "wind", "sunny", "cloudy", "fog", "mist",
            "thunderstorm", "lightning", "weather warning", "weather alert",
            "extreme weather", "weather emergency", "weather advisory"
        ]
    
    # Get news for location
    news_result = await get_news_for_location(location, max_results * 2, tool_context, tool_config)
    
    if news_result["status"] != "success":
        return news_result
    
    # Filter articles by weather-related keywords
    weather_patterns = [re.compile(keyword, re.IGNORECASE) for keyword in weather_attributes]
    weather_articles = []
    
    for article in news_result["articles"]:
        title = article.get("title", "")
        description = article.get("description", "")
        content = f"{title} {description}"
        
        # Check if any weather keyword matches
        for pattern in weather_patterns:
            if pattern.search(content):
                weather_articles.append(article)
                break
    
    # Categorize weather articles by type
    weather_categories = {
        "temperature": [],
        "storms": [],
        "precipitation": [],
        "climate": [],
        "warnings": [],
        "general": []
    }
    
    for article in weather_articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        content = f"{title} {description}"
        
        # Categorize based on content
        if any(word in content for word in ["temperature", "heat", "cold", "freeze", "warm"]):
            weather_categories["temperature"].append(article)
        elif any(word in content for word in ["storm", "hurricane", "tornado", "thunder", "lightning"]):
            weather_categories["storms"].append(article)
        elif any(word in content for word in ["rain", "snow", "precipitation", "flood", "drought"]):
            weather_categories["precipitation"].append(article)
        elif any(word in content for word in ["climate", "global warming", "climate change"]):
            weather_categories["climate"].append(article)
        elif any(word in content for word in ["warning", "alert", "advisory", "emergency"]):
            weather_categories["warnings"].append(article)
        else:
            weather_categories["general"].append(article)
    
    result = {
        "status": "success",
        "location": location,
        "weather_attributes": weather_attributes,
        "articles_count": len(weather_articles),
        "total_articles_searched": len(news_result["articles"]),
        "articles": weather_articles[:max_results],
        "weather_categories": {
            category: len(articles) for category, articles in weather_categories.items()
        },
        "category_breakdown": weather_categories,
        "feed_info": news_result["feed_info"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "google-news-rss-weather"
    }
    
    log.info(f"[GetWeatherNews] Found {len(weather_articles)} weather-related articles for {location}")
    return result


async def get_trending_topics(
    location: str,
    max_results: int = 10,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Extract trending topics from news articles for a location.
    
    Args:
        location: The location to analyze
        max_results: Maximum number of trending topics to return (default: 10)
    
    Returns:
        Dict containing trending topics and their frequencies
    """
    log.info(f"[GetTrendingTopics] Extracting trending topics for {location}")
    
    # Get recent news
    news_result = await get_news_for_location(location, 50, tool_context, tool_config)
    
    if news_result["status"] != "success":
        return news_result
    
    # Extract topics from titles and descriptions
    topic_freq = {}
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs'}
    
    for article in news_result["articles"]:
        title = article.get("title", "")
        description = article.get("description", "")
        content = f"{title} {description}"
        
        # Extract words (simple approach)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
        
        for word in words:
            if word not in stop_words and len(word) > 2:
                topic_freq[word] = topic_freq.get(word, 0) + 1
    
    # Sort by frequency and get top topics
    sorted_topics = sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)
    trending_topics = [
        {"topic": topic, "frequency": freq, "percentage": round((freq / len(news_result["articles"])) * 100, 1)}
        for topic, freq in sorted_topics[:max_results]
    ]
    
    result = {
        "status": "success",
        "location": location,
        "trending_topics": trending_topics,
        "total_articles_analyzed": len(news_result["articles"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "google-news-rss-trending"
    }
    
    log.info(f"[GetTrendingTopics] Extracted {len(trending_topics)} trending topics for {location}")
    return result


def parse_news_item(item: ET.Element) -> Optional[Dict[str, Any]]:
    """Parse a news item from RSS XML."""
    try:
        title = get_text(item.find('title'))
        link = get_text(item.find('link'))
        description = get_text(item.find('description'))
        pub_date = get_text(item.find('pubDate'))
        source = get_text(item.find('source'))
        
        # Clean up description (remove HTML tags)
        if description:
            description = re.sub(r'<[^>]+>', '', description)
            description = re.sub(r'\s+', ' ', description).strip()
        
        # Parse publication date
        published_date = None
        if pub_date:
            try:
                published_date = date_parser.parse(pub_date).isoformat()
            except (ValueError, TypeError):
                published_date = pub_date
        
        return {
            "title": title,
            "link": link,
            "description": description,
            "published_date": published_date,
            "source": source,
            "raw_pub_date": pub_date
        }
    except Exception as e:
        log.warning(f"[ParseNewsItem] Failed to parse news item: {e}")
        return None


def get_text(element: Optional[ET.Element]) -> str:
    """Safely get text from XML element."""
    if element is not None and element.text:
        return element.text.strip()
    return ""


def parse_date_filter(date_str: str) -> datetime:
    """Parse date filter string into datetime object."""
    if not date_str:
        return datetime.now(timezone.utc)
    
    # Handle relative dates
    if date_str.lower() == "now":
        return datetime.now(timezone.utc)
    
    # Handle relative formats like "7d", "24h", "1w"
    relative_match = re.match(r'^(\d+)([dhwmy])$', date_str.lower())
    if relative_match:
        value = int(relative_match.group(1))
        unit = relative_match.group(2)
        
        now = datetime.now(timezone.utc)
        if unit == 'd':
            return now - timedelta(days=value)
        elif unit == 'h':
            return now - timedelta(hours=value)
        elif unit == 'w':
            return now - timedelta(weeks=value)
        elif unit == 'm':
            return now - timedelta(days=value * 30)  # Approximate
        elif unit == 'y':
            return now - timedelta(days=value * 365)  # Approximate
    
    # Handle ISO format dates
    try:
        return date_parser.parse(date_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid date format: {date_str}")


def generate_news_summary(articles: List[Dict[str, Any]], location: str) -> Dict[str, Any]:
    """Generate a summary of news articles."""
    if not articles:
        return {"summary": "No news articles found", "top_stories": []}
    
    # Extract top stories (first 5)
    top_stories = articles[:5]
    
    # Count sources
    sources = {}
    for article in articles:
        source = article.get("source", "Unknown")
        sources[source] = sources.get(source, 0) + 1
    
    # Find most common topics
    topic_freq = {}
    for article in articles:
        title = article.get("title", "")
        words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
        for word in words:
            if word not in {'news', 'report', 'says', 'said', 'will', 'have', 'been', 'this', 'that', 'with', 'from', 'they', 'their'}:
                topic_freq[word] = topic_freq.get(word, 0) + 1
    
    top_topics = sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    
    summary = {
        "location": location,
        "total_articles": len(articles),
        "top_stories": [
            {
                "title": article.get("title", ""),
                "source": article.get("source", ""),
                "published_date": article.get("published_date", "")
            }
            for article in top_stories
        ],
        "top_sources": sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3],
        "trending_topics": [{"topic": topic, "count": count} for topic, count in top_topics],
        "summary_text": f"Found {len(articles)} news articles for {location}. Top sources include {', '.join([s[0] for s in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3]])}."
    }
    
    return summary
