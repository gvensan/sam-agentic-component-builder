# Exchange Rate Lookup Agent

A SAM-based agent that provides real-time currency exchange rates and conversion data using the Exchange Rate API.

## 🌟 Features

- **Real-time Exchange Rates**: Get current rates for 150+ currencies
- **Currency Conversion**: Convert amounts between any supported currency pair
- **Currency Information**: Get detailed information about currencies
- **Rate Limiting**: Smart caching and quota management
- **API Key Security**: Secure environment variable-based authentication
- **Comprehensive Error Handling**: Graceful handling of API errors and rate limits

## 🚀 Quick Start

### 1. Get API Key
Sign up for a free API key at [Exchange Rate API](https://www.exchangerate-api.com/):
- Free plan: 1,500 requests per month
- Paid plans: Higher limits available

### 2. Set Environment Variables
Copy the sample environment file and configure your API key:

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

**Required**: Replace `your_api_key_here` with your actual API key:
```bash
EXCHANGE_RATE_API_KEY=your_actual_api_key_here
```

**Optional**: The `.env.sample` file includes all optional configuration variables with their default values.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Deploy Agent
```bash
python deploy_agent.py /path/to/sam exchange-rate-lookup
```

### 5. Run Agent
```bash
./start_agent.sh
```

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_exchange_rates` | Get current rates from base currency to all supported currencies | `base_currency` (string) |
| `convert_currency` | Convert specific amount between currencies | `from_currency`, `to_currency`, `amount` |
| `get_supported_currencies` | Get list of all supported currency codes | None |
| `get_currency_info` | Get detailed information about a currency | `currency_code` |
| `get_agent_stats` | Get agent statistics and usage info | None |

## 💱 Example Queries

### Exchange Rate Lookup
- "What's the current USD to EUR exchange rate?"
- "Get exchange rates for GBP"
- "Show me rates from Japanese yen"

### Currency Conversion
- "Convert 100 US dollars to euros"
- "What's 500 GBP worth in USD?"
- "Convert 1000 yen to Canadian dollars"

### Currency Information
- "Tell me about the Euro currency"
- "What is USD?"
- "Get information about Japanese Yen"

### General Queries
- "Show me all supported currencies"
- "What currencies do you support?"
- "Get agent statistics"

## 📊 Supported Currencies

The agent supports 150+ currencies including:

**Major Currencies:**
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)
- CHF (Swiss Franc)
- CNY (Chinese Yuan)

**Other Popular Currencies:**
- INR (Indian Rupee)
- BRL (Brazilian Real)
- MXN (Mexican Peso)
- KRW (South Korean Won)
- SGD (Singapore Dollar)
- NZD (New Zealand Dollar)
- And 140+ more...

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EXCHANGE_RATE_API_KEY` | ✅ Yes | - | Your API key from Exchange Rate API |
| `EXCHANGE_RATE_API_BASE_URL` | ❌ No | `https://v6.exchangerate-api.com/v6` | API base URL |
| `EXCHANGE_RATE_API_TIMEOUT` | ❌ No | `30` | API timeout in seconds |
| `EXCHANGE_RATE_CACHE_DURATION` | ❌ No | `3600` | Cache duration in seconds |
| `EXCHANGE_RATE_MONTHLY_LIMIT` | ❌ No | `1500` | Monthly request limit |
| `EXCHANGE_RATE_LOG_LEVEL` | ❌ No | `INFO` | Logging level |

### Rate Limiting
- **Free Plan**: 1,500 requests per month
- **Caching**: 1-hour cache to reduce API calls
- **Smart Management**: Automatic quota tracking and warnings

## 🧪 Testing

### API Tests
Test the actual Exchange Rate API:
```bash
cd src/exchange_rate_lookup_agent
python tests/test_exchange_rate_lookup_api.py
```

### Tools Tests
Test agent functions with mocked dependencies:
```bash
cd src/exchange_rate_lookup_agent
python -m pytest tests/test_exchange_rate_lookup_agent.py -v
```

## 📁 Project Structure

```
src/exchange_rate_lookup_agent/
├── __init__.py                    # Module initialization
├── lifecycle.py                   # Agent lifecycle functions
├── tools.py                       # Core tool functions
├── requirements.txt               # Agent-specific dependencies
├── services/                      # Service layer
│   ├── __init__.py
│   ├── exchange_rate_service.py   # API communication
│   ├── currency_validator.py      # Input validation
│   ├── rate_limiter.py           # Rate limiting
│   └── cache_manager.py          # Caching
├── tests/                         # Test files
│   ├── test_exchange_rate_lookup_api.py
│   └── test_exchange_rate_lookup_agent.py
├── API_REFERENCE.md               # Detailed API documentation
└── README.md                      # This file
```

## 🔒 Security Features

- **API Key Protection**: Never logged or exposed in responses
- **Input Validation**: Comprehensive validation of currency codes and amounts
- **Error Handling**: Secure error messages without sensitive data
- **Rate Limiting**: Prevents quota exhaustion
- **Caching**: Reduces API calls and improves performance

## 📈 Performance Features

- **Smart Caching**: 1-hour cache for exchange rates
- **Connection Pooling**: Efficient HTTP session management
- **Rate Limiting**: Prevents API quota issues
- **Error Recovery**: Graceful handling of network issues
- **Statistics Tracking**: Monitor usage and performance

## 🚨 Error Handling

The agent handles various error scenarios:

- **Invalid API Key**: Clear error message with setup instructions
- **Rate Limit Exceeded**: Informative message about quota limits
- **Invalid Currency Codes**: Helpful suggestions for correct codes
- **Network Issues**: Graceful timeout and retry handling
- **API Errors**: Detailed error messages with troubleshooting tips

## 📊 Usage Statistics

The agent tracks usage statistics including:
- Total API requests made
- Cache hit/miss ratios
- Rate limit status
- Popular currency pairs
- Error rates and types

## 🔄 Updates and Maintenance

- **Real-time Data**: Always provides current exchange rates
- **Automatic Caching**: Reduces API calls and improves response times
- **Quota Monitoring**: Tracks usage and provides warnings
- **Error Recovery**: Handles temporary API issues gracefully

## 📞 Support

For issues or questions:
1. Check the [API_REFERENCE.md](API_REFERENCE.md) for detailed documentation
2. Review the test files for usage examples
3. Check environment variable configuration
4. Verify API key is valid and has sufficient quota

## 📄 License

This agent is part of the SAM (Solace Agent Mesh) ecosystem and follows the same licensing terms.

---

**Ready to convert currencies?** Set up your API key and start using the Exchange Rate Lookup Agent! 💱
