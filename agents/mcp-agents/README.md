# 🚀 MCP Agents for Solace Agent Mesh (SAM)

This directory contains **YAML-only MCP agents** for **Solace Agent Mesh (SAM)** - demonstrating the minimal approach to MCP integration using SAM's built-in runner.

## **🎯 Key Insight: YAML-Only MCP Agents**

**For basic MCP integration in SAM, only YAML configuration is required** - no custom source code needed!

- ✅ **SAM built-in runner** handles MCP handshake automatically
- ✅ **No custom Python code** required for basic MCP integration  
- ✅ **Custom code only needed** for post-processing/validation or mixing MCP + Python tools

## **📁 Directory Structure**

```
agents/mcp-agents/
├── instructions.mdc                           # Framework guidelines
├── custom-mcp-builder-prompt-sample.md        # Generic template
├── text-mcp-agent-builder-prompt.md           # Text MCP Agent prompt
├── deploy_mcp_agent.py                        # MCP agent deployment script
├── undeploy_mcp_agent.py                      # MCP agent undeployment script
├── verify_mcp_agent.py                        # MCP agent verification script
├── configs/
│   ├── shared_config.yaml                     # Shared configuration
│   └── agents/
│       ├── text_mcp_agent.yaml                # Text MCP Agent (YAML-only)
│       ├── filesystem_mcp_agent.yaml          # Filesystem MCP Agent (YAML-only)
│       └── system_mcp_agent.yaml              # System MCP Agent (YAML-only)
├── src/                                       # Test structure (following convention)
│   ├── text_mcp_agent/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_text_mcp_agent.py         # Text MCP Agent tests
│   │   ├── requirements.txt                   # Test dependencies
│   │   └── run_tests.sh                       # Test runner script
│   ├── filesystem_mcp_agent/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_filesystem_mcp_agent.py   # Filesystem MCP Agent tests
│   │   └── requirements.txt                   # Test dependencies
│   └── system_mcp_agent/
│       ├── tests/
│       │   ├── __init__.py
│       │   └── test_system_mcp_agent.py       # System MCP Agent tests
│       └── requirements.txt                   # Test dependencies
├── run_all_mcp_tests.py                       # Master test runner
├── .gitignore                                 # Git ignore file for MCP agents
└── README.md                                  # This file
```

**Note**: While the agents themselves are YAML-only, we maintain a test structure following the established convention for validation and quality assurance.

## **🤖 Available MCP Agents**

### **📝 Text MCP Agent**
**Purpose**: Text processing, search, and manipulation capabilities
**MCP Server**: `@modelcontextprotocol/server-text`
**Configuration**: `configs/agents/text_mcp_agent.yaml`

**Capabilities**:
- Read and write text files
- Search for text patterns using regex
- Replace text patterns with new content
- Split text by delimiters
- Join text parts with delimiters
- Extract text using patterns
- Analyze text for statistics and sentiment

### **📁 Filesystem MCP Agent**
**Purpose**: File system access and management capabilities
**MCP Server**: `@modelcontextprotocol/server-filesystem`
**Configuration**: `configs/agents/filesystem_mcp_agent.yaml`

**Capabilities**:
- Read file contents
- Write content to files
- List directory contents
- Create directories
- Delete files and directories
- Navigate file system
- Check file and directory properties

### **⚙️ System MCP Agent**
**Purpose**: System information and process management capabilities
**MCP Server**: `@modelcontextprotocol/server-system`
**Configuration**: `configs/agents/system_mcp_agent.yaml`

**Capabilities**:
- Get system information (OS, architecture, etc.)
- List running processes
- Execute system commands
- Monitor system resources
- Get environment variables
- Check system status
- Manage system operations

## **🚀 Quick Start**

### **1. Prerequisites**
- Node.js and NPM installed
- SAM installation configured
- MCP servers available (installed via NPM)

### **2. Install MCP Servers**
```bash
# Install required MCP servers
npm install -g @modelcontextprotocol/server-text
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-system
```

### **3. Deploy an MCP Agent**
```bash
# Deploy with interactive selection
python deploy_mcp_agent.py /path/to/sam

# Deploy specific MCP agent
python deploy_mcp_agent.py /path/to/sam text_mcp_agent

# List available MCP agents
python deploy_mcp_agent.py /path/to/sam --list
```

### **4. Run the Deployed Agent**
```bash
# Use the generated run script
./start_mcp_agent.sh

# Or run manually
cd /path/to/sam
sam run configs/agents/text_mcp_agent.yaml
```

### **5. Undeploy an MCP Agent**
```bash
# Undeploy with interactive selection
python undeploy_mcp_agent.py /path/to/sam

# Undeploy specific MCP agent
python undeploy_mcp_agent.py /path/to/sam text_mcp_agent

# List deployed MCP agents
python undeploy_mcp_agent.py /path/to/sam --list
```

### **6. Verify MCP Agent Deployment**
```bash
# Verify with interactive selection
python verify_mcp_agent.py /path/to/sam

# Verify specific MCP agent
python verify_mcp_agent.py /path/to/sam filesystem_mcp_agent

# Show help and usage
python verify_mcp_agent.py --help
```

The verification script checks:
- ✅ Agent configuration files are in place
- ✅ Shared configuration is properly set up
- ✅ MCP server availability and connectivity
- ✅ SAM environment readiness
- ✅ Deployment information and start scripts

### **7. Test the Agent**
```bash
# Test with natural language queries
"Read the contents of test.txt"
"Search for the word 'hello' in this text"
"Create a new file called hello.txt with the content 'Hello World'"
```

## **📋 Minimal YAML Configuration**

### **Basic Structure**
```yaml
# configs/agents/example_agent.yaml
!include ../shared_config.yaml

apps:
  - name: example_mcp_agent_app
    app_module: solace_agent_mesh.agent.sac.app   # built-in runner
    app_base_path: .
    broker: { <<: *broker_connection }
    app_config:
      agent_name: "ExampleAgent"
      supports_streaming: true
      model: *general_model
      tools:
        - tool_type: mcp
          connection_params:
            type: stdio
            command: "npx"
            args: ["-y", "@modelcontextprotocol/server-example"]
      agent_card: { description: "MCP example agent" }
```

### **Key Components**
- **`app_module: solace_agent_mesh.agent.sac.app`**: SAM's built-in runner
- **`tool_type: mcp`**: MCP tool integration
- **`connection_params`**: MCP server connection details
- **`agent_card`**: Agent discovery and capabilities

## **🔧 MCP Server Connection Types**

### **1. Stdio Connection (Local)**
```yaml
tools:
  - tool_type: mcp
    connection_params:
      type: stdio
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp/samv2"]
```

### **2. SSE Connection (Remote)**
```yaml
tools:
  - tool_type: mcp
    connection_params:
      type: sse
      url: "https://mcp.example.com/v1/sse"
      headers:
        Authorization: "Bearer ${MCP_AUTH_TOKEN}"
```

### **3. Docker Connection**
```yaml
tools:
  - tool_type: mcp
    connection_params:
      type: stdio
      command: "docker"
      args: ["run", "-i", "--rm", "mcp-server-image:latest"]
```

## **📚 Documentation**

### **Framework Guidelines**
- **`instructions.mdc`**: Complete MCP agent development guidelines
- **`custom-mcp-builder-prompt-sample.md`**: Template for creating new MCP agents

### **Agent-Specific Prompts**
- **`text-mcp-agent-builder-prompt.md`**: Text MCP Agent specifications
- Additional prompts for other MCP agents

### **Deployment Scripts**
- **`deploy_mcp_agent.py`**: Deploy MCP agents to SAM installation
- **`undeploy_mcp_agent.py`**: Remove MCP agents from SAM installation
- **`verify_mcp_agent.py`**: Verify MCP agent deployment and environment
- **`start_mcp_agent.sh`**: Generated run script for deployed agents

## **🔄 Recent Improvements**

### **Testing Framework Enhancements**
- **Optimized Test Structure**: Eliminated repetitive `!include` handling code across all test files
- **Helper Method Pattern**: Created `load_config_with_includes()` helper method for consistent YAML parsing
- **Comprehensive Test Coverage**: Updated tests to validate YAML syntax, agent configuration, MCP server availability, and shared config integration
- **Test Dependencies**: Standardized test dependencies with `pytest`, `PyYAML`, and `solace-agent-mesh`

### **Verification Script**
- **`verify_mcp_agent.py`**: New comprehensive verification script for MCP agent deployments
- **Multi-Level Verification**: Checks agent configuration, shared configuration, MCP server availability, and SAM environment
- **Interactive Usage**: Supports both interactive and command-line usage with help documentation
- **Detailed Reporting**: Provides clear success/failure indicators and next steps

### **Documentation Updates**
- **Updated `instructions.mdc`**: Enhanced testing strategy section with YAML-only MCP agent focus
- **Updated Prompt Template**: Refined testing requirements and development workflow
- **Enhanced README**: Added verification script documentation and usage examples
- **Test Examples**: Provided comprehensive test implementation examples

### **Code Quality Improvements**
- **DRY Principle**: Eliminated code duplication in test files
- **Consistent Patterns**: Standardized test structure across all MCP agents
- **Error Handling**: Improved YAML parsing with proper error handling for `!include` directives
- **Maintainability**: Made tests easier to maintain and extend

### **Git Configuration**
- **`.gitignore`**: Comprehensive Git ignore file for MCP agents project
- **Security**: Excludes sensitive files, credentials, and temporary artifacts
- **Development**: Ignores IDE files, OS-specific files, and build artifacts
- **Testing**: Excludes test outputs, coverage reports, and cache files

## **🧪 Testing MCP Agents**

### **Test Structure**
Tests follow the established convention: `src/<agent_name>/tests/test_<agent_name>.py`

### **What We Test**
For **YAML-only MCP agents**, we test:

1. **YAML Configuration Syntax** - Valid YAML structure and syntax
2. **Agent Configuration Structure** - Required fields and proper configuration
3. **MCP Server Availability** - MCP server installation and startup
4. **Agent Instructions** - Proper instruction content and capabilities
5. **Agent Card Configuration** - Skills, input/output modes, and descriptions
6. **Shared Config Integration** - Proper inclusion of shared configuration

### **What We DON'T Test**
- Custom Python logic (none exists in YAML-only agents)
- Tool implementation (handled by MCP servers)
- Error handling logic (handled by SAM and MCP servers)
- State management (handled by SAM built-in runner)

### **Running Tests**

#### Individual Agent Tests
```bash
# Run tests for a specific agent
cd src/text_mcp_agent
python -m pytest tests/test_text_mcp_agent.py -v

### **Test Dependencies**
Install test dependencies for each agent:
```bash
cd src/<agent_name>
pip install -r requirements.txt
```

### **Manual Testing**
```bash
# Test MCP Server Availability
npx -y @modelcontextprotocol/server-text

# Test Filesystem MCP Server
npx -y @modelcontextprotocol/server-filesystem /tmp/test

# Test System MCP Server
npx -y @modelcontextprotocol/server-system

# Validate YAML syntax
yamllint configs/agents/text_mcp_agent.yaml

# Test agent startup
sam run configs/agents/text_mcp_agent.yaml --dry-run
```

## **🚀 Deployment for MCP Agents**

### **What Constitutes Deployment**

For **YAML-only MCP agents**, deployment consists of:

1. **YAML Configuration Files**
   - Agent configuration file (`<agent_name>.yaml`)
   - Shared configuration file (`shared_config.yaml`)
   - Customized with the target agent name

2. **Future: Source Code Deployment**
   - When post-processing/customization is added
   - `src/` folder contents will be deployed
   - Custom Python logic and tools

3. **Deployment Artifacts**
   - Configuration files copied to SAM installation
   - Agent name customization applied
   - Deployment info file created
   - Run script generated

### **Deployment Process**

```bash
# 1. Verify MCP server availability
python deploy_mcp_agent.py /path/to/sam text_mcp_agent

# 2. Deploy YAML configurations
# - Copies agent config to SAM configs/agents/
# - Copies shared config to SAM configs/
# - Customizes agent names and references

# 3. Generate run script
# - Creates start_mcp_agent.sh for easy execution

# 4. Verify deployment
# - Check deployment info file
# - Test agent startup
```

### **Undeployment Process**

```bash
# 1. Remove agent configuration
python undeploy_mcp_agent.py /path/to/sam text_mcp_agent

# 2. Clean up artifacts
# - Removes agent config file
# - Removes deployment info
# - Optionally removes shared config (if not used by other agents)

# 3. Future: Remove source code
# - When src/ folder deployment is added
```

## **🔑 Environment Variables**
```bash
# SAM Configuration
SOLACE_BROKER_URL=ws://localhost:8080
SOLACE_BROKER_USERNAME=default
SOLACE_BROKER_PASSWORD=default
SOLACE_BROKER_VPN=default

# LLM Configuration
LLM_SERVICE_ENDPOINT=https://api.openai.com/v1
LLM_SERVICE_GENERAL_MODEL_NAME=gpt-4
LLM_SERVICE_API_KEY=your_api_key_here
```

### **Optional Environment Variables**
```bash
# Development Mode
SOLACE_DEV_MODE=false
USE_TEMPORARY_QUEUES=true

# MCP Server Configuration
MCP_WORKING_DIR=/tmp/text_workspace
MCP_DEBUG_MODE=false
```

## **🚨 When to Add Custom Code**

### **Add Custom Python Code When**:
- **Post-processing MCP outputs** with custom logic
- **Mixing MCP + Python tools** in the same agent
- **Custom validation** of MCP tool results
- **Advanced error handling** beyond MCP defaults
- **Custom lifecycle management** (initialization, cleanup)
- **Integration with other services** beyond MCP

### **Stick with YAML-Only When**:
- **Basic MCP integration** is sufficient
- **No custom logic** needed beyond MCP tools
- **Standard MCP server** functionality meets requirements
- **Simple agent behavior** without complex workflows

## **📈 Best Practices**

### **MCP Agent Development**
1. **Start with YAML-only** - Use minimal configuration first
2. **Test MCP server** independently before integration
3. **Use clear agent instructions** for better user experience
4. **Document agent capabilities** in agent_card skills
5. **Handle errors gracefully** with informative messages

### **Configuration Management**
1. **Use shared_config.yaml** for common settings
2. **Reference environment variables** for sensitive data
3. **Keep configurations minimal** and focused
4. **Document all configuration options**
5. **Version control configurations** properly

## **🤝 Contributing**

### **Adding New MCP Agents**
1. **Create agent builder prompt** using the template
2. **Create YAML configuration** following the pattern
3. **Test MCP server** availability and functionality
4. **Update documentation** with agent details
5. **Add to this README** with capabilities and usage

### **Development Workflow**
1. **Plan agent requirements** using builder prompt
2. **Create YAML configuration** with MCP integration
3. **Test agent functionality** in SAM environment
4. **Document agent capabilities** and usage
5. **Deploy and monitor** agent performance

---

## **📞 Support & Resources**

### **SAM Documentation**
- **Primary Documentation**: https://solacelabs.github.io/solace-agent-mesh/docs/documentation/
- **MCP Integration**: https://solacelabs.github.io/solace-agent-mesh/docs/documentation/tutorials/mcp-integration

### **MCP Resources**
- **MCP Protocol**: https://modelcontextprotocol.io/
- **MCP Servers**: https://github.com/modelcontextprotocol/servers
- **MCP Documentation**: https://modelcontextprotocol.io/docs

### **Example MCP Servers**
- **Filesystem**: https://github.com/modelcontextprotocol/server-filesystem
- **Text**: https://github.com/modelcontextprotocol/server-text
- **System**: https://github.com/modelcontextprotocol/server-system

---

*This framework demonstrates the power of YAML-only MCP agents in SAM, enabling rapid development and deployment of MCP-enabled agents with minimal configuration.*
