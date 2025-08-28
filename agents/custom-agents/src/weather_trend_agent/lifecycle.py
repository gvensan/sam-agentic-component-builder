"""
Weather History Agent Lifecycle Functions

This module contains initialization and cleanup functions for the Weather History Agent.
"""

import asyncio
from typing import Any
from solace_ai_connector.common.log import log


def initialize_weather_trend_agent(host_component: Any):
    """
    Initialize the Weather Trend Agent.
    
    Args:
        host_component: The agent host component
    """
    log_identifier = f"[{host_component.agent_name}:init]"
    log.info(f"{log_identifier} Starting Weather Trend Agent initialization...")
    
    try:
        # Store initialization metadata
        host_component.set_agent_specific_state("initialized_at", "2024-01-01T00:00:00Z")
        host_component.set_agent_specific_state("weather_requests_count", 0)
        host_component.set_agent_specific_state("agent_version", "1.0.0")
        
        # Initialize service configuration
        service_config = {
            "forecast_url": "https://api.open-meteo.com/v1/forecast",
            "archive_url": "https://archive-api.open-meteo.com/v1/archive",
            "geocoding_url": "https://geocoding-api.open-meteo.com/v1/search",
            "timeout": 15,
            "max_retries": 3
        }
        host_component.set_agent_specific_state("service_config", service_config)
        
        # Log startup message
        log.info(f"{log_identifier} Weather Trend Agent initialization completed successfully")
        log.info(f"{log_identifier} Agent is ready to provide historical weather data")
        
    except Exception as e:
        log.error(f"{log_identifier} Failed to initialize Weather History Agent: {e}")
        raise


def cleanup_weather_trend_agent(host_component: Any):
    """
    Clean up Weather Trend Agent resources.
    
    Args:
        host_component: The agent host component
    """
    log_identifier = f"[{host_component.agent_name}:cleanup]"
    log.info(f"{log_identifier} Starting Weather Trend Agent cleanup...")

    async def cleanup_async(host_component: Any):
        try:
            # Get final statistics
            request_count = host_component.get_agent_specific_state("weather_requests_count", 0)
            initialized_at = host_component.get_agent_specific_state("initialized_at", "unknown")
            
            log.info(f"{log_identifier} Agent processed {request_count} weather requests during its lifetime")
            log.info(f"{log_identifier} Agent was initialized at: {initialized_at}")
            
            # Clean up any remaining resources
            # Note: Service cleanup is handled automatically by the service layer
            
            log.info(f"{log_identifier} Weather Trend Agent cleanup completed successfully")
        
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
    
    log.info(f"{log_identifier} Weather Trend Agent cleanup completed")
