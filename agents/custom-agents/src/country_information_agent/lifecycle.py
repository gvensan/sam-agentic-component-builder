"""
Country Information Agent Lifecycle Functions

This module contains initialization and cleanup functions for the Country Information Agent.
"""

import asyncio
from typing import Any
from solace_ai_connector.common.log import log
from .services.country_service import close_country_service


def initialize_country_information_agent(host_component: Any):
    """
    Initialize the Country Information Agent.
    
    Args:
        host_component: The agent host component
    """
    log_identifier = f"[{host_component.agent_name}:init]"
    log.info(f"{log_identifier} Starting Country Information Agent initialization...")
    
    try:
        # Store initialization metadata
        host_component.set_agent_specific_state("initialized_at", "2024-01-01T00:00:00Z")
        host_component.set_agent_specific_state("country_requests_count", 0)
        host_component.set_agent_specific_state("agent_version", "1.0.0")
        
        # Initialize service configuration
        service_config = {
            "rest_countries_api_url": "https://restcountries.com/v3.1",
            "default_timeout": 30,
            "max_retries": 3,
            "cache_duration_hours": 24,
            "max_comparison_count": 5,
            "supported_search_types": [
                "name",
                "code", 
                "partial_match",
                "region",
                "subregion"
            ]
        }
        host_component.set_agent_specific_state("service_config", service_config)
        
        # Initialize statistics
        stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "countries_searched": set(),
            "most_requested_countries": {},
            "last_request_time": None,
            "cache_hits": 0,
            "cache_misses": 0
        }
        host_component.set_agent_specific_state("statistics", stats)
        
        # Initialize popular countries cache
        popular_countries = [
            "United States", "China", "India", "Japan", "Germany",
            "United Kingdom", "France", "Brazil", "Italy", "Canada",
            "Australia", "Spain", "Mexico", "South Korea", "Russia"
        ]
        host_component.set_agent_specific_state("popular_countries", popular_countries)
        
        # Log startup message
        log.info(f"{log_identifier} Country Information Agent initialization completed successfully")
        log.info(f"{log_identifier} Agent is ready to provide comprehensive country information")
        log.info(f"{log_identifier} Supported features: country lookup, search, borders, comparison, all countries")
        log.info(f"{log_identifier} Data source: REST Countries API (https://restcountries.com/v3.1)")
        
    except Exception as e:
        log.error(f"{log_identifier} Failed to initialize Country Information Agent: {e}")
        raise


def cleanup_country_information_agent(host_component: Any):
    """
    Clean up Country Information Agent resources.
    
    Args:
        host_component: The agent host component
    """
    log_identifier = f"[{host_component.agent_name}:cleanup]"
    log.info(f"{log_identifier} Starting Country Information Agent cleanup...")

    async def cleanup_async(host_component: Any):
        try:
            # Get final statistics
            stats = host_component.get_agent_specific_state("statistics", {})
            request_count = stats.get("total_requests", 0)
            successful_requests = stats.get("successful_requests", 0)
            failed_requests = stats.get("failed_requests", 0)
            countries_searched = len(stats.get("countries_searched", set()))
            cache_hits = stats.get("cache_hits", 0)
            cache_misses = stats.get("cache_misses", 0)
            initialized_at = host_component.get_agent_specific_state("initialized_at", "unknown")
            
            log.info(f"{log_identifier} Agent processed {request_count} country requests during its lifetime")
            log.info(f"{log_identifier} Successful requests: {successful_requests}")
            log.info(f"{log_identifier} Failed requests: {failed_requests}")
            log.info(f"{log_identifier} Unique countries searched: {countries_searched}")
            log.info(f"{log_identifier} Cache hits: {cache_hits}, Cache misses: {cache_misses}")
            log.info(f"{log_identifier} Agent was initialized at: {initialized_at}")
            
            # Calculate success rate
            if request_count > 0:
                success_rate = (successful_requests / request_count) * 100
                log.info(f"{log_identifier} Success rate: {success_rate:.1f}%")
            
            # Calculate cache efficiency
            total_cache_requests = cache_hits + cache_misses
            if total_cache_requests > 0:
                cache_efficiency = (cache_hits / total_cache_requests) * 100
                log.info(f"{log_identifier} Cache efficiency: {cache_efficiency:.1f}%")
            
            # Log most requested countries
            most_requested = stats.get("most_requested_countries", {})
            if most_requested:
                sorted_countries = sorted(most_requested.items(), key=lambda x: x[1], reverse=True)
                log.info(f"{log_identifier} Top 5 most requested countries:")
                for country, count in sorted_countries[:5]:
                    log.info(f"{log_identifier}   - {country}: {count} requests")
            
            # Close the country service
            await close_country_service()
            
            log.info(f"{log_identifier} Country Information Agent cleanup completed successfully")
        
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
    
    log.info(f"{log_identifier} Country Information Agent cleanup completed")
