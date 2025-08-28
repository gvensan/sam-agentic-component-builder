# **SAM MCP Agent Builder Prompt Template**

Use this template to capture **MCP agent-specific details** for building a new SAM-based MCP agent. This template focuses on the **specific MCP server integration, tools, and configuration** for your agent, while general development guidelines are in `instructions.mdc`.

**📋 Before using this template:**
1. Review `instructions.mdc` for complete MCP agent development guidelines and best practices
2. Use this template to capture MCP-specific details (servers, tools, connections, etc.)
3. Follow the checklist in `instructions.mdc` for implementation

---

## **🔴 MCP AGENT-SPECIFIC REQUIREMENTS (Fill These In)**

### **Agent Identity**
```
Agent Name: [REQUIRED] The internal name for the MCP agent (e.g., "filesystem_mcp_agent", "database_mcp_agent")
Display Name: [REQUIRED] Human-readable name (e.g., "File System MCP Agent", "Database MCP Agent")
Description: [REQUIRED] Brief description of what the MCP agent does (1-2 sentences)
Version: [REQUIRED] Version number (e.g., "1.0.0")
```

### **MCP Server Details**
```
MCP Server Name: [REQUIRED] Name of the MCP server to integrate with
MCP Server Package: [REQUIRED] NPM package or Python module name
MCP Server Documentation: [REQUIRED] Link to MCP server documentation
Connection Type: [REQUIRED] stdio, sse, or docker
Server Command: [REQUIRED] Command to run the MCP server (e.g., "npx", "python", "docker")
Server Arguments: [REQUIRED] Arguments needed for the MCP server
Working Directory: [REQUIRED] Working directory for the MCP server (if applicable)
```

### **MCP Server Configuration**
```
Authentication Method: [REQUIRED] None, API key, OAuth, token, etc.
Authentication Requirements: [REQUIRED] What credentials are needed
Rate Limits: [REQUIRED] Any rate limits or usage restrictions
Resource Requirements: [REQUIRED] CPU, memory, disk space requirements
Dependencies: [REQUIRED] External dependencies (Node.js, Python, Docker, etc.)
```

### **Environment Variables**
```
Required Environment Variables:
- MCP_SERVER_COMMAND: [REQUIRED] Command to run the MCP server
- MCP_SERVER_ARGS: [REQUIRED] Arguments for the MCP server
- MCP_WORKING_DIR: [OPTIONAL] Working directory for the MCP server
- MCP_AUTH_TOKEN: [OPTIONAL] Authentication token (if required)
- MCP_API_KEY: [OPTIONAL] API key (if required)
- MCP_DEBUG_MODE: [OPTIONAL] Debug mode flag (default: false)
- MCP_LOG_LEVEL: [OPTIONAL] Log level (default: INFO)

Example .env.sample content:
MCP_SERVER_COMMAND=npx
MCP_SERVER_ARGS=-y @modelcontextprotocol/server-filesystem /tmp/samv2
MCP_WORKING_DIR=/tmp/samv2
MCP_DEBUG_MODE=false
MCP_LOG_LEVEL=INFO
```

### **MCP Tools (Agent-Specific)**
```
Available Tools: [REQUIRED] List all tools provided by the MCP server
Tool Filtering: [OPTIONAL] Which specific tools to expose (if not all)
Tool 1: [REQUIRED] [TOOL_NAME]
- Purpose: [REQUIRED] What this MCP tool does
- Parameters: [REQUIRED] Input parameters with types
- Returns: [REQUIRED] What the tool returns
- Example Usage: [REQUIRED] How to use this tool
- Error Cases: [REQUIRED] Common error scenarios

Tool 2: [REQUIRED] [TOOL_NAME]
- Purpose: [REQUIRED] What this MCP tool does
- Parameters: [REQUIRED] Input parameters with types
- Returns: [REQUIRED] What the tool returns
- Example Usage: [REQUIRED] How to use this tool
- Error Cases: [REQUIRED] Common error scenarios

[Add more tools as needed]
```

### **Natural Language Examples (MCP-Specific)**
```
Example Queries: [REQUIRED] List 3-5 example user questions specific to this MCP agent
Example Responses: [REQUIRED] Show how this MCP agent should respond to each query
Domain-Specific Terms: [REQUIRED] Any special terminology or concepts users might use
MCP Tool Usage: [REQUIRED] How users should reference MCP tools in their queries
```

### **Testing Requirements (MCP-Specific)**
```
Test Structure: [REQUIRED] Follow convention: src/<agent_name>/tests/test_<agent_name>.py
YAML Configuration Tests: [REQUIRED] Test YAML syntax and structure
MCP Server Availability: [REQUIRED] Test MCP server installation and startup
Agent Configuration: [REQUIRED] Test required fields and proper setup
Agent Instructions: [REQUIRED] Test instruction content and capabilities
Agent Card Configuration: [REQUIRED] Test skills, input/output modes, descriptions
Shared Config Integration: [REQUIRED] Test !include directive handling
Test Dependencies: [REQUIRED] pytest, PyYAML, solace-agent-mesh
Verification Script: [REQUIRED] Use verify_mcp_agent.py for deployment verification
```

### **Dependencies (MCP-Specific)**
```
MCP Server Dependencies: [REQUIRED] What needs to be installed for the MCP server
Python Packages: [REQUIRED] Python packages needed for the agent
Node.js Packages: [OPTIONAL] NPM packages needed (if applicable)
Docker Images: [OPTIONAL] Docker images needed (if applicable)
System Requirements: [REQUIRED] OS, version, and system requirements
```

### **Configuration (MCP-Specific)**
```
Agent Card Skills: [REQUIRED] What skills should be listed in the agent card
Discovery Settings: [REQUIRED] How other agents can discover this MCP agent
Communication: [REQUIRED] Any special communication requirements
YAML Configuration: [REQUIRED] Custom YAML configuration for MCP integration
Tool Exposure: [REQUIRED] Which MCP tools to expose and how
```

---

## **🟡 OPTIONAL MCP-SPECIFIC FEATURES**

### **Advanced MCP Features**
```
Tool Filtering: [OPTIONAL] Specific tools to expose or hide
Custom Wrappers: [OPTIONAL] Custom Python wrappers around MCP tools
Resource Management: [OPTIONAL] Advanced resource management for MCP server
Monitoring: [OPTIONAL] MCP server health monitoring
Fallback Strategies: [OPTIONAL] Fallback mechanisms when MCP server is unavailable
```

### **Security & Privacy (MCP-Specific)**
```
Authentication: [OPTIONAL] Advanced authentication for MCP server
Authorization: [OPTIONAL] Fine-grained access control for MCP tools
Data Privacy: [OPTIONAL] How to handle sensitive data in MCP tools
Audit Logging: [OPTIONAL] Logging of MCP tool usage and access
```

### **Performance & Optimization**
```
Connection Pooling: [OPTIONAL] Connection pooling for MCP server
Caching: [OPTIONAL] Caching strategies for MCP tool responses
Load Balancing: [OPTIONAL] Load balancing for multiple MCP server instances
Resource Limits: [OPTIONAL] Resource limits and quotas
```

---

## **📋 COMPLETE EXAMPLE**

Here's a complete example using the Filesystem MCP Agent:

### **Agent Identity**
```
Agent Name: filesystem_mcp_agent
Display Name: File System MCP Agent
Description: Provides filesystem access and management capabilities through MCP integration
Version: 1.0.0
```

### **MCP Server Details**
```
MCP Server Name: @modelcontextprotocol/server-filesystem
MCP Server Package: @modelcontextprotocol/server-filesystem
MCP Server Documentation: https://github.com/modelcontextprotocol/server-filesystem
Connection Type: stdio
Server Command: npx
Server Arguments: -y @modelcontextprotocol/server-filesystem /tmp/samv2
Working Directory: /tmp/samv2
```

### **MCP Server Configuration**
```
Authentication Method: None (local filesystem access)
Authentication Requirements: None
Rate Limits: No specific limits
Resource Requirements: Minimal (file system access only)
Dependencies: Node.js, NPM
```

### **Environment Variables**
```
Required Environment Variables:
- MCP_SERVER_COMMAND: npx
- MCP_SERVER_ARGS: -y @modelcontextprotocol/server-filesystem /tmp/samv2
- MCP_WORKING_DIR: /tmp/samv2

Example .env.sample content:
MCP_SERVER_COMMAND=npx
MCP_SERVER_ARGS=-y @modelcontextprotocol/server-filesystem /tmp/samv2
MCP_WORKING_DIR=/tmp/samv2
MCP_DEBUG_MODE=false
MCP_LOG_LEVEL=INFO
```

### **MCP Tools (Agent-Specific)**
```
Available Tools: read_file, write_file, list_directory, delete_file, create_directory
Tool Filtering: Expose all filesystem tools

Tool 1: read_file
- Purpose: Read contents of a file
- Parameters: path (string, required) - Path to the file to read
- Returns: File contents as string
- Example Usage: read_file("/tmp/samv2/test.txt")
- Error Cases: File not found, permission denied, file too large

Tool 2: write_file
- Purpose: Write content to a file
- Parameters: path (string, required) - Path to the file, content (string, required) - Content to write
- Returns: Success confirmation
- Example Usage: write_file("/tmp/samv2/new.txt", "Hello World")
- Error Cases: Permission denied, disk full, invalid path

Tool 3: list_directory
- Purpose: List contents of a directory
- Parameters: path (string, required) - Path to the directory
- Returns: Array of file and directory names
- Example Usage: list_directory("/tmp/samv2")
- Error Cases: Directory not found, permission denied

Tool 4: delete_file
- Purpose: Delete a file
- Parameters: path (string, required) - Path to the file to delete
- Returns: Success confirmation
- Example Usage: delete_file("/tmp/samv2/old.txt")
- Error Cases: File not found, permission denied

Tool 5: create_directory
- Purpose: Create a new directory
- Parameters: path (string, required) - Path for the new directory
- Returns: Success confirmation
- Example Usage: create_directory("/tmp/samv2/new_folder")
- Error Cases: Directory already exists, permission denied
```

### **Natural Language Examples (MCP-Specific)**
```
Example Queries:
- "Read the contents of test.txt"
- "Create a new file called hello.txt with the content 'Hello World'"
- "List all files in the current directory"
- "Delete the file old.txt"
- "Create a new folder called documents"

Example Responses:
- "Here are the contents of test.txt: [file contents]"
- "Successfully created hello.txt with the content 'Hello World'"
- "Files in the current directory: [list of files]"
- "Successfully deleted old.txt"
- "Successfully created the documents folder"

Domain-Specific Terms: file, directory, folder, path, read, write, create, delete, list
MCP Tool Usage: Users can reference files by path and use natural language to describe file operations
```

### **Testing Requirements (MCP-Specific)**
```
Test Structure: src/filesystem_mcp_agent/tests/test_filesystem_mcp_agent.py
YAML Configuration Tests: Test YAML syntax and structure with !include handling
MCP Server Availability: Test @modelcontextprotocol/server-filesystem startup
Agent Configuration: Test required fields (agent_name, display_name, model, tools, instruction)
Agent Instructions: Test filesystem-specific instruction content
Agent Card Configuration: Test skills (file system access, file management, directory operations)
Shared Config Integration: Test !include ../shared_config.yaml directive
Test Dependencies: pytest, PyYAML, solace-agent-mesh
Verification Script: Use verify_mcp_agent.py for deployment verification
```

### **Dependencies (MCP-Specific)**
```
MCP Server Dependencies: Node.js, NPM
Python Packages: pytest, pytest-asyncio, pytest-mock
Node.js Packages: @modelcontextprotocol/server-filesystem
Docker Images: None
System Requirements: Unix-like system with file system access
```

### **Configuration (MCP-Specific)**
```
Agent Card Skills: File system access, file management, directory operations
Discovery Settings: Discoverable by other agents needing file system access
Communication: Standard A2A protocol
YAML Configuration: Standard agent configuration with filesystem skills
Tool Exposure: Expose all filesystem tools for maximum functionality
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
- **YAML Configuration Tests**: Test YAML syntax and structure with !include handling
- **MCP Server Tests**: Test server availability and startup
- **Agent Configuration Tests**: Test required fields and proper setup
- **Agent Instructions Tests**: Test instruction content and capabilities
- **Agent Card Tests**: Test skills, input/output modes, and descriptions
- **Integration Tests**: Test shared config integration and deployment
- **Verification**: Use verify_mcp_agent.py for deployment verification

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
src/<mcp_agent_name>/
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
└── <mcp_agent_name>.yaml          # Agent configuration
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
npm install -g @modelcontextprotocol/server-filesystem

# Create working directory
mkdir -p /tmp/mcp_workspace

# Set up environment variables
export MCP_SERVER_COMMAND="npx"
export MCP_SERVER_ARGS="-y @modelcontextprotocol/server-filesystem /tmp/mcp_workspace"

echo "MCP server setup complete"
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
            ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp/test"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"MCP server test result: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"MCP server test failed: {e}")
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
npm install -g @modelcontextprotocol/server-filesystem  # For filesystem server
pip install mcp-server-database                         # For database server
docker pull mcp-server-image:latest                     # For Docker-based server
```

### **Agent Dependencies**
Each MCP agent must have its own `requirements.txt` file:

```txt
# src/mcp_agent/requirements.txt
# MCP-specific dependencies
mcp-client>=1.0.0
mcp-server-utils>=1.0.0

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
