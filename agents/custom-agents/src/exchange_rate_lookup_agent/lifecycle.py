"""
Lifecycle management for Exchange Rate Lookup Agent
"""

import os
import logging
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


def initialize_exchange_rate_lookup_agent(host_component) -> Dict[str, Any]:
    """
    Initialize the Exchange Rate Lookup Agent
    
    Args:
        host_component: SAM host component
        
    Returns:
        Dict with initialization status and agent info
    """
    try:
        logger.info("🚀 Initializing Exchange Rate Lookup Agent")
        
        # Validate API key presence
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        if not api_key:
            logger.error("❌ EXCHANGE_RATE_API_KEY environment variable not set")
            return {
                "status": "error",
                "error": "EXCHANGE_RATE_API_KEY environment variable not set. Please set it before starting the agent.",
                "error_type": "missing_api_key",
                "solution": "Add EXCHANGE_RATE_API_KEY=your_api_key_here to your .env file",
                "api_website": "https://www.exchangerate-api.com/",
                "timestamp": datetime.now().isoformat()
            }
        
        # Check for empty or invalid API key values
        if api_key.strip() == "" or api_key.lower() in ["none", "null", "undefined", ""]:
            logger.error("❌ API key is empty or invalid")
            return {
                "status": "error",
                "error": "API key is empty or invalid. Please provide a valid Exchange Rate API key.",
                "error_type": "invalid_api_key",
                "solution": "Update your .env file with a valid EXCHANGE_RATE_API_KEY from https://www.exchangerate-api.com/",
                "api_website": "https://www.exchangerate-api.com/",
                "timestamp": datetime.now().isoformat()
            }
        
        # Validate API key format (basic check)
        if len(api_key) < 10:
            logger.error("❌ API key appears to be invalid (too short)")
            return {
                "status": "error",
                "error": "API key appears to be invalid (too short). Please check your EXCHANGE_RATE_API_KEY.",
                "error_type": "invalid_api_key_format",
                "solution": "Get a valid API key from https://www.exchangerate-api.com/ and update your .env file",
                "api_website": "https://www.exchangerate-api.com/",
                "timestamp": datetime.now().isoformat()
            }
        
        # Get configuration from environment variables
        base_url = os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6')
        cache_duration = int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600'))  # 1 hour default
        timeout = int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30'))  # 30 seconds default
        monthly_limit = int(os.getenv('EXCHANGE_RATE_MONTHLY_LIMIT', '1500'))  # Free plan limit
        log_level = os.getenv('EXCHANGE_RATE_LOG_LEVEL', 'INFO')
        
        # Configure logging level
        logging.getLogger().setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Initialize agent state
        agent_state = {
            "api_key": api_key,
            "base_url": base_url,
            "cache_duration": cache_duration,
            "timeout": timeout,
            "monthly_limit": monthly_limit,
            "log_level": log_level,
            "initialized_at": datetime.now().isoformat(),
            "request_count": 0,
            "cache": {},
            "rate_limits": {
                "requests_this_month": 0,
                "monthly_limit": monthly_limit,
                "last_reset": datetime.now().isoformat()
            }
        }
        
        # Store state in host component using the correct SAM method
        host_component.set_agent_specific_state("agent_state", agent_state)
        
        logger.info("✅ Exchange Rate Lookup Agent initialized successfully")
        logger.info(f"📊 Configuration: Base URL={base_url}, Cache Duration={cache_duration}s, Timeout={timeout}s, Monthly Limit={monthly_limit}, Log Level={log_level}")
        
        return {
            "status": "success",
            "message": "Exchange Rate Lookup Agent initialized successfully",
            "agent_info": {
                "name": "Exchange Rate Lookup Agent",
                "version": "1.0.0",
                "description": "Real-time currency exchange rate lookup and conversion",
                "supported_currencies": "150+ currencies including USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY",
                "api_source": "Exchange Rate API",
                "rate_limit": f"{monthly_limit} requests per month (configurable)"
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Exchange Rate Lookup Agent: {str(e)}")
        return {
            "status": "error",
            "error": f"Initialization failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


def cleanup_exchange_rate_lookup_agent(host_component) -> Dict[str, Any]:
    """
    Cleanup the Exchange Rate Lookup Agent
    
    Args:
        host_component: SAM host component
        
    Returns:
        Dict with cleanup status
    """
    try:
        logger.info("🧹 Cleaning up Exchange Rate Lookup Agent")
        
        # Get agent state
        agent_state = getattr(host_component, 'agent_state', {})
        
        # Log final statistics
        if agent_state:
            request_count = agent_state.get('request_count', 0)
            logger.info(f"📊 Final statistics: {request_count} API requests made")
            
            # Clear cache
            cache_size = len(agent_state.get('cache', {}))
            if cache_size > 0:
                logger.info(f"🗑️ Clearing cache with {cache_size} entries")
        
        # Clear agent state
        if hasattr(host_component, 'agent_state'):
            delattr(host_component, 'agent_state')
        
        logger.info("✅ Exchange Rate Lookup Agent cleaned up successfully")
        
        return {
            "status": "success",
            "message": "Exchange Rate Lookup Agent cleaned up successfully",
            "final_stats": {
                "total_requests": agent_state.get('request_count', 0) if agent_state else 0,
                "cache_entries_cleared": cache_size if agent_state else 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to cleanup Exchange Rate Lookup Agent: {str(e)}")
        return {
            "status": "error",
            "error": f"Cleanup failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
