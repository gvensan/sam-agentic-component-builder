# Exchange Rate Lookup Agent - Environment Variables

This document describes the environment variables used by the Exchange Rate Lookup Agent and the changes made to replace hard-coded values with configurable environment variables.

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `EXCHANGE_RATE_API_KEY` | Your Exchange Rate API key (required) | `7013c55240c86e3eaee3c548` |

### Optional Variables (with defaults)

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `EXCHANGE_RATE_API_BASE_URL` | Base URL for the Exchange Rate API | `https://v6.exchangerate-api.com/v6` | `https://v6.exchangerate-api.com/v6` |
| `EXCHANGE_RATE_API_TIMEOUT` | Request timeout in seconds | `30` | `60` |
| `EXCHANGE_RATE_CACHE_DURATION` | Cache duration in seconds | `3600` (1 hour) | `1800` |
| `EXCHANGE_RATE_MONTHLY_LIMIT` | Monthly request limit | `1500` (free tier) | `5000` |
| `EXCHANGE_RATE_LOG_LEVEL` | Log level | `INFO` | `DEBUG` |

## Files Updated

### 1. `lifecycle.py`
- **Changes**: Updated to use all environment variables from `.env.sample`
- **Environment Variables Used**:
  - `EXCHANGE_RATE_API_KEY` (required)
  - `EXCHANGE_RATE_API_BASE_URL` (optional)
  - `EXCHANGE_RATE_API_TIMEOUT` (optional)
  - `EXCHANGE_RATE_CACHE_DURATION` (optional)
  - `EXCHANGE_RATE_MONTHLY_LIMIT` (optional)
  - `EXCHANGE_RATE_LOG_LEVEL` (optional)

### 2. `services/exchange_rate_service.py`
- **Changes**: Updated constructor to use environment variables as defaults
- **Environment Variables Used**:
  - `EXCHANGE_RATE_API_BASE_URL` (default for `base_url` parameter)
  - `EXCHANGE_RATE_API_TIMEOUT` (default for `timeout` parameter)

### 3. `services/rate_limiter.py`
- **Changes**: Updated constructor to use environment variable as default
- **Environment Variables Used**:
  - `EXCHANGE_RATE_MONTHLY_LIMIT` (default for `monthly_limit` parameter)

### 4. `services/cache_manager.py`
- **Changes**: Updated constructor to use environment variable as default
- **Environment Variables Used**:
  - `EXCHANGE_RATE_CACHE_DURATION` (default for `default_ttl` parameter)

### 5. `tools.py`
- **Changes**: Already using environment variables via `agent_state` (no changes needed)
- **Environment Variables Used**: All via `agent_state` from lifecycle initialization

## Test Files Updated

### 1. `tests/test_environment_loading.py`
- **Purpose**: Tests environment variable loading functionality
- **Features**:
  - API key validation
  - Optional environment variable validation
  - Environment file location detection
  - Variable persistence testing

### 2. `tests/test_environment_integration.py`
- **Purpose**: Tests that all services use environment variables correctly
- **Features**:
  - Service constructor testing
  - Environment variable consistency verification
  - Lifecycle integration testing

### 3. `tests/test_exchange_rate_lookup_agent.py`
- **Changes**: Updated to load environment variables before running tests
- **Features**: Uses real API key from environment for testing

### 4. `tests/test_exchange_rate_lookup_api.py`
- **Changes**: Enhanced environment variable loading and validation
- **Features**: Better error messages for missing API keys

## Benefits of These Changes

1. **Configurability**: All hard-coded values are now configurable via environment variables
2. **Flexibility**: Different environments can use different settings without code changes
3. **Security**: API keys and sensitive configuration are externalized
4. **Maintainability**: Easy to update configuration without modifying code
5. **Testing**: Tests can use different configurations for different scenarios
6. **Deployment**: Easy to deploy with different settings in different environments

## Usage Examples

### Basic Usage (with defaults)
```bash
export EXCHANGE_RATE_API_KEY=your_api_key_here
python -m pytest tests/
```

### Custom Configuration
```bash
export EXCHANGE_RATE_API_KEY=your_api_key_here
export EXCHANGE_RATE_API_TIMEOUT=60
export EXCHANGE_RATE_CACHE_DURATION=1800
export EXCHANGE_RATE_MONTHLY_LIMIT=5000
export EXCHANGE_RATE_LOG_LEVEL=DEBUG
python -m pytest tests/
```

### Using .env File
```bash
# Copy the sample file
cp .env.sample .env

# Edit .env with your values
# Then run tests
python -m pytest tests/
```

## Migration Guide

If you have existing code that uses hard-coded values:

1. **Before**: `ExchangeRateService(api_key, "https://v6.exchangerate-api.com/v6", 30)`
2. **After**: `ExchangeRateService(api_key)` (uses environment variables)

1. **Before**: `RateLimiter(1500)`
2. **After**: `RateLimiter()` (uses `EXCHANGE_RATE_MONTHLY_LIMIT`)

1. **Before**: `CacheManager(3600)`
2. **After**: `CacheManager()` (uses `EXCHANGE_RATE_CACHE_DURATION`)

## Testing

Run the environment variable tests to verify everything works:

```bash
# Test environment variable loading
python tests/test_environment_loading.py -v

# Test environment variable integration
python tests/test_environment_integration.py -v

# Test API functionality with environment variables
python tests/test_exchange_rate_lookup_api.py
```

## Notes

- All environment variables have sensible defaults
- The agent will work with just the required `EXCHANGE_RATE_API_KEY`
- Environment variables are loaded from multiple locations for flexibility
- Tests automatically load environment variables from the appropriate `.env` file
- The `.env.sample` file provides documentation and examples for all variables
