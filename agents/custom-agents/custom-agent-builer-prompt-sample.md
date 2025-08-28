# **SAM Agent Builder Prompt Template**

Use this template to capture **agent-specific details** for building a new SAM-based agent. This template focuses on the **specific requirements, APIs, and configuration** for your agent, while general development guidelines are in `instructions.mdc`.

**📋 Before using this template:**
1. Review `instructions.mdc` for complete development guidelines and best practices
2. Use this template to capture agent-specific details (APIs, keys, URLs, etc.)
3. Follow the checklist in `instructions.mdc` for implementation

---

## **🔴 AGENT-SPECIFIC REQUIREMENTS (Fill These In)**

### **Agent Identity**
```
Agent Name: [REQUIRED] The internal name for the agent (e.g., "ip_geolocation_agent", "weather_trend_agent")
Display Name: [REQUIRED] Human-readable name (e.g., "IP Geolocation Agent", "Weather Trend Agent")
Description: [REQUIRED] Brief description of what the agent does (1-2 sentences)
Version: [REQUIRED] Version number (e.g., "1.0.0")
```

### **API & Data Source Details**
```
Primary API: [REQUIRED] Exact API endpoint and URL
API Documentation: [REQUIRED] Link to API documentation
Authentication Method: [REQUIRED] API key, OAuth, none, etc.
API Key Requirements: [REQUIRED] Format, length, where to get it
Rate Limits: [REQUIRED] Requests per minute/hour/day
API Response Format: [REQUIRED] JSON, XML, etc.
Error Codes: [REQUIRED] Common error codes and meanings
```

### **Environment Variables**
```
Required Environment Variables:
- API_KEY_NAME: [REQUIRED] Your API key variable name
- API_BASE_URL: [REQUIRED] Base URL for API calls
- API_TIMEOUT: [OPTIONAL] Request timeout in seconds (default: 30)
- API_CACHE_DURATION: [OPTIONAL] Cache duration in seconds (default: 3600)

Example .env.sample content:
API_KEY_NAME=your_actual_api_key_here
API_BASE_URL=https://api.example.com/v1
API_TIMEOUT=30
API_CACHE_DURATION=3600
```

### **Tool Functions (Agent-Specific)**
```
Function 1: [REQUIRED] [FUNCTION_NAME]
- Purpose: [REQUIRED] What this function does
- Parameters: [REQUIRED] List of input parameters with types
- Returns: [REQUIRED] What the function returns
- API Endpoint: [REQUIRED] Which API endpoint this function calls
- Example Request: [REQUIRED] Sample API request
- Example Response: [REQUIRED] Sample API response

Function 2: [REQUIRED] [FUNCTION_NAME]
- Purpose: [REQUIRED] What this function does
- Parameters: [REQUIRED] List of input parameters with types
- Returns: [REQUIRED] What the function returns
- API Endpoint: [REQUIRED] Which API endpoint this function calls
- Example Request: [REQUIRED] Sample API request
- Example Response: [REQUIRED] Sample API response

[Add more functions as needed]
```

### **Natural Language Examples (Agent-Specific)**
```
Example Queries: [REQUIRED] List 3-5 example user questions specific to this agent
Example Responses: [REQUIRED] Show how this agent should respond to each query
Domain-Specific Terms: [REQUIRED] Any special terminology or concepts users might use
```

### **Testing Data (Agent-Specific)**
```
API Test Data: [REQUIRED] Sample API responses for testing
Success Cases: [REQUIRED] Valid inputs and expected outputs
Error Cases: [REQUIRED] Invalid inputs and expected error responses
Edge Cases: [REQUIRED] Boundary conditions and special scenarios
Mock Data: [REQUIRED] Sample data for mocked API responses in tools tests
```

### **Dependencies (Agent-Specific)**
```
Required Python Packages: [REQUIRED] List specific packages this agent needs
Package Versions: [REQUIRED] Minimum versions required
Special Dependencies: [OPTIONAL] Any unusual or specific dependencies
```

### **Configuration (Agent-Specific)**
```
Agent Card Skills: [REQUIRED] What skills should be listed in the agent card
Discovery Settings: [REQUIRED] How other agents can discover this agent
Communication: [REQUIRED] Any special communication requirements
YAML Configuration: [REQUIRED] Any custom YAML configuration needed
```

---

## **🟡 OPTIONAL AGENT-SPECIFIC FEATURES**

### **Advanced Features (Agent-Specific)**
```
Rate Limiting: [OPTIONAL] Specific rate limits for this API
Caching Strategy: [OPTIONAL] What data to cache and for how long
Fallback APIs: [OPTIONAL] Backup data sources if primary fails
Data Validation: [OPTIONAL] Specific validation rules for this agent's data
Statistics Tracking: [OPTIONAL] What metrics to collect for this agent
```

### **Service Layer (Agent-Specific)**
```
Custom Services: [OPTIONAL] Any special service classes needed
Error Handling: [OPTIONAL] Specific error handling for this API
Response Processing: [OPTIONAL] Special data transformation needed
Rate Limiting: [OPTIONAL] Specific rate limiting implementation
Caching: [OPTIONAL] Specific caching strategy for this agent
Validation: [OPTIONAL] Specific validation for this agent's inputs
```

### **Security & Privacy (Agent-Specific)**
```
Data Privacy: [OPTIONAL] How to handle sensitive data for this agent
API Key Management: [OPTIONAL] Specific security requirements for this API
Logging: [OPTIONAL] What to log and what to exclude for this agent
```

---

## **📋 COMPLETE EXAMPLE**

Here's a complete example using the Country Information Agent:

### **Agent Identity**
```
Agent Name: country_information_agent
Display Name: Country Information Agent
Description: Provides comprehensive country data including demographics, geography, economy, and cultural information
Version: 1.0.0
```

### **API & Data Source Details**
```
Primary API: https://restcountries.com/v3.1/
API Documentation: https://restcountries.com/
Authentication Method: None (free public API)
API Key Requirements: Not required
Rate Limits: No specific limits (generous usage)
API Response Format: JSON
Error Codes: 404 (country not found), 500 (server error)
```

### **Environment Variables**
```
Required Environment Variables:
- No API key required for this agent

Example .env.sample content:
# No API key needed for REST Countries API
# Optional: Custom timeout and cache settings
API_TIMEOUT=30
API_CACHE_DURATION=3600
```

### **Tool Functions (Agent-Specific)**
```
Function 1: get_country_info
- Purpose: Get comprehensive information about a specific country
- Parameters: country_name (str, required) - Name or code of the country
- Returns: JSON with country details including population, area, capital, languages, currencies
- API Endpoint: GET https://restcountries.com/v3.1/name/{country_name}
- Example Request: GET https://restcountries.com/v3.1/name/france
- Example Response: {"name": "France", "population": 67391582, "capital": "Paris", ...}

Function 2: search_countries
- Purpose: Search for countries by name or partial match
- Parameters: query (str, required) - Search term for country name
- Returns: JSON array of matching countries with basic info
- API Endpoint: GET https://restcountries.com/v3.1/name/{query}
- Example Request: GET https://restcountries.com/v3.1/name/united
- Example Response: [{"name": "United States"}, {"name": "United Kingdom"}, ...]

Function 3: get_country_comparison
- Purpose: Compare multiple countries side by side
- Parameters: countries (list, required) - List of 2-5 country names to compare
- Returns: JSON with comparison table of key metrics
- API Endpoint: Multiple calls to GET https://restcountries.com/v3.1/name/{country}
- Example Request: GET https://restcountries.com/v3.1/name/usa, GET https://restcountries.com/v3.1/name/canada
- Example Response: {"comparison": {"USA": {...}, "Canada": {...}}}
```

### **Natural Language Examples (Agent-Specific)**
```
Example Queries:
- "Tell me about France"
- "What countries are in Europe?"
- "Compare the population of USA and China"
- "Search for countries with 'land' in the name"
- "Get information about Japan"

Example Responses:
- "France is a country in Western Europe with a population of 67.4 million people..."
- "Here are the countries in Europe: [list of countries]"
- "Population comparison: USA has 331 million people, China has 1.4 billion people"

Domain-Specific Terms: country names, population, capital, region, subregion, currencies, languages
```

### **Testing Data (Agent-Specific)**
```
API Test Data: Sample responses from REST Countries API
Success Cases: Valid country names like "France", "USA", "Japan"
Error Cases: Invalid country names like "NonExistentCountry"
Edge Cases: Countries with special characters, multiple countries with same name
Mock Data: Sample country objects for tools tests
```

### **Dependencies (Agent-Specific)**
```
Required Python Packages: aiohttp>=3.8.0, python-dateutil>=2.8.0
Package Versions: Minimum versions specified above
Special Dependencies: None
```

### **Configuration (Agent-Specific)**
```
Agent Card Skills: Country information, demographics, geography, cultural data
Discovery Settings: Discoverable by other agents needing country data
Communication: Standard A2A protocol
YAML Configuration: Standard agent configuration with country-specific skills
```

### **Testing Requirements**
```
API Tests: 
- Test REST Countries API endpoints directly
- Test IP-API.com for geolocation fallback
- Validate response formats and error handling
- Test rate limits and timeouts

Tools Tests:
- Test agent functions with mocked API responses
- Test error handling and edge cases
- Test data formatting and validation
- Test statistics tracking and state management

Test Data:
- Success cases: Valid country names, search queries
- Error cases: Invalid country names, API failures
- Edge cases: Empty queries, special characters, multiple countries

Test Structure: Use sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
Mock Strategy: Mock google.adk.tools and solace_ai_connector.common.log before imports
```

### **Documentation Requirements**
```
README Content:
- Quick start guide and installation
- Example queries and responses
- Available tools table
- Test status and data sources
- Use cases and project structure

API Reference Content:
- Detailed function descriptions
- Parameter specifications
- Return value formats
- Example JSON responses
- Error handling documentation
- Natural language query examples
```

### **Dependencies & Requirements**
```
Python Packages: 
- aiohttp>=3.8.0 (async HTTP client for API calls)
- python-dateutil>=2.8.0 (date parsing utilities)
- pytest>=7.0.0 (testing framework)
- pytest-asyncio>=0.21.0 (async testing support)
- typing-extensions>=4.0.0 (type hints support)

Agent-Specific Requirements: Create src/country_information_agent/requirements.txt
Installation Instructions: pip install -r src/country_information_agent/requirements.txt
Common Dependencies: Inherit google.adk.tools, solace_ai_connector, solace-agent-mesh from parent
```

### **Advanced Features (Optional)**
```
Rate Limiting: No specific limits (REST Countries API is generous)
Caching: Cache country data for 24 hours to reduce API calls
Fallback APIs: IP-API.com for geolocation-based country detection
Data Validation: Validate country names and handle fuzzy matching
Statistics Tracking: Track popular countries, search queries, and usage patterns
```

---

## **🚀 USAGE INSTRUCTIONS**

### **For ChatGPT:**
1. Copy this template
2. Replace all `[REQUIRED]` sections with your specific requirements
3. Fill in `[OPTIONAL]` sections as needed
4. Paste into ChatGPT with: "Build a SAM agent using these requirements:"

### **For Manual Development:**
1. Fill in all required sections
2. Complete optional sections based on complexity needs
3. Use as specification document for development
4. Reference existing agents for implementation patterns

### **Quick Start:**
1. Start with Agent Identity and Core Functionality
2. Define 2-3 main tool functions
3. Specify input/output formats
4. Add natural language examples
5. Define testing requirements
6. Specify documentation needs
7. Define dependencies and requirements
8. Complete optional sections as needed

---

## **🧪 DEVELOPMENT WORKFLOW**

### **Phase 1: Planning**
- Complete all required sections of this template
- Identify external APIs and data sources
- Plan tool functions and error handling
- Design testing strategy
- Plan dependency management

### **Phase 2: Implementation**
- Create agent directory structure
- Implement core tool functions
- Add lifecycle management
- Create service layer (if needed)
- Create agent-specific requirements.txt

### **Phase 3: Testing**
- **API Tests**: Test external APIs directly (`test_<agent>_api.py`)
- **Tools Tests**: Test agent logic with mocked dependencies (`test_<agent>.py`)
  - Use proper import structure: `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))`
  - Mock SAM dependencies: `google.adk.tools` and `solace_ai_connector.common.log`
  - Use `AsyncMock` for async service methods
  - Test actual agent functions, not just mocks
- **Integration Tests**: Test agent in SAM environment
- **Documentation**: Create README.md and API_REFERENCE.md

### **Phase 4: Deployment**
- Run comprehensive test suite
- Deploy using `deploy_agent.py` (supports interactive agent selection)
- Verify deployment with `verify_agent.py`
- Test agent in SAM runtime

### **Phase 5: Maintenance**
- Monitor agent performance
- Update documentation as needed
- Add new features following established patterns
- Maintain test coverage

---

## **📁 REQUIRED FILE STRUCTURE**

```
src/<agent_name>/
├── __init__.py                    # Module initialization
├── lifecycle.py                   # Agent lifecycle functions
├── tools.py                       # Core tool functions
├── requirements.txt               # Agent-specific dependencies
├── .env.sample                    # Environment variables template
├── .gitignore                     # Git ignore rules
├── services/                      # Service layer (if needed)
│   ├── __init__.py
│   ├── <service_name>.py
│   ├── rate_limiter.py            # Rate limiting service
│   ├── cache_manager.py           # Caching service
│   └── <validator>.py             # Input validation service
├── tests/
│   ├── test_<agent>_api.py        # Direct API testing
│   └── test_<agent>.py            # Tools/function testing
├── API_REFERENCE.md               # Detailed API documentation
└── README.md                      # Quick start & overview

configs/agents/
└── <agent_name>.yaml              # Agent configuration
```

---

## **🔧 DEPLOYMENT TOOLS**

### **Enhanced Deployment Scripts**
The project includes advanced deployment tools:

#### **deploy_agent.py** - Generic Deployment Tool
```bash
# List available agents
python deploy_agent.py <sam_path> --list

# Interactive agent selection
python deploy_agent.py <sam_path>

# Deploy specific agent
python deploy_agent.py <sam_path> [agent_name] [source_dir]
```

#### **undeploy_agent.py** - Agent Removal Tool
```bash
# List deployed agents
python undeploy_agent.py <sam_path> --list

# Interactive agent selection for undeployment
python undeploy_agent.py <sam_path>

# Undeploy specific agent
python undeploy_agent.py <sam_path> [agent_name]
```

#### **verify_agent.py** - Deployment Verification
```bash
# Verify any agent deployment
python verify_agent.py <sam_path> [agent_name] [source_dir]
```

### **Key Features**
- **Auto-detection**: Automatically finds agent source code
- **Interactive Selection**: Choose from available agents
- **Dynamic Customization**: Replaces agent-specific references
- **Flexible Naming**: Supports custom agent names
- **Smart Configuration**: Updates config files automatically
- **Comprehensive Verification**: Checks all deployment aspects

---

## **📦 DEPENDENCY MANAGEMENT**

### **Individual Agent Requirements**
Each agent must have its own `requirements.txt` file with specific dependencies:

```bash
# Agent-specific requirements structure
src/
├── find_my_ip_agent/
│   ├── requirements.txt          # IP agent dependencies
│   └── ...
├── weather_trend_agent/
│   ├── requirements.txt          # Weather agent dependencies
│   └── ...
├── country_information_agent/
│   ├── requirements.txt          # Country agent dependencies
│   └── ...
└── news_snapshot_agent/
    ├── requirements.txt          # News agent dependencies
    └── ...
```

### **Installation Strategy**
After deployment, install dependencies in this order:

```bash
# 1. Navigate to SAM installation
cd /opt/sam

# 2. Install base dependencies (if not already installed)
pip install -r requirements.txt

# 3. Install agent-specific dependencies
pip install -r src/my-agent/requirements.txt
```

### **Common Dependencies**
All agents inherit these common dependencies from the parent project:
- `google.adk.tools` - SAM framework tools
- `solace_ai_connector` - SAM connector framework
- `solace-agent-mesh` - SAM core framework

### **Agent-Specific Dependencies**
Each agent may require additional packages:
- **Weather Trend Agent**: `httpx`, `aiohttp`, `python-dateutil`
- **Find My IP Agent**: `httpx`, `python-dateutil`
- **Country Information Agent**: `aiohttp`, `python-dateutil`
- **News Snapshot Agent**: `httpx`, `python-dateutil`

---

## **🔑 KEY LESSONS LEARNED**

### **Environment Configuration Best Practices**
- **Always create `.env.sample`**: Document all required environment variables with clear instructions
- **API Key Management**: Use environment variables for API keys, never hardcode them
- **Security**: Include `.gitignore` to prevent committing sensitive `.env` files
- **Documentation**: Provide clear setup instructions in README.md

### **Testing Strategy Insights**
- **Dual Test Approach**: Separate API tests (real calls) from tools tests (mocked dependencies)
- **Mock Import Paths**: Use exact import paths for mocking (e.g., `'services.exchange_rate_service.ExchangeRateService'`)
- **Test Environment**: Ensure tests can run with or without API keys
- **Mocking Challenges**: Be aware that mocking complex service layers requires careful import path management

### **Service Layer Architecture**
- **Separation of Concerns**: Create dedicated service classes for API communication, validation, caching, and rate limiting
- **Async Patterns**: Use async context managers for HTTP clients
- **Error Handling**: Centralize error handling in service classes
- **State Management**: Track usage statistics and maintain agent state

### **Common Pitfalls to Avoid**
- **Import Path Issues**: Incorrect mocking paths can cause tests to run real code instead of mocks
- **Missing Dependencies**: Always include `pytest-asyncio` for async testing
- **Environment Setup**: Missing `.env.sample` makes agent setup difficult for users
- **Documentation Gaps**: Incomplete setup instructions lead to user confusion

### **Success Patterns**
- **Comprehensive Documentation**: Both README.md and API_REFERENCE.md are essential
- **Robust Error Handling**: Handle API failures, rate limits, and validation errors gracefully
- **User-Friendly Setup**: Clear step-by-step instructions with examples
- **Production Ready**: Include rate limiting, caching, and monitoring capabilities

### **🔧 Critical SAM Integration Lessons (From Exchange Rate Agent Debugging)**

#### **Agent State Management Issues**
- **Problem**: "Agent not properly initialized" error in SAM despite working standalone
- **Root Cause**: Agent state not accessible through expected methods
- **Solution**: Implement robust state access with multiple fallback mechanisms:
  ```python
  def _get_agent_state(tool_context, log_identifier):
      # Try SAM method first
      if hasattr(tool_context, 'get_agent_specific_state'):
          agent_state = tool_context.get_agent_specific_state("agent_state", {})
      # Fall back to ADK method
      elif hasattr(tool_context, 'state'):
          agent_state = getattr(tool_context.state, 'agent_state', {})
      # Final fallback to environment variables
      else:
          agent_state = create_state_from_environment()
  ```

#### **Function Signature Compatibility**
- **Problem**: `ValueError: Failed to parse the parameter context=None` in ADK
- **Root Cause**: Incompatible function signatures for automatic function calling
- **Solution**: Use exact signature pattern:
  ```python
  async def function_name(
      param1: str,
      tool_context: Optional[ToolContext] = None,
      tool_config: Optional[Dict[str, Any]] = None
  ) -> Dict[str, Any]:
  ```

#### **Environment Variable Fallback Strategy**
- **Problem**: API keys available in environment but agent state empty
- **Root Cause**: State management inconsistency between test and SAM environments
- **Solution**: Smart fallback that creates state from environment when needed:
  ```python
  if not agent_state and env_api_key:
      log.info("Agent state is empty but API key available, creating state from environment")
      agent_state = create_state_from_environment()
  ```

#### **Debugging in SAM Environment**
- **Problem**: Difficult to debug issues in deployed SAM environment
- **Solution**: Use proper logging strategy:
  - Use `log.info()` and `log.error()` for production logging
  - Avoid `print()` statements in production code
  - Log state access attempts and failures
  - Provide detailed error context

#### **Testing vs Production Differences**
- **Problem**: Tests pass but agent fails in SAM
- **Root Cause**: Different state access mechanisms between test and SAM environments
- **Solution**: Test both scenarios:
  - Test with mocked SAM dependencies
  - Test environment variable fallback
  - Test state access failures
  - Test function signature compatibility

#### **Common SAM Integration Pitfalls**
1. **State Access Methods**: ToolContext might not have expected methods
2. **Environment Variable Availability**: API keys might not be available in SAM
3. **Function Signature Parsing**: ADK is strict about parameter types and defaults
4. **Lifecycle Integration**: State must be properly initialized in lifecycle functions
5. **Error Handling**: Must handle all possible failure modes gracefully

#### **Best Practices for API Key Agents**
- **Multiple Loading Strategies**: Try multiple locations for .env files
- **Robust Validation**: Validate API keys for presence, format, and requirements
- **Graceful Degradation**: Provide helpful error messages when API keys are missing
- **State Persistence**: Store API keys and configuration in agent state
- **Fallback Mechanisms**: Always provide fallback to environment variables

---

## **✅ CHECKLIST**

Before using this template, ensure you have:
- [ ] Clear understanding of what the agent should do
- [ ] Identified the primary data source/API
- [ ] Defined the main functions the agent will provide
- [ ] Thought about how users will interact with the agent
- [ ] Considered error handling and edge cases
- [ ] Planned testing strategy (API + Tools tests)
- [ ] Defined documentation requirements
- [ ] Planned dependency management strategy
- [ ] Considered deployment and maintenance needs

### **Quality Assurance Checklist:**
- [ ] All required sections completed
- [ ] Tool functions clearly defined with parameters and returns
- [ ] Input/output formats specified
- [ ] Natural language examples provided
- [ ] Testing requirements defined
- [ ] Documentation requirements specified
- [ ] Dependencies and requirements specified
- [ ] Optional sections completed as needed
- [ ] File structure requirements understood

### **Deployment Checklist:**
- [ ] Agent source code implemented and tested
- [ ] Agent-specific requirements.txt created
- [ ] Documentation (README.md and API_REFERENCE.md) complete
- [ ] Both API and tools tests passing
- [ ] Agent configuration YAML file created
- [ ] Ready for deployment using deploy_agent.py

This template ensures all critical aspects are covered while maintaining consistency with existing SAM agent patterns and incorporating best practices from hands-on development experience, including the enhanced deployment tools and improved dependency management.