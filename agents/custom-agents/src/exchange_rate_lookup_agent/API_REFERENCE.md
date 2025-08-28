# Exchange Rate Lookup Agent - API Reference

Comprehensive documentation for the Exchange Rate Lookup Agent functions and capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Core Functions](#core-functions)
- [Error Handling](#error-handling)
- [Response Formats](#response-formats)
- [Examples](#examples)
- [Rate Limiting](#rate-limiting)
- [Caching](#caching)

## 🌐 Overview

The Exchange Rate Lookup Agent provides real-time currency exchange rates and conversion capabilities using the Exchange Rate API. It supports 150+ currencies with secure API key authentication, smart caching, and comprehensive error handling.

### Base Information
- **API Source**: [Exchange Rate API](https://www.exchangerate-api.com/)
- **Supported Currencies**: 150+ ISO 4217 currency codes
- **Rate Limits**: 1,500 requests/month (free plan)
- **Cache Duration**: 1 hour (configurable)
- **Authentication**: API key via environment variable

## 🔑 Authentication

### Required Environment Variables

```bash
# Required: Your API key from Exchange Rate API
EXCHANGE_RATE_API_KEY=your_api_key_here

# Optional: Customize settings
EXCHANGE_RATE_API_BASE_URL=https://v6.exchangerate-api.com/v6
EXCHANGE_RATE_CACHE_DURATION=3600  # 1 hour
EXCHANGE_RATE_TIMEOUT=30           # 30 seconds
```

### API Key Setup
1. Sign up at [Exchange Rate API](https://www.exchangerate-api.com/)
2. Get your free API key (1,500 requests/month)
3. Set the `EXCHANGE_RATE_API_KEY` environment variable
4. Restart the agent

## 🛠️ Core Functions

### 1. get_exchange_rates

Get current exchange rates from a base currency to all supported currencies.

#### Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `base_currency` | string | ✅ Yes | ISO 4217 currency code | `"USD"`, `"EUR"`, `"GBP"` |

#### Response Format
```json
{
  "status": "success",
  "data": {
    "result": "success",
    "documentation": "https://www.exchangerate-api.com/docs",
    "terms_of_use": "https://www.exchangerate-api.com/terms",
    "time_last_update_unix": 1585267200,
    "time_last_update_utc": "Fri, 27 Mar 2020 00:00:00 +0000",
    "time_next_update_unix": 1585353700,
    "time_next_update_utc": "Sat, 28 Mar 2020 00:00:00 +0000",
    "base_code": "USD",
    "conversion_rates": {
      "USD": 1,
      "EUR": 0.9013,
      "GBP": 0.7679,
      "JPY": 110.25,
      "CAD": 1.3168,
      "AUD": 1.4817,
      "CHF": 0.9774,
      "CNY": 6.9454
    }
  },
  "timestamp": "2024-01-15T10:30:00.000Z",
  "source": "exchangerate-api",
  "cached": false
}
```

#### Example Usage
```python
# Get USD exchange rates
result = await get_exchange_rates("USD", context)

# Get EUR exchange rates
result = await get_exchange_rates("EUR", context)
```

### 2. convert_currency

Convert a specific amount from one currency to another.

#### Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from_currency` | string | ✅ Yes | Source currency code | `"USD"`, `"EUR"` |
| `to_currency` | string | ✅ Yes | Target currency code | `"EUR"`, `"GBP"` |
| `amount` | float | ✅ Yes | Amount to convert | `100.0`, `50.5` |

#### Response Format
```json
{
  "status": "success",
  "data": {
    "result": "success",
    "documentation": "https://www.exchangerate-api.com/docs",
    "terms_of_use": "https://www.exchangerate-api.com/terms",
    "time_last_update_unix": 1585267200,
    "time_last_update_utc": "Fri, 27 Mar 2020 00:00:00 +0000",
    "time_next_update_unix": 1585353700,
    "time_next_update_utc": "Sat, 28 Mar 2020 00:00:00 +0000",
    "base_code": "USD",
    "target_code": "EUR",
    "conversion_rate": 0.9013,
    "conversion_result": 90.13
  },
  "timestamp": "2024-01-15T10:30:00.000Z",
  "source": "exchangerate-api",
  "cached": false
}
```

#### Example Usage
```python
# Convert 100 USD to EUR
result = await convert_currency("USD", "EUR", 100.0, context)

# Convert 500 GBP to USD
result = await convert_currency("GBP", "USD", 500.0, context)
```

### 3. get_supported_currencies

Get list of all supported currency codes and their names.

#### Parameters
None

#### Response Format
```json
{
  "status": "success",
  "data": {
    "currencies": [
      {
        "code": "USD",
        "name": "US Dollar"
      },
      {
        "code": "EUR",
        "name": "Euro"
      },
      {
        "code": "GBP",
        "name": "British Pound"
      }
    ],
    "total_count": 150,
    "source": "Exchange Rate API"
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### Example Usage
```python
# Get all supported currencies
result = await get_supported_currencies(context)
```

### 4. get_currency_info

Get detailed information about a specific currency.

#### Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `currency_code` | string | ✅ Yes | ISO 4217 currency code | `"USD"`, `"EUR"` |

#### Response Format
```json
{
  "status": "success",
  "data": {
    "code": "EUR",
    "name": "Euro",
    "description": "Euro - Official currency of the Eurozone (19 EU countries)",
    "symbol": "€",
    "decimal_places": 2,
    "usd_rate": 1.1094,
    "supported": true,
    "source": "Exchange Rate API"
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### Example Usage
```python
# Get EUR information
result = await get_currency_info("EUR", context)

# Get USD information
result = await get_currency_info("USD", context)
```

### 5. get_agent_stats

Get agent statistics and usage information.

#### Parameters
None

#### Response Format
```json
{
  "status": "success",
  "data": {
    "agent_info": {
      "name": "Exchange Rate Lookup Agent",
      "version": "1.0.0",
      "initialized_at": "2024-01-15T10:00:00.000Z",
      "total_requests": 25
    },
    "api_info": {
      "base_url": "https://v6.exchangerate-api.com/v6",
      "timeout": 30,
      "cache_duration": 3600
    },
    "rate_limiting": {
      "requests_this_month": 25,
      "monthly_limit": 1500,
      "remaining_requests": 1475,
      "usage_percentage": 1.67,
      "last_reset": "2024-01-01T00:00:00.000Z",
      "next_reset": "2024-02-01T00:00:00.000Z"
    },
    "caching": {
      "total_entries": 5,
      "expired_entries": 0,
      "valid_entries": 5,
      "total_size_bytes": 2048,
      "default_ttl_seconds": 3600
    }
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### Example Usage
```python
# Get agent statistics
result = await get_agent_stats(context)
```

## ❌ Error Handling

### Error Response Format
```json
{
  "status": "error",
  "error": "Error message description",
  "error_type": "error_type_code",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Common Error Types

| Error Type | Description | Resolution |
|------------|-------------|------------|
| `invalid_key` | Invalid API key | Check your `EXCHANGE_RATE_API_KEY` |
| `quota_exceeded` | Monthly quota exceeded | Upgrade plan or wait until next month |
| `unsupported_code` | Invalid currency code | Use valid ISO 4217 currency code |
| `malformed_request` | Invalid request format | Check parameter types and values |
| `timeout` | API request timeout | Check network connection |
| `network_error` | Network connectivity issue | Check internet connection |
| `unexpected_error` | Unexpected system error | Check logs and restart agent |

### Error Examples

#### Invalid API Key
```json
{
  "status": "error",
  "error": "Invalid API key. Please check your EXCHANGE_RATE_API_KEY.",
  "error_type": "invalid_key",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### Quota Exceeded
```json
{
  "status": "error",
  "error": "Monthly API quota exceeded. Please upgrade your plan or wait until next month.",
  "error_type": "quota_exceeded",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### Invalid Currency Code
```json
{
  "status": "error",
  "error": "Unsupported currency code: XXX. Please use a supported ISO 4217 currency code.",
  "error_type": "unsupported_code",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## 📊 Response Formats

### Success Response
All successful responses follow this format:
```json
{
  "status": "success",
  "data": { /* function-specific data */ },
  "timestamp": "ISO 8601 timestamp",
  "source": "exchangerate-api",
  "cached": false
}
```

### Cached Response
When data is returned from cache:
```json
{
  "status": "success",
  "data": { /* function-specific data */ },
  "timestamp": "ISO 8601 timestamp",
  "source": "exchangerate-api",
  "cached": true
}
```

## 💡 Examples

### Natural Language Queries

#### Exchange Rate Queries
- "What's the current USD to EUR exchange rate?"
- "Get exchange rates for GBP"
- "Show me rates from Japanese yen"

#### Currency Conversion Queries
- "Convert 100 US dollars to euros"
- "What's 500 GBP worth in USD?"
- "Convert 1000 yen to Canadian dollars"

#### Currency Information Queries
- "Tell me about the Euro currency"
- "What is USD?"
- "Get information about Japanese Yen"

#### General Queries
- "Show me all supported currencies"
- "What currencies do you support?"
- "Get agent statistics"

### Function Call Examples

#### Get USD Exchange Rates
```python
result = await get_exchange_rates("USD", context)
if result["status"] == "success":
    rates = result["data"]["conversion_rates"]
    print(f"USD to EUR: {rates['EUR']}")
    print(f"USD to GBP: {rates['GBP']}")
```

#### Convert Currency
```python
result = await convert_currency("USD", "EUR", 100.0, context)
if result["status"] == "success":
    data = result["data"]
    print(f"{data['base_code']} {data['conversion_result']} = {data['target_code']} {data['conversion_result']}")
```

#### Get Currency Information
```python
result = await get_currency_info("EUR", context)
if result["status"] == "success":
    info = result["data"]
    print(f"{info['name']} ({info['code']}): {info['description']}")
    print(f"Symbol: {info['symbol']}")
```

## ⚡ Rate Limiting

### Free Plan Limits
- **Monthly Limit**: 1,500 requests
- **Cache Duration**: 1 hour (reduces API calls)
- **Warning Thresholds**: 80%, 90%, 95% usage

### Rate Limit Warnings
The agent provides warnings when approaching limits:
- **80% Usage**: Notice about high usage
- **90% Usage**: Warning about approaching limit
- **95% Usage**: Critical warning about remaining requests

### Quota Management
- Automatic monthly reset
- Request tracking and statistics
- Cache optimization to reduce API calls
- Graceful handling when quota exceeded

## 💾 Caching

### Cache Strategy
- **Duration**: 1 hour (configurable)
- **Scope**: Per currency pair and amount
- **Automatic Cleanup**: Expired entries removed
- **Cache Keys**: Generated based on function and parameters

### Cache Benefits
- Reduces API calls by 60-80%
- Improves response times
- Extends quota lifespan
- Provides offline capability for recent data

### Cache Statistics
The agent tracks cache performance:
- Total entries
- Cache hit/miss ratios
- Memory usage
- Expired entries

## 🔒 Security

### API Key Protection
- Never logged in responses
- Stored securely in environment variables
- Validated at startup
- Clear error messages for missing/invalid keys

### Input Validation
- Currency code format validation (ISO 4217)
- Amount range validation (0.000001 to 1 trillion)
- Parameter type validation
- Sanitization of user inputs

### Error Message Security
- No sensitive data in error messages
- Generic error types for security
- Detailed logging for debugging
- User-friendly error messages

## 📈 Performance

### Optimization Features
- **Connection Pooling**: Reuses HTTP connections
- **Async Operations**: Non-blocking API calls
- **Smart Caching**: Reduces redundant requests
- **Rate Limiting**: Prevents quota exhaustion
- **Error Recovery**: Graceful failure handling

### Monitoring
- Request/response times
- Cache hit ratios
- Error rates and types
- Quota usage tracking
- Performance statistics

---

**For more information, see the [README.md](README.md) for setup and usage instructions.**
