"""
Rate Limiter for managing API rate limits and quotas
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for managing API usage and quotas"""
    
    def __init__(self, monthly_limit: int = None):
        """
        Initialize the rate limiter
        
        Args:
            monthly_limit: Monthly request limit (defaults to environment variable)
        """
        self.monthly_limit = monthly_limit or int(os.getenv('EXCHANGE_RATE_MONTHLY_LIMIT', '1500'))
        self.requests_this_month = 0
        self.last_reset = datetime.now()
        self.last_request_time = None
        
    def can_make_request(self) -> bool:
        """
        Check if a request can be made
        
        Returns:
            True if request can be made, False otherwise
        """
        # Check if we need to reset monthly counter
        self._check_monthly_reset()
        
        # Check if we've hit the monthly limit
        if self.requests_this_month >= self.monthly_limit:
            logger.warning(f"⚠️ Monthly rate limit reached: {self.requests_this_month}/{self.monthly_limit}")
            return False
            
        return True
        
    def record_request(self) -> None:
        """
        Record that a request was made
        """
        self.requests_this_month += 1
        self.last_request_time = datetime.now()
        
        # Log usage
        remaining = self.monthly_limit - self.requests_this_month
        logger.info(f"📊 API request recorded. Remaining: {remaining}/{self.monthly_limit}")
        
        # Warn when approaching limit
        if remaining <= 50:
            logger.warning(f"⚠️ Approaching rate limit: {remaining} requests remaining")
        elif remaining <= 10:
            logger.error(f"🚨 Critical: Only {remaining} requests remaining this month")
            
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get current usage statistics
        
        Returns:
            Dict with usage statistics
        """
        self._check_monthly_reset()
        
        return {
            "requests_this_month": self.requests_this_month,
            "monthly_limit": self.monthly_limit,
            "remaining_requests": self.monthly_limit - self.requests_this_month,
            "usage_percentage": (self.requests_this_month / self.monthly_limit) * 100,
            "last_reset": self.last_reset.isoformat(),
            "last_request_time": self.last_request_time.isoformat() if self.last_request_time else None,
            "next_reset": (self.last_reset + timedelta(days=30)).isoformat()
        }
        
    def _check_monthly_reset(self) -> None:
        """
        Check if monthly counter needs to be reset
        """
        now = datetime.now()
        
        # Reset if it's been more than 30 days since last reset
        if (now - self.last_reset).days >= 30:
            logger.info(f"🔄 Resetting monthly rate limit counter. Previous: {self.requests_this_month} requests")
            self.requests_this_month = 0
            self.last_reset = now
            
    def get_quota_warning(self) -> Optional[str]:
        """
        Get a warning message if approaching quota limit
        
        Returns:
            Warning message or None
        """
        self._check_monthly_reset()
        
        remaining = self.monthly_limit - self.requests_this_month
        usage_percentage = (self.requests_this_month / self.monthly_limit) * 100
        
        if remaining <= 10:
            return f"🚨 CRITICAL: Only {remaining} requests remaining this month ({usage_percentage:.1f}% used)"
        elif remaining <= 50:
            return f"⚠️ WARNING: {remaining} requests remaining this month ({usage_percentage:.1f}% used)"
        elif usage_percentage >= 80:
            return f"⚠️ Notice: {usage_percentage:.1f}% of monthly quota used ({remaining} requests remaining)"
            
        return None
