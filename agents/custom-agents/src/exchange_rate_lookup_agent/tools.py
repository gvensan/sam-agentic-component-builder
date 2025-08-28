"""
Exchange Rate Lookup Agent Tools

Core functions for currency exchange rate lookup and conversion using the Exchange Rate API.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from google.adk.tools import ToolContext
from solace_ai_connector.common.log import log

try:
    from .services.exchange_rate_service import ExchangeRateService
    from .services.currency_validator import CurrencyValidator
    from .services.rate_limiter import RateLimiter
    from .services.cache_manager import CacheManager
except ImportError:
    # For testing purposes
    from services.exchange_rate_service import ExchangeRateService
    from services.currency_validator import CurrencyValidator
    from services.rate_limiter import RateLimiter
    from services.cache_manager import CacheManager

# Configure logging
logger = logging.getLogger(__name__)


def _get_agent_state(tool_context, log_identifier):
    """Helper function to get agent state from tool context"""
    # Try different methods to access agent state
    agent_state = {}
    import os
    env_api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    
    if tool_context:
        if hasattr(tool_context, 'get_agent_specific_state'):
            try:
                agent_state = tool_context.get_agent_specific_state("agent_state", {})
            except Exception as e:
                log.error(f"{log_identifier} Error calling get_agent_specific_state: {e}")
                agent_state = {}
        elif hasattr(tool_context, 'state'):
            try:
                agent_state = getattr(tool_context.state, 'agent_state', {})
            except Exception as e:
                log.error(f"{log_identifier} Error accessing tool_context.state: {e}")
                agent_state = {}
        else:
            # Fallback: try to get from environment variables directly
            agent_state = {
                'api_key': env_api_key,
                'base_url': os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6'),
                'timeout': int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30')),
                'cache_duration': int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600')),
                'request_count': 0,
                'initialized_at': datetime.now().isoformat()
            }
    else:
        # No tool context, use environment variables directly
        agent_state = {
            'api_key': env_api_key,
            'base_url': os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6'),
            'timeout': int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30')),
            'cache_duration': int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600')),
            'request_count': 0,
            'initialized_at': datetime.now().isoformat()
        }
    
    # If agent state is empty but we have environment variables, create state from environment
    if not agent_state and env_api_key:
        log.info(f"{log_identifier} Agent state is empty but API key available in environment, creating state from environment variables")
        agent_state = {
            'api_key': env_api_key,
            'base_url': os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6'),
            'timeout': int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30')),
            'cache_duration': int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600')),
            'request_count': 0,
            'initialized_at': datetime.now().isoformat()
        }
    
    return agent_state


async def get_exchange_rates(
    base_currency: str,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get current exchange rates from a base currency to all supported currencies
    
    Args:
        base_currency: ISO 4217 currency code (e.g., "USD", "EUR", "GBP")
        tool_context: Tool context object
        tool_config: Tool configuration
        
    Returns:
        Dict with exchange rates for all supported currencies from the base currency
    """
    log_identifier = f"[ExchangeRateAgent:get_exchange_rates]"
    log.info(f"{log_identifier} Getting exchange rates for base currency: {base_currency}")
    
    try:
        # Validate currency code
        is_valid, error_msg = CurrencyValidator.validate_currency_code(base_currency)
        if not is_valid:
            return {
                "status": "error",
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
        
        # Get agent state using the correct SAM method
        log.info(f"{log_identifier} Tool context type: {type(tool_context)}")
        log.info(f"{log_identifier} Tool context attributes: {dir(tool_context) if tool_context else 'None'}")
        
        agent_state = _get_agent_state(tool_context, log_identifier)
        
        if not agent_state:
            log.error(f"{log_identifier} Agent state is empty or None")
            return {
                "status": "error",
                "error": "Agent not properly initialized. Please restart the agent.",
                "timestamp": datetime.now().isoformat()
            }
        
        # Initialize services
        api_key = agent_state.get('api_key')
        base_url = agent_state.get('base_url', 'https://v6.exchangerate-api.com/v6')
        timeout = agent_state.get('timeout', 30)
        cache_duration = agent_state.get('cache_duration', 3600)
        
        # Check for missing API key
        if not api_key:
            log.error(f"{log_identifier} API key is missing from agent configuration")
            return {
                "status": "error",
                "error": "API key is missing. Please configure the EXCHANGE_RATE_API_KEY in your .env file or agent configuration.",
                "error_type": "missing_api_key",
                "solution": "Add EXCHANGE_RATE_API_KEY=your_api_key_here to your .env file or agent configuration",
                "timestamp": datetime.now().isoformat()
            }
        
        # Check for empty or invalid API key
        if api_key.strip() == "" or api_key.lower() in ["none", "null", "undefined", ""]:
            log.error(f"{log_identifier} API key is empty or invalid")
            return {
                "status": "error",
                "error": "API key is empty or invalid. Please provide a valid Exchange Rate API key.",
                "error_type": "invalid_api_key",
                "solution": "Update your .env file with a valid EXCHANGE_RATE_API_KEY from https://www.exchangerate-api.com/",
                "timestamp": datetime.now().isoformat()
            }
        
        # Get or initialize rate limiter and cache
        rate_limiter = getattr(tool_context, '_rate_limiter', None) if tool_context else None
        if rate_limiter is None:
            rate_limiter = RateLimiter()
            if tool_context and hasattr(tool_context, "set_agent_specific_state"):
                setattr(tool_context, '_rate_limiter', rate_limiter)
            
        cache_manager = getattr(tool_context, '_cache_manager', None) if tool_context else None
        if cache_manager is None:
            cache_manager = CacheManager(default_ttl=cache_duration)
            if tool_context and hasattr(tool_context, "set_agent_specific_state"):
                setattr(tool_context, '_cache_manager', cache_manager)
        
        # Check rate limits
        if not rate_limiter.can_make_request():
            return {
                "status": "error",
                "error": "Monthly API quota exceeded. Please upgrade your plan or wait until next month.",
                "error_type": "quota_exceeded",
                "timestamp": datetime.now().isoformat()
            }
        
        # Check cache first
        cache_key = cache_manager.generate_cache_key(base_currency.upper())
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            log.info(f"{log_identifier} Returning cached exchange rates for {base_currency}")
            return {
                "status": "success",
                "data": cached_data,
                "cached": True,
                "timestamp": datetime.now().isoformat(),
                "source": "exchangerate-api"
            }
        
        # Make API request
        async with ExchangeRateService(api_key, base_url, timeout) as service:
            result = await service.get_latest_rates(base_currency.upper())
            
            if result["status"] == "success":
                # Record the request
                rate_limiter.record_request()
                
                # Update agent state
                agent_state['request_count'] = agent_state.get('request_count', 0) + 1
                if tool_context and hasattr(tool_context, "set_agent_specific_state"):
                    tool_context.set_agent_specific_state("agent_state", agent_state)
                
                # Cache the result
                cache_manager.set(cache_key, result["data"])
                
                # Add quota warning if needed
                quota_warning = rate_limiter.get_quota_warning()
                if quota_warning:
                    result["quota_warning"] = quota_warning
                
                log.info(f"{log_identifier} Successfully retrieved exchange rates for {base_currency}")
                return result
            else:
                log.error(f"{log_identifier} Failed to get exchange rates for {base_currency}: {result.get('error')}")
                return result
                
    except Exception as e:
        log.error(f"{log_identifier} Unexpected error in get_exchange_rates: {str(e)}")
        
        # Provide more specific error messages for common issues
        error_message = str(e)
        if "401" in error_message or "unauthorized" in error_message.lower():
            return {
                "status": "error",
                "error": "API key is invalid or expired. Please check your EXCHANGE_RATE_API_KEY configuration.",
                "error_type": "authentication_error",
                "solution": "Verify your API key at https://www.exchangerate-api.com/ and update your .env file",
                "timestamp": datetime.now().isoformat()
            }
        elif "429" in error_message or "rate limit" in error_message.lower():
            return {
                "status": "error",
                "error": "API rate limit exceeded. Please wait before making another request.",
                "error_type": "rate_limit_error",
                "solution": "Wait a few minutes before trying again, or upgrade your API plan",
                "timestamp": datetime.now().isoformat()
            }
        elif "connection" in error_message.lower() or "timeout" in error_message.lower():
            return {
                "status": "error",
                "error": "Network connection error. Please check your internet connection.",
                "error_type": "network_error",
                "solution": "Check your internet connection and try again",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "error",
                "error": f"Unexpected error: {error_message}",
                "error_type": "unknown_error",
                "timestamp": datetime.now().isoformat()
            }


async def convert_currency(
    from_currency: str,
    to_currency: str,
    amount: float,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Convert a specific amount from one currency to another
    
    Args:
        from_currency: Source currency code
        to_currency: Target currency code
        amount: Amount to convert
        tool_context: Tool context object
        tool_config: Tool configuration
        
    Returns:
        Dict with conversion result including original amount, converted amount, and exchange rate
    """
    log_identifier = f"[ExchangeRateAgent:convert_currency]"
    log.info(f"{log_identifier} Converting {amount} {from_currency} to {to_currency}")
    
    try:
        # Validate inputs
        is_valid, error_msg = CurrencyValidator.validate_currency_code(from_currency)
        if not is_valid:
            return {
                "status": "error",
                "error": f"Invalid from_currency: {error_msg}",
                "timestamp": datetime.now().isoformat()
            }
            
        is_valid, error_msg = CurrencyValidator.validate_currency_code(to_currency)
        if not is_valid:
            return {
                "status": "error",
                "error": f"Invalid to_currency: {error_msg}",
                "timestamp": datetime.now().isoformat()
            }
            
        is_valid, error_msg = CurrencyValidator.validate_amount(amount)
        if not is_valid:
            return {
                "status": "error",
                "error": f"Invalid amount: {error_msg}",
                "timestamp": datetime.now().isoformat()
            }
        
        # Get agent state using the correct SAM method
        log.info(f"{log_identifier} Tool context type: {type(tool_context)}")
        log.info(f"{log_identifier} Tool context attributes: {dir(tool_context) if tool_context else 'None'}")
        
        agent_state = _get_agent_state(tool_context, log_identifier)
        
        if not agent_state:
            log.error(f"{log_identifier} Agent state is empty or None")
            return {
                "status": "error",
                "error": "Agent not properly initialized. Please restart the agent.",
                "timestamp": datetime.now().isoformat()
            }
        
        # Initialize services
        api_key = agent_state.get('api_key')
        base_url = agent_state.get('base_url', 'https://v6.exchangerate-api.com/v6')
        timeout = agent_state.get('timeout', 30)
        cache_duration = agent_state.get('cache_duration', 3600)
        
        # Check for missing API key
        if not api_key:
            log.error(f"{log_identifier} API key is missing from agent configuration")
            return {
                "status": "error",
                "error": "API key is missing. Please configure the EXCHANGE_RATE_API_KEY in your .env file or agent configuration.",
                "error_type": "missing_api_key",
                "solution": "Add EXCHANGE_RATE_API_KEY=your_api_key_here to your .env file or agent configuration",
                "timestamp": datetime.now().isoformat()
            }
        
        # Check for empty or invalid API key
        if api_key.strip() == "" or api_key.lower() in ["none", "null", "undefined", ""]:
            log.error(f"{log_identifier} API key is empty or invalid")
            return {
                "status": "error",
                "error": "API key is empty or invalid. Please provide a valid Exchange Rate API key.",
                "error_type": "invalid_api_key",
                "solution": "Update your .env file with a valid EXCHANGE_RATE_API_KEY from https://www.exchangerate-api.com/",
                "timestamp": datetime.now().isoformat()
            }
        
        # Get or initialize rate limiter and cache
        rate_limiter = getattr(tool_context, '_rate_limiter', None) if tool_context else None
        if rate_limiter is None:
            rate_limiter = RateLimiter()
            if tool_context and hasattr(tool_context, "set_agent_specific_state"):
                setattr(tool_context, '_rate_limiter', rate_limiter)
            
        cache_manager = getattr(tool_context, '_cache_manager', None) if tool_context else None
        if cache_manager is None:
            cache_manager = CacheManager(default_ttl=cache_duration)
            if tool_context and hasattr(tool_context, "set_agent_specific_state"):
                setattr(tool_context, '_cache_manager', cache_manager)
        
        # Check rate limits
        if not rate_limiter.can_make_request():
            return {
                "status": "error",
                "error": "Monthly API quota exceeded. Please upgrade your plan or wait until next month.",
                "error_type": "quota_exceeded",
                "timestamp": datetime.now().isoformat()
            }
        
        # Check cache first
        cache_key = cache_manager.generate_cache_key(from_currency.upper(), to_currency.upper(), amount)
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            log.info(f"{log_identifier} Returning cached conversion for {amount} {from_currency} to {to_currency}")
            return {
                "status": "success",
                "data": cached_data,
                "cached": True,
                "timestamp": datetime.now().isoformat(),
                "source": "exchangerate-api"
            }
        
        # Make API request
        async with ExchangeRateService(api_key, base_url, timeout) as service:
            result = await service.convert_currency(from_currency.upper(), to_currency.upper(), amount)
            
            if result["status"] == "success":
                # Record the request
                rate_limiter.record_request()
                
                # Update agent state
                agent_state['request_count'] = agent_state.get('request_count', 0) + 1
                if tool_context and hasattr(tool_context, "set_agent_specific_state"):
                    tool_context.set_agent_specific_state("agent_state", agent_state)
                
                # Cache the result
                cache_manager.set(cache_key, result["data"])
                
                # Add quota warning if needed
                quota_warning = rate_limiter.get_quota_warning()
                if quota_warning:
                    result["quota_warning"] = quota_warning
                
                log.info(f"{log_identifier} Successfully converted {amount} {from_currency} to {to_currency}")
                return result
            else:
                log.error(f"{log_identifier} Failed to convert {amount} {from_currency} to {to_currency}: {result.get('error')}")
                return result
                
    except Exception as e:
        log.error(f"{log_identifier} Unexpected error in convert_currency: {str(e)}")
        
        # Provide more specific error messages for common issues
        error_message = str(e)
        if "401" in error_message or "unauthorized" in error_message.lower():
            return {
                "status": "error",
                "error": "API key is invalid or expired. Please check your EXCHANGE_RATE_API_KEY configuration.",
                "error_type": "authentication_error",
                "solution": "Verify your API key at https://www.exchangerate-api.com/ and update your .env file",
                "timestamp": datetime.now().isoformat()
            }
        elif "429" in error_message or "rate limit" in error_message.lower():
            return {
                "status": "error",
                "error": "API rate limit exceeded. Please wait before making another request.",
                "error_type": "rate_limit_error",
                "solution": "Wait a few minutes before trying again, or upgrade your API plan",
                "timestamp": datetime.now().isoformat()
            }
        elif "connection" in error_message.lower() or "timeout" in error_message.lower():
            return {
                "status": "error",
                "error": "Network connection error. Please check your internet connection.",
                "error_type": "network_error",
                "solution": "Check your internet connection and try again",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "error",
                "error": f"Unexpected error: {error_message}",
                "error_type": "unknown_error",
                "timestamp": datetime.now().isoformat()
            }


async def get_supported_currencies(
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get list of all supported currency codes and their names
    
    Args:
        tool_context: Tool context object
        tool_config: Tool configuration
        
    Returns:
        Dict with list of supported currency codes and descriptions
    """
    log_identifier = f"[ExchangeRateAgent:get_supported_currencies]"
    log.info(f"{log_identifier} Getting list of supported currencies")
    
    try:
        currencies = CurrencyValidator.get_supported_currencies()
        
        # Format the response
        currency_list = []
        for code, name in currencies.items():
            currency_list.append({
                "code": code,
                "name": name
            })
        
        # Sort by currency code
        currency_list.sort(key=lambda x: x["code"])
        
        log.info(f"{log_identifier} Retrieved {len(currency_list)} supported currencies")
        
        return {
            "status": "success",
            "data": {
                "currencies": currency_list,
                "total_count": len(currency_list),
                "source": "Exchange Rate API"
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        log.error(f"{log_identifier} Unexpected error in get_supported_currencies: {str(e)}")
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


async def get_currency_info(
    currency_code: str,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific currency
    
    Args:
        currency_code: ISO 4217 currency code
        tool_context: Tool context object
        tool_config: Tool configuration
        
    Returns:
        Dict with currency details including name, symbol, and usage information
    """
    log_identifier = f"[ExchangeRateAgent:get_currency_info]"
    log.info(f"{log_identifier} Getting information for currency: {currency_code}")
    
    try:
        # Validate currency code
        is_valid, error_msg = CurrencyValidator.validate_currency_code(currency_code)
        if not is_valid:
            return {
                "status": "error",
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
        
        # Get currency name
        currency_name = CurrencyValidator.get_currency_name(currency_code.upper())
        
        # Get current exchange rate to USD for reference
        agent_state = _get_agent_state(tool_context, log_identifier)
        if agent_state and currency_code.upper() != 'USD':
            try:
                # Get exchange rate to USD
                rates_result = await get_exchange_rates('USD', tool_context, tool_config)
                if rates_result["status"] == "success":
                    usd_rate = rates_result["data"]["conversion_rates"].get(currency_code.upper())
                else:
                    usd_rate = None
            except:
                usd_rate = None
        else:
            usd_rate = 1.0 if currency_code.upper() == 'USD' else None
        
        # Build currency information
        currency_info = {
            "code": currency_code.upper(),
            "name": currency_name,
            "description": f"{currency_name} ({currency_code.upper()})",
            "usd_rate": usd_rate,
            "supported": True,
            "source": "Exchange Rate API"
        }
        
        # Add additional information for major currencies
        major_currency_info = {
            'USD': {
                'description': 'US Dollar - Official currency of the United States',
                'symbol': '$',
                'decimal_places': 2
            },
            'EUR': {
                'description': 'Euro - Official currency of the Eurozone (19 EU countries)',
                'symbol': '€',
                'decimal_places': 2
            },
            'GBP': {
                'description': 'British Pound - Official currency of the United Kingdom',
                'symbol': '£',
                'decimal_places': 2
            },
            'JPY': {
                'description': 'Japanese Yen - Official currency of Japan',
                'symbol': '¥',
                'decimal_places': 0
            },
            'CAD': {
                'description': 'Canadian Dollar - Official currency of Canada',
                'symbol': 'C$',
                'decimal_places': 2
            },
            'AUD': {
                'description': 'Australian Dollar - Official currency of Australia',
                'symbol': 'A$',
                'decimal_places': 2
            },
            'CHF': {
                'description': 'Swiss Franc - Official currency of Switzerland',
                'symbol': 'CHF',
                'decimal_places': 2
            },
            'CNY': {
                'description': 'Chinese Yuan - Official currency of China',
                'symbol': '¥',
                'decimal_places': 2
            }
        }
        
        if currency_code.upper() in major_currency_info:
            currency_info.update(major_currency_info[currency_code.upper()])
        
        log.info(f"{log_identifier} Retrieved information for {currency_code}")
        
        return {
            "status": "success",
            "data": currency_info,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        log.error(f"{log_identifier} Unexpected error in get_currency_info: {str(e)}")
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


async def get_agent_stats(
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get agent statistics and usage information
    
    Args:
        tool_context: Tool context object
        tool_config: Tool configuration
        
    Returns:
        Dict with agent statistics
    """
    log_identifier = f"[ExchangeRateAgent:get_agent_stats]"
    log.info(f"{log_identifier} Getting agent statistics")
    
    try:
        agent_state = _get_agent_state(tool_context, log_identifier)
        rate_limiter = getattr(tool_context, '_rate_limiter', None) if tool_context else None
        cache_manager = getattr(tool_context, '_cache_manager', None) if tool_context else None
        
        stats = {
            "agent_info": {
                "name": "Exchange Rate Lookup Agent",
                "version": "1.0.0",
                "initialized_at": agent_state.get('initialized_at'),
                "total_requests": agent_state.get('request_count', 0)
            },
            "api_info": {
                "base_url": agent_state.get('base_url'),
                "timeout": agent_state.get('timeout'),
                "cache_duration": agent_state.get('cache_duration')
            }
        }
        
        # Add rate limiting stats
        if rate_limiter:
            stats["rate_limiting"] = rate_limiter.get_usage_stats()
        
        # Add cache stats
        if cache_manager:
            stats["caching"] = cache_manager.get_stats()
        
        log.info(f"{log_identifier} Retrieved agent statistics")
        
        return {
            "status": "success",
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        log.error(f"{log_identifier} Unexpected error in get_agent_stats: {str(e)}")
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
