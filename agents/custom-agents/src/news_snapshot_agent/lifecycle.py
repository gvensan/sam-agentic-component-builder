"""
News Snapshot Agent Lifecycle Functions

This module contains initialization and cleanup functions for the News Snapshot Agent.
"""

import asyncio
from typing import Any
from solace_ai_connector.common.log import log


def initialize_news_snapshot_agent(host_component: Any):
    """
    Initialize the News Snapshot Agent.
    
    Args:
        host_component: The agent host component
    """
    log_identifier = f"[{host_component.agent_name}:init]"
    log.info(f"{log_identifier} Starting News Snapshot Agent initialization...")
    
    try:
        # Store initialization metadata
        host_component.set_agent_specific_state("initialized_at", "2024-01-01T00:00:00Z")
        host_component.set_agent_specific_state("news_requests_count", 0)
        host_component.set_agent_specific_state("agent_version", "1.0.0")
        
        # Initialize service configuration
        service_config = {
            "google_news_rss_url": "https://news.google.com/rss/search",
            "default_timeout": 15,
            "max_retries": 3,
            "default_max_results": 20,
            "cache_duration_minutes": 30,
            "supported_date_formats": [
                "ISO format (YYYY-MM-DD)",
                "Relative format (7d, 24h, 1w, 1m, 1y)",
                "Now keyword"
            ]
        }
        host_component.set_agent_specific_state("service_config", service_config)
        
        # Initialize statistics
        stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "locations_searched": set(),
            "last_request_time": None
        }
        host_component.set_agent_specific_state("statistics", stats)
        
        # Log startup message
        log.info(f"{log_identifier} News Snapshot Agent initialization completed successfully")
        log.info(f"{log_identifier} Agent is ready to provide news snapshots from Google News RSS feeds")
        log.info(f"{log_identifier} Supported features: location-based news, date filtering, keyword search, trending topics")
        
    except Exception as e:
        log.error(f"{log_identifier} Failed to initialize News Snapshot Agent: {e}")
        raise


def cleanup_news_snapshot_agent(host_component: Any):
    """
    Clean up News Snapshot Agent resources.
    
    Args:
        host_component: The agent host component
    """
    log_identifier = f"[{host_component.agent_name}:cleanup]"
    log.info(f"{log_identifier} Starting News Snapshot Agent cleanup...")

    async def cleanup_async(host_component: Any):
        try:
            # Get final statistics
            stats = host_component.get_agent_specific_state("statistics", {})
            request_count = stats.get("total_requests", 0)
            successful_requests = stats.get("successful_requests", 0)
            failed_requests = stats.get("failed_requests", 0)
            locations_searched = len(stats.get("locations_searched", set()))
            initialized_at = host_component.get_agent_specific_state("initialized_at", "unknown")
            
            log.info(f"{log_identifier} Agent processed {request_count} news requests during its lifetime")
            log.info(f"{log_identifier} Successful requests: {successful_requests}")
            log.info(f"{log_identifier} Failed requests: {failed_requests}")
            log.info(f"{log_identifier} Unique locations searched: {locations_searched}")
            log.info(f"{log_identifier} Agent was initialized at: {initialized_at}")
            
            # Calculate success rate
            if request_count > 0:
                success_rate = (successful_requests / request_count) * 100
                log.info(f"{log_identifier} Success rate: {success_rate:.1f}%")
            
            # Clean up any remaining resources
            # Note: Service cleanup is handled automatically by the service layer
            
            log.info(f"{log_identifier} News Snapshot Agent cleanup completed successfully")
        
        except Exception as e:
            log.error(f"{log_identifier} Error during cleanup: {e}")
    
    # Run cleanup in the event loop
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a task
            asyncio.create_task(cleanup_async(host_component))
        else:
            # Otherwise, run until complete
            loop.run_until_complete(cleanup_async(host_component))
    except RuntimeError:
        # If no event loop is available, create a new one
        asyncio.run(cleanup_async(host_component))
    
    log.info(f"{log_identifier} News Snapshot Agent cleanup completed")
