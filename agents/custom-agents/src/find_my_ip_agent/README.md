# 🌐 Find My IP Agent

A comprehensive agent for IP address detection, geolocation, and network information analysis. Provides detailed IP information including location, ISP, security analysis, and network details.

## 🚀 Quick Start

### What it does
- Get your current IP address
- Find IP geolocation and network details
- Analyze IP security information
- Get comprehensive IP intelligence
- Retry mechanism for reliability

### Example Queries
```
"What's my current IP address?"
"Where is IP address 8.8.8.8 located?"
"Get detailed information about IP 1.1.1.1"
"Show me network information for 208.67.222.222"
"Get IP security analysis for 192.168.1.1"
```

## 📋 Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `get_current_ip` | Get current IP address | "What's my IP?" |
| `get_ip_location` | Get IP geolocation | "Where is 8.8.8.8?" |
| `get_ip_info` | Get basic IP information | "Info about 1.1.1.1" |
| `get_ip_comprehensive_info` | Get detailed IP analysis | "Detailed info for 208.67.222.222" |
| `get_ip_with_retry` | Get IP with retry mechanism | "Get my IP reliably" |

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- SAM framework
- Required dependencies: `httpx`

### Configuration
The agent is configured via `configs/agents/find_my_ip_agent.yaml` and uses:
- **Primary API**: [IPify API](https://api.ipify.org/)
- **Secondary API**: [IP-API.com](http://ip-api.com/)

## 🧪 Testing

### Run Tests
```bash
# API Tests (external APIs)
python tests/test_find_my_ip_api.py

# Tools Tests (agent logic)
python tests/test_find_my_ip_agent.py
```

### Test Status
- ✅ **API Tests**: IPify and IP-API.com working
- ⚠️ **Tools Tests**: Import issues (0/11 tests passing)
- ⚠️ **Needs Fix**: Import problems to resolve

## 📊 Data Sources

### IPify API
- **URL**: https://api.ipify.org/
- **Purpose**: Current IP address detection
- **Rate Limit**: No authentication required
- **Format**: JSON response

### IP-API.com
- **URL**: http://ip-api.com/
- **Purpose**: IP geolocation and details
- **Rate Limit**: 45 requests per minute (free tier)
- **Format**: JSON, XML, CSV

## 🎯 Use Cases

### Network Administration
- IP address management
- Network monitoring
- Security analysis
- Geolocation tracking

### Development & Testing
- IP validation
- Location-based services
- Network debugging
- API testing

### Security Analysis
- IP reputation checking
- Proxy/VPN detection
- Security threat analysis
- Network forensics

### Business Intelligence
- User location analysis
- Geographic targeting
- Network analytics
- Security monitoring

## 📁 Project Structure

```
find_my_ip_agent/
├── __init__.py                 # Module initialization
├── tools.py                    # Core tool functions
├── lifecycle.py                # Agent lifecycle management
├── tests/                      # Test files
│   ├── test_find_my_ip_agent.py        # Tools tests
│   └── test_find_my_ip_api.py          # API tests
├── API_REFERENCE.md            # Detailed API documentation
└── README.md                   # This file
```

## 🌍 IP Information Available

### Basic Information
- **IP Address**: Current or specified IP
- **Location**: Country, region, city
- **Coordinates**: Latitude and longitude
- **Timezone**: Local timezone

### Network Details
- **ISP**: Internet Service Provider
- **Organization**: Network organization
- **ASN**: Autonomous System Number
- **Connection Type**: Connection details

### Security Analysis
- **Proxy Detection**: Proxy/VPN identification
- **Security Status**: Security analysis
- **Risk Assessment**: Security risk level
- **Threat Intelligence**: Security threats

## 🔒 Security & Privacy

- **No Authentication Required**: Uses public APIs
- **IP Privacy**: Only processes IP addresses (no personal data)
- **Rate Limiting**: Respects API rate limits
- **Data Privacy**: No user data stored

## 🚨 Error Handling

The agent provides comprehensive error handling:
- Network connectivity issues
- Invalid IP addresses
- API rate limiting
- Service unavailability
- Data parsing errors

## 📈 Performance

- **Retry Mechanism**: Automatic retry for failed requests
- **Caching**: In-memory caching for repeated requests
- **Async Operations**: Non-blocking API calls
- **Statistics Tracking**: Built-in usage metrics

## 🛠️ Development

### Adding New Features
1. Add tool function to `tools.py`
2. Update configuration in YAML file
3. Add tests to test suite
4. Update documentation

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_find_my_ip_agent.py

# Run API tests
python tests/test_find_my_ip_api.py
```

### Known Issues
- **Import Issues**: Tools tests have module path problems
- **Fix Needed**: Update import paths in test files

## 📞 Support

- **Documentation**: See `API_REFERENCE.md` for detailed API docs
- **Tests**: Check test files for usage examples
- **Issues**: Review error handling in tools.py
- **SAM Framework**: Consult SAM documentation for deployment

## 📄 License

Follows the same license as the parent SAM project.

---

**Discover the world behind IP addresses! 🌐✨**
