# **SAM Agent Builder Prompt - OpenTable Restaurant Booking Agent**

Use this template to create comprehensive requirements for building a new SAM-based agent. Fill in the sections marked as **REQUIRED** and optionally complete the **OPTIONAL** sections based on your needs.

---

## **🔴 REQUIRED SECTIONS (Must Complete)**

### **Agent Identity**
```
Agent Name: open_table_restaurant_agent
Display Name: OpenTable Restaurant Booking Agent
Description: Provides restaurant search, availability checking, and reservation information using the OpenTable API
Version: 1.0.0
```

### **Core Functionality**
```
Primary Function: Search restaurants and check availability for dining reservations
Secondary Functions: 
- Get restaurant details, reviews, and ratings
- Find restaurants by location, cuisine, and price range
- Check reservation availability for specific dates and times
- Get restaurant contact information and hours
Data Source: https://opentable.herokuapp.com/ (no authentication required)
Authentication: None (free public API)
```

### **Tool Functions**
```
Function 1: search_restaurants
- Purpose: Search for restaurants by location, cuisine, or name
- Parameters: location (str, required), cuisine (str, optional), name (str, optional), price_range (str, optional)
- Returns: JSON with list of restaurants including name, address, cuisine, price range, rating
- Example: search_restaurants("New York", "Italian", "price_range": "$$") returns Italian restaurants in NYC

Function 2: get_restaurant_details
- Purpose: Get detailed information about a specific restaurant
- Parameters: restaurant_id (str, required)
- Returns: JSON with restaurant details including menu, hours, contact info, reviews
- Example: get_restaurant_details("12345") returns complete restaurant information

Function 3: check_availability
- Purpose: Check reservation availability for a specific restaurant and date/time
- Parameters: restaurant_id (str, required), date (str, required), time (str, required), party_size (int, required)
- Returns: JSON with available time slots and reservation options
- Example: check_availability("12345", "2024-01-15", "19:00", 4) returns available slots for 4 people

Function 4: get_restaurants_by_location
- Purpose: Find restaurants near a specific location or coordinates
- Parameters: latitude (float, required), longitude (float, required), radius (int, optional)
- Returns: JSON with nearby restaurants sorted by distance
- Example: get_restaurants_by_location(40.7128, -74.0060, 5) returns restaurants within 5 miles of NYC coordinates

Function 5: get_cuisine_types
- Purpose: Get list of available cuisine types for filtering
- Parameters: None
- Returns: JSON with list of cuisine categories and descriptions
- Example: get_cuisine_types() returns all available cuisine types like Italian, Japanese, Mexican, etc.
```

### **Input/Output Format**
```
Input Parameters: location (string), cuisine (string), restaurant_id (string), date (string), time (string), party_size (integer), latitude (float), longitude (float), radius (integer)
Output Format: {
  "status": "success|error",
  "data": {
    "restaurants": [
      {
        "id": "string",
        "name": "string",
        "address": "string",
        "city": "string",
        "state": "string",
        "zip": "string",
        "phone": "string",
        "cuisine": "string",
        "price_range": "string",
        "rating": "float",
        "review_count": "integer",
        "latitude": "float",
        "longitude": "float"
      }
    ],
    "availability": [
      {
        "date": "string",
        "time": "string",
        "party_size": "integer",
        "available": "boolean"
      }
    ],
    "restaurant_details": {
      "id": "string",
      "name": "string",
      "description": "string",
      "hours": "object",
      "menu": "array",
      "reviews": "array"
    }
  },
  "timestamp": "ISO format",
  "source": "opentable"
}
Error Responses: {
  "status": "error",
  "error": "error message",
  "error_type": "error_category",
  "timestamp": "ISO format"
}
```

### **Natural Language Examples**
```
Example Queries:
- "Find Italian restaurants in New York City"
- "Show me restaurants near Times Square"
- "What's available for dinner tonight at 7 PM for 4 people?"
- "Get details about Restaurant ABC"
- "Find restaurants with 4-star ratings in San Francisco"
- "Show me Mexican restaurants under $30 per person"
- "What cuisines are available in Chicago?"

Example Responses:
- "I found 15 Italian restaurants in New York City. Here are the top 5: [restaurant list]"
- "There are 8 restaurants within 1 mile of Times Square. The closest is [restaurant name] at [address]"
- "For dinner tonight at 7 PM for 4 people, I found these available options: [availability list]"
- "Restaurant ABC is located at [address] and serves [cuisine]. They're open [hours] and have a [rating] star rating"
- "Here are 12 restaurants with 4-star ratings in San Francisco: [restaurant list]"
```

### **Testing Requirements**
```
API Tests: 
- Test OpenTable API endpoints directly
- Test restaurant search functionality
- Test availability checking
- Validate response formats and error handling
- Test location-based search
- Test cuisine filtering

Tools Tests:
- Test agent functions with mocked API responses
- Test error handling and edge cases
- Test data formatting and validation
- Test location validation and geocoding
- Test date/time parsing and validation

Test Data:
- Success cases: Valid locations, restaurant IDs, dates/times
- Error cases: Invalid restaurant IDs, unavailable dates, API failures
- Edge cases: Empty searches, special characters, future dates

Test Structure: Use sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
Mock Strategy: Mock google.adk.tools and solace_ai_connector.common.log before imports
Mock Import Paths: Use exact import paths for mocking (e.g., 'services.opentable_service.OpenTableService')
Dual Test Strategy: Separate API tests (real API calls) from tools tests (mocked dependencies)
Test Environment Setup: No API key required, but test with various location inputs
```

### **Documentation Requirements**
```
README Content:
- Quick start guide and installation
- Example queries and responses
- Available tools table
- Test status and data sources
- Use cases and project structure
- Location-based search examples
- Reservation checking workflow

API Reference Content:
- Detailed function descriptions
- Parameter specifications
- Return value formats
- Example JSON responses
- Error handling documentation
- Natural language query examples
- Location format requirements
- Date/time format specifications
```

### **Dependencies & Requirements**
```
Python Packages: 
- httpx>=0.24.0 (async HTTP client for API calls)
- python-dateutil>=2.8.0 (date parsing utilities)
- geopy>=2.3.0 (geocoding and location services)
- pytest>=7.0.0 (testing framework)
- pytest-asyncio>=0.21.0 (async testing support)
- typing-extensions>=4.0.0 (type hints support)

Agent-Specific Requirements: Create src/open_table_restaurant_agent/requirements.txt
Installation Instructions: pip install -r src/open_table_restaurant_agent/requirements.txt
Common Dependencies: Inherit google.adk.tools, solace_ai_connector, solace-agent-mesh from parent
Environment Variables: No API key required, but may need location service configuration
API Key Management: No API key required for OpenTable API
```

---

## **🟡 OPTIONAL SECTIONS (Complete as Needed)**

### **Advanced Features**
```
Rate Limiting: No specific limits (OpenTable API is generous)
Caching: Cache restaurant data for 1 hour to reduce API calls
Fallback APIs: Google Places API for additional restaurant information
Data Validation: Validate location formats, date/time inputs, party sizes
Statistics Tracking: Track popular locations, cuisine types, and search patterns
Geocoding: Convert addresses to coordinates for location-based searches
```

### **Lifecycle Management**
```
Initialization: Set up geocoding service and cache manager
Cleanup: Clear cached data and log usage statistics
State Management: Store recent searches and popular locations
Statistics: Track search patterns, popular cuisines, and location preferences
```

### **Service Layer Design**
```
Service Classes: 
- OpenTableService: Main API communication for restaurant data
- GeocodingService: Location validation and coordinate conversion
- CacheManager: Restaurant data caching with configurable TTL
- ValidationService: Input validation for locations, dates, and party sizes
- AvailabilityService: Reservation availability checking and time slot management

Error Handling: Centralized error handling for API failures, invalid locations, and date parsing
Connection Management: HTTP session reuse and connection pooling
Response Processing: Data transformation, rating normalization, and distance calculations
Rate Limiting: Implement basic rate limiting to be respectful to the API
Caching: In-memory caching with configurable TTL to reduce API calls
Validation: Input validation classes for location, date, and party size validation
```

### **Configuration Options**
```
Agent Card: Restaurant booking and discovery capabilities
Discovery Settings: Make agent discoverable for restaurant-related queries
Communication: Inter-agent communication for location-based services
YAML Configuration: Custom YAML configuration for default locations and preferences
```

### **Testing Best Practices**
```
Import Structure: Use sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
Mock Dependencies: Mock google.adk.tools and solace_ai_connector.common.log before imports
Async Testing: Use AsyncMock for async service methods
Test Coverage: Aim for 100% test coverage with success, error, and edge cases
Real Function Testing: Test actual agent functions, not just mocks
Mock Import Paths: Use exact import paths for mocking (e.g., 'services.opentable_service.OpenTableService')
Dual Test Strategy: Separate API tests (real API calls) from tools tests (mocked dependencies)
Environment Setup: No API key required, but test with various location and date inputs
```

### **Security & Privacy**
```
Data Privacy: Handle location data responsibly
API Key Management: No API key required for OpenTable API
Logging: Log search patterns but not personal location data
```

### **Deployment Considerations**
```
File Structure: Standard agent structure with service layer
Configuration Files: YAML configuration for default locations and preferences
Dependencies: Standard Python packages with geocoding support
```

---

## **📋 COMPLETE EXAMPLE**

Here's a complete example using the OpenTable Restaurant Booking Agent:

### **Agent Identity**
```
Agent Name: open_table_restaurant_agent
Display Name: OpenTable Restaurant Booking Agent
Description: Provides restaurant search, availability checking, and reservation information using the OpenTable API
Version: 1.0.0
```

### **Core Functionality**
```
Primary Function: Search restaurants and check availability for dining reservations
Secondary Functions: 
- Get restaurant details, reviews, and ratings
- Find restaurants by location, cuisine, and price range
- Check reservation availability for specific dates and times
- Get restaurant contact information and hours
Data Source: https://opentable.herokuapp.com/ (no authentication required)
Authentication: None (free public API)
```

### **Tool Functions**
```
Function 1: search_restaurants
- Purpose: Search for restaurants by location, cuisine, or name
- Parameters: location (str, required), cuisine (str, optional), name (str, optional), price_range (str, optional)
- Returns: JSON with list of restaurants including name, address, cuisine, price range, rating
- Example: search_restaurants("New York", "Italian", "price_range": "$$") returns Italian restaurants in NYC

Function 2: get_restaurant_details
- Purpose: Get detailed information about a specific restaurant
- Parameters: restaurant_id (str, required)
- Returns: JSON with restaurant details including menu, hours, contact info, reviews
- Example: get_restaurant_details("12345") returns complete restaurant information

Function 3: check_availability
- Purpose: Check reservation availability for a specific restaurant and date/time
- Parameters: restaurant_id (str, required), date (str, required), time (str, required), party_size (int, required)
- Returns: JSON with available time slots and reservation options
- Example: check_availability("12345", "2024-01-15", "19:00", 4) returns available slots for 4 people

Function 4: get_restaurants_by_location
- Purpose: Find restaurants near a specific location or coordinates
- Parameters: latitude (float, required), longitude (float, required), radius (int, optional)
- Returns: JSON with nearby restaurants sorted by distance
- Example: get_restaurants_by_location(40.7128, -74.0060, 5) returns restaurants within 5 mile of NYC coordinates

Function 5: get_cuisine_types
- Purpose: Get list of available cuisine types for filtering
- Parameters: None
- Returns: JSON with list of cuisine categories and descriptions
- Example: get_cuisine_types() returns all available cuisine types like Italian, Japanese, Mexican, etc.
```

### **Input/Output Format**
```
Input Parameters: location (string), cuisine (string), restaurant_id (string), date (string), time (string), party_size (integer), latitude (float), longitude (float), radius (integer)
Output Format: {
  "status": "success|error",
  "data": {
    "restaurants": [
      {
        "id": "string",
        "name": "string",
        "address": "string",
        "city": "string",
        "state": "string",
        "zip": "string",
        "phone": "string",
        "cuisine": "string",
        "price_range": "string",
        "rating": "float",
        "review_count": "integer",
        "latitude": "float",
        "longitude": "float"
      }
    ],
    "availability": [
      {
        "date": "string",
        "time": "string",
        "party_size": "integer",
        "available": "boolean"
      }
    ],
    "restaurant_details": {
      "id": "string",
      "name": "string",
      "description": "string",
      "hours": "object",
      "menu": "array",
      "reviews": "array"
    }
  },
  "timestamp": "ISO format",
  "source": "opentable"
}
Error Responses: {
  "status": "error",
  "error": "error message",
  "error_type": "error_category",
  "timestamp": "ISO format"
}
```

### **Natural Language Examples**
```
Example Queries:
- "Find Italian restaurants in New York City"
- "Show me restaurants near Times Square"
- "What's available for dinner tonight at 7 PM for 4 people?"
- "Get details about Restaurant ABC"
- "Find restaurants with 4-star ratings in San Francisco"
- "Show me Mexican restaurants under $30 per person"
- "What cuisines are available in Chicago?"

Example Responses:
- "I found 15 Italian restaurants in New York City. Here are the top 5: [restaurant list]"
- "There are 8 restaurants within 1 mile of Times Square. The closest is [restaurant name] at [address]"
- "For dinner tonight at 7 PM for 4 people, I found these available options: [availability list]"
- "Restaurant ABC is located at [address] and serves [cuisine]. They're open [hours] and have a [rating] star rating"
- "Here are 12 restaurants with 4-star ratings in San Francisco: [restaurant list]"
```

### **Testing Requirements**
```
API Tests: 
- Test OpenTable API endpoints directly
- Test restaurant search functionality
- Test availability checking
- Validate response formats and error handling
- Test location-based search
- Test cuisine filtering

Tools Tests:
- Test agent functions with mocked API responses
- Test error handling and edge cases
- Test data formatting and validation
- Test location validation and geocoding
- Test date/time parsing and validation

Test Data:
- Success cases: Valid locations, restaurant IDs, dates/times
- Error cases: Invalid restaurant IDs, unavailable dates, API failures
- Edge cases: Empty searches, special characters, future dates

Test Structure: Use sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
Mock Strategy: Mock google.adk.tools and solace_ai_connector.common.log before imports
Mock Import Paths: Use exact import paths for mocking (e.g., 'services.opentable_service.OpenTableService')
Dual Test Strategy: Separate API tests (real API calls) from tools tests (mocked dependencies)
Test Environment Setup: No API key required, but test with various location inputs
```

### **Documentation Requirements**
```
README Content:
- Quick start guide and installation
- Example queries and responses
- Available tools table
- Test status and data sources
- Use cases and project structure
- Location-based search examples
- Reservation checking workflow

API Reference Content:
- Detailed function descriptions
- Parameter specifications
- Return value formats
- Example JSON responses
- Error handling documentation
- Natural language query examples
- Location format requirements
- Date/time format specifications
```

### **Dependencies & Requirements**
```
Python Packages: 
- httpx>=0.24.0 (async HTTP client for API calls)
- python-dateutil>=2.8.0 (date parsing utilities)
- geopy>=2.3.0 (geocoding and location services)
- pytest>=7.0.0 (testing framework)
- pytest-asyncio>=0.21.0 (async testing support)
- typing-extensions>=4.0.0 (type hints support)

Agent-Specific Requirements: Create src/open_table_restaurant_agent/requirements.txt
Installation Instructions: pip install -r src/open_table_restaurant_agent/requirements.txt
Common Dependencies: Inherit google.adk.tools, solace_ai_connector, solace-agent-mesh from parent
Environment Variables: No API key required, but may need location service configuration
API Key Management: No API key required for OpenTable API
```

### **Advanced Features (Optional)**
```
Rate Limiting: No specific limits (OpenTable API is generous)
Caching: Cache restaurant data for 1 hour to reduce API calls
Fallback APIs: Google Places API for additional restaurant information
Data Validation: Validate location formats, date/time inputs, party sizes
Statistics Tracking: Track popular locations, cuisine types, and search patterns
Geocoding: Convert addresses to coordinates for location-based searches
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
2. Define 5 main tool functions for restaurant operations
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
- Identify OpenTable API endpoints and capabilities
- Plan tool functions and error handling
- Design testing strategy
- Plan dependency management

### **Phase 2: Implementation**
- Create agent directory structure
- Implement core tool functions
- Add lifecycle management
- Create service layer (OpenTableService, GeocodingService, etc.)
- Create agent-specific requirements.txt

### **Phase 3: Testing**
- **API Tests**: Test OpenTable API directly (`test_open_table_restaurant_agent_api.py`)
- **Tools Tests**: Test agent logic with mocked dependencies (`test_open_table_restaurant_agent.py`)
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
src/open_table_restaurant_agent/
├── __init__.py                    # Module initialization
├── lifecycle.py                   # Agent lifecycle functions
├── tools.py                       # Core tool functions
├── requirements.txt               # Agent-specific dependencies
├── services/                      # Service layer
│   ├── __init__.py
│   ├── opentable_service.py       # OpenTable API communication
│   ├── geocoding_service.py       # Location services
│   ├── cache_manager.py           # Caching functionality
│   └── validation_service.py      # Input validation
├── tests/
│   ├── test_open_table_restaurant_agent_api.py  # Direct API testing
│   └── test_open_table_restaurant_agent.py      # Tools/function testing
├── API_REFERENCE.md               # Detailed API documentation
└── README.md                      # Quick start & overview

configs/agents/
└── open_table_restaurant_agent.yaml  # Agent configuration
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
├── open_table_restaurant_agent/
│   ├── requirements.txt          # OpenTable agent dependencies
│   └── ...
└── other_agents/
    ├── requirements.txt          # Other agent dependencies
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
pip install -r src/open_table_restaurant_agent/requirements.txt
```

### **Common Dependencies**
All agents inherit these common dependencies from the parent project:
- `google.adk.tools` - SAM framework tools
- `solace_ai_connector` - SAM connector framework
- `solace-agent-mesh` - SAM core framework

### **Agent-Specific Dependencies**
The OpenTable Restaurant Agent requires these additional packages:
- `httpx` - Async HTTP client for API calls
- `python-dateutil` - Date parsing utilities
- `geopy` - Geocoding and location services
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support

---

## **✅ CHECKLIST**

Before using this template, ensure you have:
- [ ] Clear understanding of what the agent should do
- [ ] Identified the OpenTable API endpoints and capabilities
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

