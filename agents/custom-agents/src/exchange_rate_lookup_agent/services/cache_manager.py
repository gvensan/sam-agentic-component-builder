"""
Cache Manager for caching exchange rates
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """Cache manager for storing exchange rates with expiration"""
    
    def __init__(self, default_ttl: int = None):  # 1 hour default
        """
        Initialize the cache manager
        
        Args:
            default_ttl: Default time-to-live in seconds (defaults to environment variable)
        """
        self.default_ttl = default_ttl or int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600'))
        self.cache = {}
        
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get a value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        if key not in self.cache:
            return None
            
        cache_entry = self.cache[key]
        expires_at = cache_entry.get('expires_at')
        
        # Check if expired
        if expires_at and datetime.now() > expires_at:
            logger.debug(f"🗑️ Cache entry expired for key: {key}")
            del self.cache[key]
            return None
            
        logger.debug(f"✅ Cache hit for key: {key}")
        return cache_entry.get('data')
        
    def set(self, key: str, data: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """
        Set a value in cache
        
        Args:
            key: Cache key
            data: Data to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        if ttl is None:
            ttl = self.default_ttl
            
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        self.cache[key] = {
            'data': data,
            'expires_at': expires_at,
            'created_at': datetime.now(),
            'ttl': ttl
        }
        
        logger.debug(f"💾 Cached data for key: {key} (TTL: {ttl}s)")
        
    def delete(self, key: str) -> bool:
        """
        Delete a value from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"🗑️ Deleted cache entry for key: {key}")
            return True
        return False
        
    def clear(self) -> int:
        """
        Clear all cache entries
        
        Returns:
            Number of entries cleared
        """
        count = len(self.cache)
        self.cache.clear()
        logger.info(f"🗑️ Cleared {count} cache entries")
        return count
        
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache
        
        Returns:
            Number of expired entries removed
        """
        now = datetime.now()
        expired_keys = []
        
        for key, entry in self.cache.items():
            expires_at = entry.get('expires_at')
            if expires_at and now > expires_at:
                expired_keys.append(key)
                
        for key in expired_keys:
            del self.cache[key]
            
        if expired_keys:
            logger.info(f"🗑️ Cleaned up {len(expired_keys)} expired cache entries")
            
        return len(expired_keys)
        
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dict with cache statistics
        """
        now = datetime.now()
        total_entries = len(self.cache)
        expired_entries = 0
        total_size = 0
        
        for entry in self.cache.values():
            expires_at = entry.get('expires_at')
            if expires_at and now > expires_at:
                expired_entries += 1
            total_size += len(str(entry.get('data', {})))
            
        return {
            "total_entries": total_entries,
            "expired_entries": expired_entries,
            "valid_entries": total_entries - expired_entries,
            "total_size_bytes": total_size,
            "default_ttl_seconds": self.default_ttl
        }
        
    def generate_cache_key(self, base_currency: str, target_currency: Optional[str] = None, amount: Optional[float] = None) -> str:
        """
        Generate a cache key for exchange rate data
        
        Args:
            base_currency: Base currency code
            target_currency: Target currency code (optional)
            amount: Amount to convert (optional)
            
        Returns:
            Cache key string
        """
        if target_currency and amount is not None:
            # Conversion cache key
            return f"convert_{base_currency.upper()}_{target_currency.upper()}_{amount}"
        else:
            # Rates cache key
            return f"rates_{base_currency.upper()}"
