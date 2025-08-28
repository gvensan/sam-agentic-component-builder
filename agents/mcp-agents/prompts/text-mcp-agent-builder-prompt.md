# **SAM MCP Agent Builder Prompt - Text MCP Agent**

Use this template to create comprehensive requirements for building a new SAM-based MCP agent for text processing and manipulation using the Text MCP Server.

---

## **🔴 MCP AGENT-SPECIFIC REQUIREMENTS (Fill These In)**

### **Agent Identity**
```
Agent Name: text_mcp_agent
Display Name: Text MCP Agent
Description: Provides text processing, search, and manipulation capabilities through MCP integration
Version: 1.0.0
```

### **MCP Server Details**
```
MCP Server Name: @modelcontextprotocol/server-text
MCP Server Package: @modelcontextprotocol/server-text
MCP Server Documentation: https://github.com/modelcontextprotocol/server-text
Connection Type: stdio
Server Command: npx
Server Arguments: -y @modelcontextprotocol/server-text
Working Directory: /tmp/text_workspace
```

### **MCP Server Configuration**
```
Authentication Method: None (local text processing)
Authentication Requirements: None
Rate Limits: No specific limits (local processing)
Resource Requirements: Minimal (text processing only)
Dependencies: Node.js, NPM
```

### **Environment Variables**
```
Required Environment Variables:
- MCP_SERVER_COMMAND: npx
- MCP_SERVER_ARGS: -y @modelcontextprotocol/server-text
- MCP_WORKING_DIR: /tmp/text_workspace
- MCP_DEBUG_MODE: false
- MCP_LOG_LEVEL: INFO

Example .env.sample content:
MCP_SERVER_COMMAND=npx
MCP_SERVER_ARGS=-y @modelcontextprotocol/server-text
MCP_WORKING_DIR=/tmp/text_workspace
MCP_DEBUG_MODE=false
MCP_LOG_LEVEL=INFO
```

### **MCP Tools (Agent-Specific)**
```
Available Tools: read_text, write_text, search_text, replace_text, split_text, join_text, extract_text, analyze_text
Tool Filtering: Expose all text processing tools

Tool 1: read_text
- Purpose: Read text content from a file or input
- Parameters: source (string, required) - File path or text content to read
- Returns: Text content as string
- Example Usage: read_text("/tmp/text_workspace/document.txt")
- Error Cases: File not found, permission denied, invalid encoding

Tool 2: write_text
- Purpose: Write text content to a file
- Parameters: destination (string, required) - File path, content (string, required) - Text content to write
- Returns: Success confirmation
- Example Usage: write_text("/tmp/text_workspace/output.txt", "Hello World")
- Error Cases: Permission denied, disk full, invalid path

Tool 3: search_text
- Purpose: Search for text patterns within content
- Parameters: content (string, required) - Text to search in, pattern (string, required) - Search pattern/regex
- Returns: Array of matches with positions
- Example Usage: search_text("Hello world, hello universe", "hello")
- Error Cases: Invalid regex pattern, empty content

Tool 4: replace_text
- Purpose: Replace text patterns within content
- Parameters: content (string, required) - Original text, pattern (string, required) - Pattern to replace, replacement (string, required) - Replacement text
- Returns: Modified text content
- Example Usage: replace_text("Hello world", "world", "universe")
- Error Cases: Invalid regex pattern, empty content

Tool 5: split_text
- Purpose: Split text into parts based on delimiter
- Parameters: content (string, required) - Text to split, delimiter (string, required) - Delimiter character/string
- Returns: Array of text parts
- Example Usage: split_text("apple,banana,orange", ",")
- Error Cases: Empty content, invalid delimiter

Tool 6: join_text
- Purpose: Join text parts with a delimiter
- Parameters: parts (array, required) - Array of text parts, delimiter (string, required) - Delimiter to use
- Returns: Joined text string
- Example Usage: join_text(["apple", "banana", "orange"], ", ")
- Error Cases: Empty array, invalid delimiter

Tool 7: extract_text
- Purpose: Extract text using patterns or rules
- Parameters: content (string, required) - Source text, pattern (string, required) - Extraction pattern/regex
- Returns: Extracted text content
- Example Usage: extract_text("Email: user@example.com", "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b")
- Error Cases: Invalid regex pattern, no matches found

Tool 8: analyze_text
- Purpose: Analyze text content for statistics and insights
- Parameters: content (string, required) - Text to analyze
- Returns: Analysis results (word count, character count, sentiment, etc.)
- Example Usage: analyze_text("This is a sample text for analysis.")
- Error Cases: Empty content, encoding issues
```

### **Natural Language Examples (MCP-Specific)**
```
Example Queries:
- "Read the contents of document.txt"
- "Search for the word 'hello' in this text"
- "Replace all instances of 'old' with 'new' in the content"
- "Split this text by commas"
- "Join these words with spaces"
- "Extract all email addresses from this text"
- "Analyze the sentiment of this text"

Example Responses:
- "Here are the contents of document.txt: [file contents]"
- "Found 3 matches for 'hello' at positions: [positions]"
- "Text with replacements: [modified text]"
- "Split text: [array of parts]"
- "Joined text: [joined string]"
- "Extracted email addresses: [email list]"
- "Analysis results: Word count: 150, Character count: 750, Sentiment: positive"

Domain-Specific Terms: text, content, pattern, regex, delimiter, sentiment, analysis, extraction, search, replace
MCP Tool Usage: Users can reference text operations by natural language and specify patterns or rules for text processing
```

### **Testing Data (MCP-Specific)**
```
MCP Server Test Data: Sample text files, various text formats, different encodings
Tool Success Cases: Valid text content, proper regex patterns, existing files
Tool Error Cases: Empty content, invalid regex patterns, non-existent files, permission errors
Integration Test Cases: Full text processing workflows, multiple tool combinations
Mock MCP Server: Mock text processing responses for testing
```

### **Dependencies (MCP-Specific)**
```
MCP Server Dependencies: Node.js, NPM
Python Packages: pytest, pytest-asyncio, pytest-mock, text-processing-utils
Node.js Packages: @modelcontextprotocol/server-text
Docker Images: None
System Requirements: Unix-like system with text processing capabilities
```

### **Configuration (MCP-Specific)**
```
Agent Card Skills: Text processing, text analysis, pattern matching, content manipulation
Discovery Settings: Discoverable by other agents needing text processing capabilities
Communication: Standard A2A protocol
YAML Configuration: Standard agent configuration with text processing skills
Tool Exposure: Expose all text processing tools for maximum functionality
```

---

## **🟡 OPTIONAL MCP-SPECIFIC FEATURES**

### **Advanced MCP Features**
```
Tool Filtering: [OPTIONAL] Specific text processing tools to expose or hide
Custom Wrappers: [OPTIONAL] Custom Python wrappers around text processing tools
Resource Management: [OPTIONAL] Advanced resource management for large text files
Monitoring: [OPTIONAL] Text processing performance monitoring
Fallback Strategies: [OPTIONAL] Fallback mechanisms when text processing fails
```

### **Security & Privacy (MCP-Specific)**
```
Authentication: [OPTIONAL] None required for local text processing
Authorization: [OPTIONAL] File system permissions for text file access
Data Privacy: [OPTIONAL] Handle sensitive text content securely
Audit Logging: [OPTIONAL] Logging of text processing operations
```

### **Performance & Optimization**
```
Text Processing: [OPTIONAL] Efficient handling of large text files
Caching: [OPTIONAL] Cache frequently processed text content
Memory Management: [OPTIONAL] Memory-efficient text processing for large files
Encoding Support: [OPTIONAL] Support for various text encodings (UTF-8, ASCII, etc.)
```

---

## **🚀 USAGE INSTRUCTIONS**

### **For ChatGPT:**
1. Copy this template
2. Replace all `[REQUIRED]` sections with your specific MCP agent requirements
3. Fill in `[OPTIONAL]` sections as needed
4. Paste into ChatGPT with: "Build a SAM MCP agent using these requirements:"

### **For Manual Development:**
1. Fill in all required sections
2. Complete optional sections based on complexity needs
3. Use as specification document for MCP agent development
4. Reference existing MCP agents for implementation patterns

### **Quick Start:**
1. Start with Agent Identity and MCP Server Details
2. Define MCP server configuration and connection type
3. Specify available MCP tools and their usage
4. Add natural language examples
5. Define testing requirements
6. Specify dependencies and configuration
7. Complete optional sections as needed

---

## **🧪 DEVELOPMENT WORKFLOW**

### **Phase 1: Planning**
- Complete all required sections of this template
- Identify MCP server and connection type
- Plan tool filtering and exposure strategy
- Design error handling and recovery
- Plan testing strategy

### **Phase 2: Implementation**
- Create MCP agent directory structure
- Configure MCP server connection
- Implement tool filtering (if needed)
- Add error handling and recovery
- Create MCP server setup scripts

### **Phase 3: Testing**
- **MCP Server Tests**: Test server connectivity and tool discovery
- **Tool Tests**: Test individual MCP tool functionality
- **Integration Tests**: Test agent with MCP tools
- **Error Tests**: Test error handling and recovery
- **Documentation**: Create README.md and API_REFERENCE.md

### **Phase 4: Deployment**
- Run comprehensive test suite
- Deploy using SAM deployment tools
- Verify MCP server connectivity
- Test agent in SAM runtime

### **Phase 5: Maintenance**
- Monitor MCP server health
- Update MCP server configuration as needed
- Maintain tool compatibility
- Update documentation

---

## **📁 REQUIRED FILE STRUCTURE**

```
src/text_mcp_agent/
├── __init__.py                    # Module initialization
├── lifecycle.py                   # Agent lifecycle functions
├── tools.py                       # Core tool functions
├── requirements.txt               # Agent-specific dependencies
├── .env.sample                    # Environment variables template
├── .gitignore                     # Git ignore rules
├── mcp_config/                    # MCP server configuration
│   ├── server_config.yaml         # MCP server configuration
│   └── tools_config.yaml          # Tool-specific configuration
├── tests/
│   ├── test_mcp_server.py         # MCP server connectivity tests
│   ├── test_mcp_tools.py          # MCP tool functionality tests
│   └── test_agent_integration.py  # Agent integration tests
├── API_REFERENCE.md               # Detailed MCP tool documentation
└── README.md                      # Quick start & overview

configs/agents/
└── text_mcp_agent.yaml            # Agent configuration
```

---

## **🔧 DEPLOYMENT TOOLS**

### **MCP Server Setup Scripts**
The project includes MCP server setup tools:

#### **setup_mcp_server.sh** - MCP Server Setup
```bash
#!/bin/bash
# Setup MCP server dependencies and configuration

# Install MCP server dependencies
npm install -g @modelcontextprotocol/server-text

# Create working directory
mkdir -p /tmp/text_workspace

# Set up environment variables
export MCP_SERVER_COMMAND="npx"
export MCP_SERVER_ARGS="-y @modelcontextprotocol/server-text"
export MCP_WORKING_DIR="/tmp/text_workspace"

echo "Text MCP server setup complete"
```

#### **test_mcp_server.py** - MCP Server Testing
```python
#!/usr/bin/env python3
# Test MCP server connectivity and functionality

import subprocess
import sys

def test_mcp_server():
    """Test MCP server startup and basic functionality"""
    try:
        result = subprocess.run(
            ["npx", "-y", "@modelcontextprotocol/server-text"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"Text MCP server test result: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"Text MCP server test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
```

---

## **📦 DEPENDENCY MANAGEMENT**

### **MCP Server Dependencies**
Each MCP agent must manage its own MCP server dependencies:

```bash
# MCP server dependencies (varies by server type)
npm install -g @modelcontextprotocol/server-text  # For text processing server
```

### **Agent Dependencies**
Each MCP agent must have its own `requirements.txt` file:

```txt
# src/text_mcp_agent/requirements.txt
# MCP-specific dependencies
mcp-client>=1.0.0
mcp-server-utils>=1.0.0

# Text processing utilities
text-processing-utils>=1.0.0

# Testing dependencies
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0

# SAM dependencies (inherited)
google-adk-tools
solace-ai-connector
```

---

## **🔑 KEY LESSONS LEARNED**

### **MCP Server Integration Best Practices**
- **Choose Well-Maintained Servers**: Select MCP servers with active community support
- **Test Independently**: Always test MCP server functionality before integration
- **Handle Failures Gracefully**: Implement proper error handling for MCP server failures
- **Resource Management**: Properly manage MCP server resources and connections
- **Security First**: Implement proper authentication and authorization for MCP tools

### **Common MCP Integration Issues**
- **Connection Failures**: MCP server not starting or connecting properly
- **Tool Discovery**: Agent unable to discover MCP tools
- **Authentication Issues**: MCP server authentication failures
- **Resource Leaks**: MCP server resources not properly managed
- **Version Compatibility**: MCP server version incompatibilities

### **Success Patterns**
- **Comprehensive Testing**: Test MCP server, tools, and integration thoroughly
- **Clear Documentation**: Document MCP server setup and tool usage clearly
- **Error Handling**: Implement robust error handling and recovery
- **Monitoring**: Monitor MCP server health and performance
- **Security**: Implement proper security measures for MCP tools

---

## **✅ CHECKLIST**

Before using this template, ensure you have:
- [ ] Clear understanding of what the MCP agent should do
- [ ] Identified the MCP server to integrate with
- [ ] Defined the MCP tools the agent will provide
- [ ] Thought about how users will interact with the MCP agent
- [ ] Considered error handling and recovery strategies
- [ ] Planned testing strategy (MCP server + Tools + Integration tests)
- [ ] Defined documentation requirements
- [ ] Planned dependency management strategy
- [ ] Considered deployment and maintenance needs

### **Quality Assurance Checklist:**
- [ ] All required sections completed
- [ ] MCP server details clearly defined
- [ ] Tool functions clearly defined with parameters and returns
- [ ] Natural language examples provided
- [ ] Testing requirements defined
- [ ] Documentation requirements specified
- [ ] Dependencies and requirements specified
- [ ] Optional sections completed as needed
- [ ] File structure requirements understood

### **Deployment Checklist:**
- [ ] MCP agent source code implemented and tested
- [ ] MCP server dependencies installed and configured
- [ ] Agent-specific requirements.txt created
- [ ] Documentation (README.md and API_REFERENCE.md) complete
- [ ] All tests passing (MCP server, tools, integration)
- [ ] Agent configuration YAML file created
- [ ] Ready for deployment using SAM tools

This template ensures all critical aspects are covered while maintaining consistency with existing SAM MCP agent patterns and incorporating best practices from MCP integration experience.
