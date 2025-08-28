# **SAM Agent Builder Prompt - Exchange Rate Lookup Agent**

Use this template to create comprehensive requirements for building a new SAM-based agent for real-time currency exchange rate lookup using the Exchange Rate API.

---

## **🔴 REQUIRED SECTIONS (Must Complete)**

### **Agent Identity**
```
Agent Name: exchange_rate_lookup_agent
Display Name: Exchange Rate Lookup Agent
Description: Provides real-time currency exchange rates and conversion data using the Exchange Rate API
Version: 1.0.0
```

### **Core Functionality**
```
Primary Function: Get real-time exchange rates for any supported currency pair
Secondary Functions: 
- Convert amounts between different currencies
- Get historical exchange rate data
- List all supported currency codes
- Get enriched currency data with additional information
Data Source: https://v6.exchangerate-api.com/v6/ (requires API key)
Authentication: API key required (stored in environment variable)
```

### **Tool Functions**
```
Function 1: get_exchange_rates
- Purpose: Get current exchange rates from a base currency to all supported currencies
- Parameters: base_currency (str, required) - ISO 4217 currency code (e.g., "USD", "EUR", "GBP")
- Returns: JSON with exchange rates for all supported currencies from the base currency
- Example: get_exchange_rates("USD") returns rates from USD to all other currencies

Function 2: convert_currency
- Purpose: Convert a specific amount from one currency to another
- Parameters: 
  - from_currency (str, required) - Source currency code
  - to_currency (str, required) - Target currency code  
  - amount (float, required) - Amount to convert
- Returns: JSON with conversion result including original amount, converted amount, and exchange rate
- Example: convert_currency("USD", "EUR", 100) returns 100 USD = X EUR

Function 3: get_supported_currencies
- Purpose: Get list of all supported currency codes and their names
- Parameters: None
- Returns: JSON array of supported currency codes with descriptions
- Example: get_supported_currencies() returns list of all available currencies

Function 4: get_currency_info
- Purpose: Get detailed information about a specific currency
- Parameters: currency_code (str, required) - ISO 4217 currency code
- Returns: JSON with currency details including name, symbol, and usage information
- Example: get_currency_info("USD") returns detailed USD information
```

### **Input/Output Format**
```
Input Parameters: 
- base_currency (string) - ISO 4217 currency code
- from_currency (string) - Source currency code
- to_currency (string) - Target currency code
- amount (float) - Amount to convert
- currency_code (string) - Currency code for information lookup

Output Format: {
  "status": "success|error",
  "data": {
    "base_code": "string",
    "conversion_rates": {
      "USD": 1.0,
      "EUR": 0.9013,
      "GBP": 0.7679,
      // ... all supported currencies
    },
    "time_last_update_utc": "string",
    "time_next_update_utc": "string"
  },
  "timestamp": "ISO format",
  "source": "exchangerate-api"
}

Error Responses: {
  "status": "error",
  "error": "error message",
  "error_type": "error_type_code",
  "timestamp": "ISO format"
}
```

### **Natural Language Examples**
```
Example Queries:
- "What's the current exchange rate for USD to EUR?"
- "Convert 100 US dollars to euros"
- "Show me all supported currencies"
- "What's the exchange rate from GBP to JPY?"
- "Get information about the Euro currency"
- "Convert 50 euros to US dollars"

Example Responses:
- "Current USD to EUR exchange rate is 0.9013 (1 USD = 0.9013 EUR)"
- "100 USD = 90.13 EUR at current exchange rate"
- "Supported currencies include: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, and 150+ more"
- "Current GBP to JPY exchange rate is 185.47 (1 GBP = 185.47 JPY)"
- "EUR (Euro) is the official currency of the Eurozone, used by 19 EU countries"
- "50 EUR = 55.47 USD at current exchange rate"
```

### **Testing Requirements**
```
API Tests: 
- Test Exchange Rate API endpoints directly with valid API key
- Test authentication with invalid/missing API key
- Validate response formats and data structures
- Test rate limits and quota management
- Test error handling for unsupported currency codes
- Test malformed request handling

Tools Tests:
- Test agent functions with mocked API responses
- Test error handling and edge cases
- Test data formatting and validation
- Test currency code validation
- Test amount conversion calculations
- Test statistics tracking and state management

Test Data:
- Success cases: Valid currency codes, standard amounts, popular currency pairs
- Error cases: Invalid currency codes, missing API key, rate limit exceeded
- Edge cases: Zero amounts, very large amounts, special characters in currency codes

Test Structure: Use sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
Mock Strategy: Mock google.adk.tools and solace_ai_connector.common.log before imports
```

### **Documentation Requirements**
```
README Content:
- Quick start guide and installation
- API key setup instructions
- Example queries and responses
- Available tools table
- Test status and data sources
- Use cases and project structure
- Rate limits and usage guidelines

API Reference Content:
- Detailed function descriptions
- Parameter specifications and currency code format
- Return value formats with examples
- Error handling documentation
- Natural language query examples
- API key configuration guide
- Rate limiting information
```

### **Dependencies & Requirements**
```
Python Packages: 
- httpx>=0.24.0 (async HTTP client for API calls)
- python-dateutil>=2.8.0 (date parsing utilities)
- pytest>=7.0.0 (testing framework)
- pytest-asyncio>=0.21.0 (async testing support)
- typing-extensions>=4.0.0 (type hints support)

Agent-Specific Requirements: Create src/exchange_rate_lookup_agent/requirements.txt
Installation Instructions: pip install -r src/exchange_rate_lookup_agent/requirements.txt
Common Dependencies: Inherit google.adk.tools, solace_ai_connector, solace-agent-mesh from parent
```

---

## **🟡 OPTIONAL SECTIONS (Complete as Needed)**

### **Advanced Features**
```
Rate Limiting: Free plan allows 1,500 requests per month, paid plans have higher limits
Caching: Cache exchange rates for 1 hour to reduce API calls and respect rate limits
Fallback APIs: Consider backup exchange rate sources for redundancy
Data Validation: Validate currency codes against ISO 4217 standard
Statistics Tracking: Track popular currency pairs, conversion amounts, and usage patterns
```

### **Lifecycle Management**
```
Initialization: 
- Validate API key presence in environment variables
- Test API connectivity with a simple request
- Initialize rate limiting counters
- Set up caching for exchange rates

Cleanup: 
- Close HTTP sessions and connections
- Save usage statistics
- Clear cached data

State Management: 
- Track API usage and rate limits
- Cache exchange rates with timestamps
- Store popular currency pairs for quick access

Statistics: 
- Track most requested currency pairs
- Monitor API usage and rate limit status
- Log conversion amounts and frequency
```

### **Service Layer Design**
```
Service Classes: 
- ExchangeRateService: Async HTTP client for API communication
- CurrencyValidator: Validate currency codes and amounts
- RateLimiter: Track and manage API rate limits
- CacheManager: Cache exchange rates with expiration

Error Handling: 
- Centralized error handling for API responses
- Graceful degradation when API is unavailable
- Clear error messages for authentication issues
- Rate limit exceeded handling

Connection Management: 
- HTTP session reuse for efficiency
- Connection pooling for multiple requests
- Timeout handling for slow responses
- Retry logic for transient failures

Response Processing: 
- JSON response parsing and validation
- Currency code normalization
- Amount formatting and precision handling
- Timestamp conversion and formatting
```

### **Configuration Options**
```
Agent Card: 
- Skills: Currency conversion, exchange rate lookup, financial data
- Discovery: Enable discovery by other financial agents
- Communication: Support inter-agent currency queries

Discovery Settings: 
- Publish currency conversion capabilities
- Enable discovery by financial analysis agents
- Support batch currency conversion requests

Communication: 
- Accept currency conversion requests from other agents
- Provide exchange rate data to financial analysis agents
- Support real-time rate updates

YAML Configuration: 
- API base URL configuration
- Rate limiting settings
- Cache duration settings
- Supported currency codes list
```

### **Security & Privacy**
```
Data Privacy: 
- Never log API keys or sensitive financial data
- Sanitize user inputs before API calls
- Handle currency amounts securely

API Key Management: 
- Store API key in EXCHANGE_RATE_API_KEY environment variable
- Validate API key format and presence at startup
- Handle API key rotation and updates
- Provide clear error messages for missing/invalid keys

Logging: 
- Log API usage statistics without sensitive data
- Track rate limit status and quota usage
- Monitor API response times and errors
- Exclude currency amounts and API keys from logs
```

### **Deployment Considerations**
```
File Structure: 
- Standard agent structure with service layer
- Environment variable configuration
- API key validation at startup

Configuration Files: 
- YAML configuration with API settings
- Environment variable template (.env.sample)
- Rate limiting configuration

Dependencies: 
- HTTP client for API communication
- Date/time utilities for timestamp handling
- Testing framework with async support
```

---

## **🔧 ENVIRONMENT VARIABLE SETUP**

### **Required Environment Variables**
```bash
# .env.sample file structure
EXCHANGE_RATE_API_KEY=your_api_key_here
EXCHANGE_RATE_API_BASE_URL=https://v6.exchangerate-api.com/v6
EXCHANGE_RATE_CACHE_DURATION=3600  # 1 hour in seconds
EXCHANGE_RATE_TIMEOUT=30           # API timeout in seconds
```

### **API Key Setup Instructions**
1. **Get API Key**: Sign up at https://www.exchangerate-api.com/
2. **Free Plan**: 1,500 requests per month
3. **Paid Plans**: Higher limits and additional features
4. **Environment Setup**: Set EXCHANGE_RATE_API_KEY in your environment

### **Security Best Practices**
- **Never commit API keys** to version control
- **Use environment variables** for all sensitive data
- **Validate API key** at agent startup
- **Handle authentication errors** gracefully
- **Monitor rate limits** and quota usage

---

## **📊 API SPECIFICATIONS**

### **Base URL and Endpoints**
```
Base URL: https://v6.exchangerate-api.com/v6/{API_KEY}/
Endpoints:
- /latest/{BASE_CURRENCY} - Get current exchange rates
- /pair/{FROM}/{TO}/{AMOUNT} - Convert specific amount
- /quota - Check API usage and limits
```

### **Supported Currency Codes**
Major currencies supported: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, and 150+ more
Full list available at: https://www.exchangerate-api.com/docs/supported-currencies

### **Rate Limits**
- **Free Plan**: 1,500 requests per month
- **Paid Plans**: Higher limits available
- **Rate Limiting**: Respect API quotas and implement caching

### **Error Types**
- `unsupported-code` - Invalid currency code
- `malformed-request` - Incorrect request format
- `invalid-key` - Invalid API key
- `inactive-account` - Unconfirmed email
- `quota-reached` - Rate limit exceeded

---

## **🧪 TESTING STRATEGY**

### **API Tests (test_exchange_rate_lookup_api.py)**
```python
# Test real API endpoints with valid API key
- Test /latest/{currency} endpoint
- Test /pair/{from}/{to}/{amount} endpoint
- Test authentication with valid/invalid keys
- Test rate limiting and quota management
- Test error responses for invalid inputs
```

### **Tools Tests (test_exchange_rate_lookup_agent.py)**
```python
# Test agent functions with mocked dependencies
- Mock Exchange Rate API responses
- Test currency code validation
- Test amount conversion calculations
- Test error handling scenarios
- Test caching and rate limiting logic
```

### **Test Data Examples**
```python
# Success cases
- Valid currency codes: "USD", "EUR", "GBP", "JPY"
- Standard amounts: 100, 1000, 1.50
- Popular pairs: USD/EUR, EUR/GBP, USD/JPY

# Error cases
- Invalid currency codes: "XXX", "INVALID"
- Missing API key: None or empty string
- Rate limit exceeded: 401/429 responses
```

---

## **📋 IMPLEMENTATION CHECKLIST**

### **Development Checklist:**
- [ ] API key setup and validation
- [ ] Currency code validation (ISO 4217)
- [ ] Rate limiting and caching implementation
- [ ] Error handling for all API error types
- [ ] Amount formatting and precision handling
- [ ] Timestamp conversion and formatting
- [ ] Comprehensive logging without sensitive data

### **Testing Checklist:**
- [ ] API tests with real API key
- [ ] Tools tests with mocked dependencies
- [ ] Authentication error handling
- [ ] Rate limit exceeded handling
- [ ] Invalid currency code handling
- [ ] Amount conversion accuracy
- [ ] Cache functionality testing

### **Documentation Checklist:**
- [ ] README.md with setup instructions
- [ ] API_REFERENCE.md with detailed documentation
- [ ] Environment variable setup guide
- [ ] API key acquisition instructions
- [ ] Rate limiting and usage guidelines
- [ ] Error handling documentation

### **Deployment Checklist:**
- [ ] Environment variables configured
- [ ] API key validated at startup
- [ ] Rate limiting configured
- [ ] Caching implemented
- [ ] Error handling tested
- [ ] Documentation complete
- [ ] Ready for deployment using deploy_agent.py

---

## **🚀 USAGE EXAMPLES**

### **Basic Usage**
```bash
# Set environment variable
export EXCHANGE_RATE_API_KEY=your_api_key_here

# Deploy agent
python deploy_agent.py /path/to/sam exchange-rate-lookup

# Run agent
./start_agent.sh
```

### **Natural Language Queries**
- "What's the current USD to EUR exchange rate?"
- "Convert 500 US dollars to British pounds"
- "Show me all supported currencies"
- "Get the exchange rate from Japanese yen to Canadian dollar"
- "What's 1000 euros worth in US dollars?"

### **Expected Responses**
- "Current USD to EUR exchange rate is 0.9013"
- "500 USD = 383.95 GBP at current exchange rate"
- "Supported currencies include USD, EUR, GBP, JPY, CAD, AUD, and 150+ more"
- "Current JPY to CAD exchange rate is 0.0091"
- "1000 EUR = 1109.40 USD at current exchange rate"

---

This agent will provide comprehensive currency exchange rate functionality while demonstrating proper API key management and security best practices in the SAM ecosystem.
