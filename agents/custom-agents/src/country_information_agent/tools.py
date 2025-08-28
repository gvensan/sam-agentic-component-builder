"""
Country Information Agent Tools

This module contains the tools for the Country Information Agent following SAM patterns.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from google.adk.tools import ToolContext
from solace_ai_connector.common.log import log
try:
    from .services.country_service import get_country_service
except ImportError:
    # For testing purposes
    from services.country_service import get_country_service


def _format_country_data(country_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format country data into a consistent structure"""
    return {
        "name": country_data.get("name", {}).get("common", "Unknown"),
        "official_name": country_data.get("name", {}).get("official", "Unknown"),
        "capital": country_data.get("capital", ["Unknown"])[0] if country_data.get("capital") else "Unknown",
        "population": country_data.get("population", 0),
        "area": country_data.get("area", 0),
        "currencies": _format_currencies(country_data.get("currencies", {})),
        "languages": _format_languages(country_data.get("languages", {})),
        "borders": country_data.get("borders", []),
        "flag": {
            "png": country_data.get("flags", {}).get("png", ""),
            "svg": country_data.get("flags", {}).get("svg", "")
        },
        "coordinates": {
            "lat": country_data.get("latlng", [0, 0])[0],
            "lng": country_data.get("latlng", [0, 0])[1]
        },
        "region": country_data.get("region", "Unknown"),
        "subregion": country_data.get("subregion", "Unknown"),
        "timezones": country_data.get("timezones", []),
        "calling_codes": _format_calling_codes(country_data.get("idd", {})),
        "gdp": country_data.get("gini", {}).get("2020", 0) if country_data.get("gini") else 0
    }


def _format_currencies(currencies_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Format currencies data"""
    formatted = []
    for code, currency_info in currencies_data.items():
        formatted.append({
            "code": code,
            "name": currency_info.get("name", ""),
            "symbol": currency_info.get("symbol", "")
        })
    return formatted


def _format_languages(languages_data: Dict[str, str]) -> List[Dict[str, str]]:
    """Format languages data"""
    formatted = []
    for code, name in languages_data.items():
        formatted.append({
            "code": code,
            "name": name
        })
    return formatted


def _format_calling_codes(idd_data: Dict[str, Any]) -> str:
    """Format calling codes data"""
    if not idd_data:
        return ""
    
    root = idd_data.get("root", "")
    suffixes = idd_data.get("suffixes", [])
    
    if not suffixes:
        return root
    
    return root + suffixes[0]


def _get_similar_countries(country_name: str, all_countries: List[Dict[str, Any]]) -> List[str]:
    """Get similar country names for suggestions"""
    similar = []
    country_lower = country_name.lower()
    
    for country in all_countries:
        common_name = country.get("name", {}).get("common", "").lower()
        official_name = country.get("name", {}).get("official", "").lower()
        
        if country_lower in common_name or country_lower in official_name:
            similar.append(country.get("name", {}).get("common", ""))
        
        if len(similar) >= 5:  # Limit to 5 suggestions
            break
    
    return similar


async def get_country_info(
    country_name: str, 
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get comprehensive information about a specific country.
    
    Args:
        country_name: Country name, code, or partial match
        tool_context: Tool context (optional)
        tool_config: Tool configuration (optional)
    
    Returns:
        Dictionary with country information
    """
    log_identifier = f"[CountryInformationAgent:get_country_info]"
    log.info(f"{log_identifier} Getting country info for: {country_name}")
    
    try:
        service = await get_country_service()
        
        # Try to get country by name first
        result = await service.get_country_by_name(country_name)
        
        if result["status"] == "success":
            country_data = result["data"][0] if isinstance(result["data"], list) else result["data"]
            formatted_data = _format_country_data(country_data)
            
            # Update statistics if context is available
            if tool_context:
                try:
                    stats = tool_context.get_agent_specific_state("statistics", {})
                    stats["total_requests"] = stats.get("total_requests", 0) + 1
                    stats["successful_requests"] = stats.get("successful_requests", 0) + 1
                    tool_context.set_agent_specific_state("statistics", stats)
                except Exception as e:
                    log.warning(f"{log_identifier} Could not update statistics: {e}")
            
            return {
                "status": "success",
                "data": formatted_data,
                "timestamp": datetime.now().isoformat(),
                "source": "rest-countries-api",
                "cached": result.get("cached", False)
            }
        else:
            # Try by code if name search failed
            result = await service.get_country_by_code(country_name)
            
            if result["status"] == "success":
                country_data = result["data"][0] if isinstance(result["data"], list) else result["data"]
                formatted_data = _format_country_data(country_data)
                
                # Update statistics if context is available
                if tool_context:
                    try:
                        stats = tool_context.get_agent_specific_state("statistics", {})
                        stats["total_requests"] = stats.get("total_requests", 0) + 1
                        stats["successful_requests"] = stats.get("successful_requests", 0) + 1
                        tool_context.set_agent_specific_state("statistics", stats)
                    except Exception as e:
                        log.warning(f"{log_identifier} Could not update statistics: {e}")
                
                return {
                    "status": "success",
                    "data": formatted_data,
                    "timestamp": datetime.now().isoformat(),
                    "source": "rest-countries-api",
                    "cached": result.get("cached", False)
                }
            else:
                # Get suggestions for similar countries
                all_countries_result = await service.get_all_countries()
                suggestions = []
                if all_countries_result["status"] == "success":
                    suggestions = _get_similar_countries(country_name, all_countries_result["data"])
                
                # Update statistics if context is available
                if tool_context:
                    try:
                        stats = tool_context.get_agent_specific_state("statistics", {})
                        stats["total_requests"] = stats.get("total_requests", 0) + 1
                        stats["failed_requests"] = stats.get("failed_requests", 0) + 1
                        tool_context.set_agent_specific_state("statistics", stats)
                    except Exception as e:
                        log.warning(f"{log_identifier} Could not update statistics: {e}")
                
                return {
                    "status": "error",
                    "error": f"Country '{country_name}' not found",
                    "suggestions": suggestions,
                    "timestamp": datetime.now().isoformat()
                }
    
    except Exception as e:
        log.error(f"{log_identifier} Error getting country info: {e}")
        
        # Update statistics if context is available
        if tool_context:
            try:
                stats = tool_context.get_agent_specific_state("statistics", {})
                stats["total_requests"] = stats.get("total_requests", 0) + 1
                stats["failed_requests"] = stats.get("failed_requests", 0) + 1
                tool_context.set_agent_specific_state("statistics", stats)
            except Exception as e:
                log.warning(f"{log_identifier} Could not update statistics: {e}")
        
        return {
            "status": "error",
            "error": f"Failed to get country information: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


async def search_countries(
    search_term: str, 
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Search for countries by name or partial match.
    
    Args:
        search_term: Search term for country name
        tool_context: Tool context (optional)
        tool_config: Tool configuration (optional)
    
    Returns:
        Dictionary with matching countries
    """
    log_identifier = f"[CountryInformationAgent:search_countries]"
    log.info(f"{log_identifier} Searching countries for: {search_term}")
    
    try:
        service = await get_country_service()
        result = await service.search_countries(search_term)
        
        if result["status"] == "success":
            countries_data = result["data"]
            formatted_countries = []
            
            for country in countries_data:
                formatted_countries.append({
                    "name": country.get("name", {}).get("common", "Unknown"),
                    "official_name": country.get("name", {}).get("official", "Unknown"),
                    "capital": country.get("capital", ["Unknown"])[0] if country.get("capital") else "Unknown",
                    "population": country.get("population", 0),
                    "region": country.get("region", "Unknown"),
                    "flag": country.get("flags", {}).get("png", "")
                })
            
            # Update statistics if context is available
            if tool_context:
                try:
                    stats = tool_context.get_agent_specific_state("statistics", {})
                    stats["total_requests"] = stats.get("total_requests", 0) + 1
                    stats["successful_requests"] = stats.get("successful_requests", 0) + 1
                    tool_context.set_agent_specific_state("statistics", stats)
                except Exception as e:
                    log.warning(f"{log_identifier} Could not update statistics: {e}")
            
            return {
                "status": "success",
                "data": formatted_countries,
                "count": len(formatted_countries),
                "timestamp": datetime.now().isoformat(),
                "source": "rest-countries-api",
                "cached": result.get("cached", False)
            }
        else:
            # Update statistics if context is available
            if tool_context:
                try:
                    stats = tool_context.get_agent_specific_state("statistics", {})
                    stats["total_requests"] = stats.get("total_requests", 0) + 1
                    stats["failed_requests"] = stats.get("failed_requests", 0) + 1
                    tool_context.set_agent_specific_state("statistics", stats)
                except Exception as e:
                    log.warning(f"{log_identifier} Could not update statistics: {e}")
            
            return {
                "status": "error",
                "error": result["error"],
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        log.error(f"{log_identifier} Error searching countries: {e}")
        
        # Update statistics if context is available
        if tool_context:
            try:
                stats = tool_context.get_agent_specific_state("statistics", {})
                stats["total_requests"] = stats.get("total_requests", 0) + 1
                stats["failed_requests"] = stats.get("failed_requests", 0) + 1
                tool_context.set_agent_specific_state("statistics", stats)
            except Exception as e:
                log.warning(f"{log_identifier} Could not update statistics: {e}")
        
        return {
            "status": "error",
            "error": f"Failed to search countries: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


async def get_country_borders(
    country_name: str, 
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get border information and neighboring countries.
    
    Args:
        country_name: Country name or code
        tool_context: Tool context (optional)
        tool_config: Tool configuration (optional)
    
    Returns:
        Dictionary with border information
    """
    log_identifier = f"[CountryInformationAgent:get_country_borders]"
    log.info(f"{log_identifier} Getting borders for: {country_name}")
    
    try:
        # First get the country info
        country_result = await get_country_info(country_name, tool_context)
        
        if country_result["status"] == "success":
            country_data = country_result["data"]
            borders = country_data.get("borders", [])
            
            # Get detailed info for border countries
            border_countries = []
            for border_code in borders:
                service = await get_country_service()
                border_result = await service.get_country_by_code(border_code)
                
                if border_result["status"] == "success":
                    border_data = border_result["data"][0] if isinstance(border_result["data"], list) else border_result["data"]
                    border_countries.append({
                        "name": border_data.get("name", {}).get("common", "Unknown"),
                        "code": border_code,
                        "capital": border_data.get("capital", ["Unknown"])[0] if border_data.get("capital") else "Unknown",
                        "population": border_data.get("population", 0),
                        "flag": border_data.get("flags", {}).get("png", "")
                    })
            
            return {
                "status": "success",
                "data": {
                    "country": country_data["name"],
                    "borders": border_countries,
                    "border_count": len(borders),
                    "coordinates": country_data["coordinates"]
                },
                "timestamp": datetime.now().isoformat(),
                "source": "rest-countries-api"
            }
        else:
            return country_result
    
    except Exception as e:
        log.error(f"{log_identifier} Error getting country borders: {e}")
        return {
            "status": "error",
            "error": f"Failed to get country borders: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


async def get_country_comparison(
    country_names: List[str], 
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Compare multiple countries side by side.
    
    Args:
        country_names: List of 2-5 country names to compare
        tool_context: Tool context (optional)
        tool_config: Tool configuration (optional)
    
    Returns:
        Dictionary with comparison data
    """
    log_identifier = f"[CountryInformationAgent:get_country_comparison]"
    log.info(f"{log_identifier} Comparing countries: {country_names}")
    
    try:
        if len(country_names) < 2:
            return {
                "status": "error",
                "error": "At least 2 countries are required for comparison",
                "timestamp": datetime.now().isoformat()
            }
        
        if len(country_names) > 5:
            return {
                "status": "error",
                "error": "Maximum 5 countries can be compared at once",
                "timestamp": datetime.now().isoformat()
            }
        
        comparison_data = []
        
        for country_name in country_names:
            country_result = await get_country_info(country_name, tool_context)
            
            if country_result["status"] == "success":
                country_data = country_result["data"]
                comparison_data.append({
                    "name": country_data["name"],
                    "capital": country_data["capital"],
                    "population": country_data["population"],
                    "area": country_data["area"],
                    "region": country_data["region"],
                    "currencies": country_data["currencies"],
                    "languages": country_data["languages"],
                    "flag": country_data["flag"]["png"]
                })
            else:
                return {
                    "status": "error",
                    "error": f"Could not get information for {country_name}: {country_result['error']}",
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "status": "success",
            "data": {
                "countries": comparison_data,
                "count": len(comparison_data),
                "comparison_fields": ["name", "capital", "population", "area", "region", "currencies", "languages"]
            },
            "timestamp": datetime.now().isoformat(),
            "source": "rest-countries-api"
        }
    
    except Exception as e:
        log.error(f"{log_identifier} Error comparing countries: {e}")
        return {
            "status": "error",
            "error": f"Failed to compare countries: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


async def get_all_countries(
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get list of all countries with basic information.
    
    Args:
        tool_context: Tool context (optional)
        tool_config: Tool configuration (optional)
    
    Returns:
        Dictionary with all countries
    """
    log_identifier = f"[CountryInformationAgent:get_all_countries]"
    log.info(f"{log_identifier} Getting all countries")
    
    try:
        service = await get_country_service()
        result = await service.get_all_countries()
        
        if result["status"] == "success":
            countries_data = result["data"]
            formatted_countries = []
            
            for country in countries_data:
                formatted_countries.append({
                    "name": country.get("name", {}).get("common", "Unknown"),
                    "official_name": country.get("name", {}).get("official", "Unknown"),
                    "code": country.get("cca2", "Unknown"),
                    "capital": country.get("capital", ["Unknown"])[0] if country.get("capital") else "Unknown",
                    "population": country.get("population", 0),
                    "region": country.get("region", "Unknown"),
                    "flag": country.get("flags", {}).get("png", "")
                })
            
            # Sort by name
            formatted_countries.sort(key=lambda x: x["name"])
            
            # Update statistics if context is available
            if tool_context:
                try:
                    stats = tool_context.get_agent_specific_state("statistics", {})
                    stats["total_requests"] = stats.get("total_requests", 0) + 1
                    stats["successful_requests"] = stats.get("successful_requests", 0) + 1
                    tool_context.set_agent_specific_state("statistics", stats)
                except Exception as e:
                    log.warning(f"{log_identifier} Could not update statistics: {e}")
            
            return {
                "status": "success",
                "data": formatted_countries,
                "count": len(formatted_countries),
                "timestamp": datetime.now().isoformat(),
                "source": "rest-countries-api",
                "cached": result.get("cached", False)
            }
        else:
            # Update statistics if context is available
            if tool_context:
                try:
                    stats = tool_context.get_agent_specific_state("statistics", {})
                    stats["total_requests"] = stats.get("total_requests", 0) + 1
                    stats["failed_requests"] = stats.get("failed_requests", 0) + 1
                    tool_context.set_agent_specific_state("statistics", stats)
                except Exception as e:
                    log.warning(f"{log_identifier} Could not update statistics: {e}")
            
            return {
                "status": "error",
                "error": result["error"],
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        log.error(f"{log_identifier} Error getting all countries: {e}")
        
        # Update statistics if context is available
        if tool_context:
            try:
                stats = tool_context.get_agent_specific_state("statistics", {})
                stats["total_requests"] = stats.get("total_requests", 0) + 1
                stats["failed_requests"] = stats.get("failed_requests", 0) + 1
                tool_context.set_agent_specific_state("statistics", stats)
            except Exception as e:
                log.warning(f"{log_identifier} Could not update statistics: {e}")
        
        return {
            "status": "error",
            "error": f"Failed to get all countries: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
