[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

# 🚀 SAM Agentic Component Builder

**A comprehensive framework for building and deploying AI agents in Solace Agent Mesh (SAM) using CURSOR**

## 📋 Overview

The **SAM Agentic Component Builder** is an open-source framework that simplifies the development, testing, and deployment of AI agents within the Solace Agent Mesh (SAM) ecosystem. This project provides standardized patterns, tools, and templates for creating both **custom Python agents** and **YAML-only MCP (Model Context Protocol) agents**.

### 🎯 Purpose

- **Accelerate Agent Development**: Provide ready-to-use templates and patterns for SAM agent development
- **Standardize Agent Architecture**: Establish consistent patterns for agent structure, testing, and deployment
- **Simplify MCP Integration**: Enable seamless integration of external MCP servers with minimal configuration
- **Reduce Development Time**: Eliminate boilerplate code and provide comprehensive tooling

## 🏗️ Architecture

### **Project Structure**
```
sam-agentic-component-builder/
├── agents/
│   ├── custom-agents/           # Custom Python agents with full control
│   │   ├── find_my_ip_agent/    # Example custom agent
│   │   ├── deploy_custom_agent.py
│   │   ├── undeploy_custom_agent.py
│   │   └── verify_custom_agent.py
│   └── mcp-agents/              # YAML-only MCP agents
│       ├── configs/agents/      # Agent configurations
│       ├── src/                 # Test structure
│       ├── deploy_mcp_agent.py
│       ├── undeploy_mcp_agent.py
│       └── verify_mcp_agent.py
├── .gitignore                   # Comprehensive Git ignore rules
└── README.md                    # This file
```

### **Agent Types**

#### **1. Custom Python Agents** (`agents/custom-agents/`)
- **Full Control**: Complete Python implementation with custom logic
- **Custom Tools**: Define your own tools and capabilities
- **Complex Workflows**: Handle sophisticated business logic
- **Use Cases**: Data processing, API integrations, custom algorithms

#### **2. YAML-Only MCP Agents** (`agents/mcp-agents/`)
- **Minimal Configuration**: Only YAML files required
- **MCP Integration**: Connect to external MCP servers seamlessly
- **Rapid Development**: Deploy agents in minutes, not hours
- **Use Cases**: File system access, system operations, external API integration

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Node.js and NPM (for MCP agents)
- Solace Agent Mesh (SAM) installation
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/solacecommunity/sam-agentic-component-builder.git
cd sam-agentic-component-builder
```

### **2. Deploy a pre-built Agent**

#### **Option A: Deploy a Custom Python Agent**
```bash
# Navigate to custom agents
cd agents/custom-agents

# Deploy an example agent
python deploy_custom_agent.py /path/to/sam find_my_ip_agent

# Verify deployment
python verify_custom_agent.py /path/to/sam find_my_ip_agent
```

#### **Option B: Deploy a YAML-Only MCP Agent**
```bash
# Navigate to MCP agents
cd agents/mcp-agents

# Deploy a filesystem MCP agent
python deploy_mcp_agent.py /path/to/sam filesystem_mcp_agent

# Verify deployment
python verify_mcp_agent.py /path/to/sam filesystem_mcp_agent
```

### **3. Start SAM and Interact with Your Agent**
```bash
# Start SAM with your deployed agents
./start_sam.sh

# SAM will start and load all deployed agents
# You'll see the SAM chat interface in your browser
```

### **4. Chat with Your Agent**
Once SAM is running:
1. **Open your browser** to the SAM chat interface (usually `http://localhost:8080`)
2. **Review Agents** from the Agents list, check your deployed agent's reference card
3. **Start chatting** with your agent using natural language with an appropriate query and watch the visualizer shwoign invocation of agent tools
4. **Test agent capabilities** by asking questions or requesting actions

**Example interactions:**
```
# For Find My IP Agent
"What's my current IP address?"
"Show me my IP location information"

# For Filesystem MCP Agent  
"List the files in the current directory"
"Create a new file called test.txt with the content 'Hello World'"
"Read the contents of config.yaml"
```

## 🛠️ Building Your Own Agent

This framework is **optimized for agentic coding tools like Cursor** and provides two streamlined approaches for building agents:

### **Step 1: Choose Your Agent Type**
- **Custom Python Agents** (`agents/custom-agents/`): Full control with custom Python logic
- **YAML-Only MCP Agents** (`agents/mcp-agents/`): Minimal configuration with MCP server integration

### **Step 2: Choose Your Build Method**

In general, you can build an agent in **2 ways**:

#### **Option A: Instructions-Guided Build**
1. **Navigate to your chosen agent type directory**
   ```bash
   # For custom agents
   cd agents/custom-agents
   
   # For MCP agents  
   cd agents/mcp-agents
   ```

2. **Let the `instructions.mdc` in the agent type folder lead the way**
   - Review the comprehensive development guidelines that the coding agent will follow
   - Familiarize yourself with the process, patterns and best practices followed

3. **Provide a prompt describing your agent requirements and details**:
   - API endpoint details
   - Documentation and specifications
   - Agent capabilities and use cases
   - Other relevant instructions

4. **Let Cursor build the agent** following the framework's established patterns

#### **Option B: Template-Based Build**
1. **Navigate to your chosen agent type directory**
   ```bash
   # For custom agents
   cd agents/custom-agents
   
   # For MCP agents
   cd agents/mcp-agents
   ```

2. **Build a prompt for your agent based on the prompt template** in that folder:
   - **Custom Agents**: `custom-agent-builder-prompt-sample.md`
   - **MCP Agents**: `custom-mcp-builder-prompt-sample.md`

3. **Fill in the template** with your specific agent requirements or **Prompt** your way to create a new agent prompt based on the template
4. **Use the built prompt to build the agent**

### **Example: Building with Cursor**
```bash
# 1. Choose agent type
cd agents/mcp-agents

# 2. Use the prompt template
# Open custom-mcp-builder-prompt-sample.md and fill in your requirements

# 3. Let Cursor generate the agent
# Provide the filled template to Cursor for agent generation

# 4. Deploy your new agent
python deploy_mcp_agent.py /path/to/sam your_new_agent
```

## 📚 Documentation

### **Framework Guidelines**
- **[Custom Agents Guide](agents/custom-agents/README.md)**: Complete guide for building custom Python agents
- **[MCP Agents Guide](agents/mcp-agents/README.md)**: Guide for YAML-only MCP agent development
- **[Development Instructions](agents/mcp-agents/instructions.mdc)**: Detailed development guidelines

### **Agent Templates**
- **[Custom Agent Template](agents/custom-agents/custom-agent-builder-prompt-sample.md)**: Template for custom agent development
- **[MCP Agent Template](agents/mcp-agents/custom-mcp-builder-prompt-sample.md)**: Template for MCP agent development

### **Examples**
- **[Find My IP Agent](agents/custom-agents/find_my_ip_agent/)**: Example custom Python agent
- **[Filesystem MCP Agent](agents/mcp-agents/configs/agents/filesystem_mcp_agent.yaml)**: Example YAML-only MCP agent

## 🧪 Testing

### **Custom Agents**
```bash
cd agents/custom-agents/src/find_my_ip_agent
python -m pytest tests/ -v
```

### **MCP Agents**
```bash
cd agents/mcp-agents
python -m pytest src/*/tests/test_*_mcp_agent.py -v
```

## 🔧 Development

### **Creating a New Custom Agent**
1. Copy the custom agent template
2. Define agent requirements and capabilities
3. Implement Python logic and tools
4. Create comprehensive tests
5. Deploy and verify

### **Creating a New MCP Agent**
1. Copy the MCP agent template
2. Identify the MCP server to integrate
3. Configure YAML settings
4. Test MCP server connectivity
5. Deploy and verify

## 🛠️ Tools and Scripts

### **Deployment Scripts**
- **`deploy_custom_agent.py`**: Deploy custom Python agents
- **`deploy_mcp_agent.py`**: Deploy YAML-only MCP agents
- **`undeploy_custom_agent.py`**: Remove custom agents
- **`undeploy_mcp_agent.py`**: Remove MCP agents

### **Verification Scripts**
- **`verify_custom_agent.py`**: Verify custom agent deployments
- **`verify_mcp_agent.py`**: Verify MCP agent deployments

### **Testing Tools**
- **Comprehensive test suites** for both agent types
- **MCP server availability testing**
- **Configuration validation**
- **Integration testing**

## 🎯 Use Cases

### **Custom Python Agents**
- **Data Processing**: Transform and analyze data
- **API Integration**: Connect to external services
- **Business Logic**: Implement complex workflows
- **Custom Tools**: Create specialized capabilities

### **YAML-Only MCP Agents**
- **File System Access**: Read, write, and manage files
- **System Operations**: Execute system commands
- **External APIs**: Connect to web services via MCP
- **Database Operations**: Query and manipulate data

## 🔒 Security

- **Comprehensive `.gitignore`**: Protects sensitive data and credentials
- **Environment Variable Management**: Secure configuration handling
- **Credential Protection**: Excludes API keys and tokens from version control
- **Deployment Verification**: Ensures secure agent deployment

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Follow the development guidelines**
4. **Add comprehensive tests**
5. **Submit a pull request**

### **Development Guidelines**
- Follow the established patterns and templates
- Add comprehensive documentation
- Include tests for all new functionality
- Use the provided verification scripts
- Follow the code of conduct

## 📊 Project Status

### **✅ Completed Features**
- Custom Python agent framework
- YAML-only MCP agent framework
- Comprehensive deployment scripts
- Verification and testing tools
- Documentation and templates

### **🔄 In Progress**
- Additional MCP server integrations
- Enhanced testing frameworks
- Performance optimizations

### **📋 Planned Features**
- More MCP server integrations
- Advanced deployment options
- Monitoring and observability
- Community agent marketplace

## 🆘 Support

### **Community Resources**
- **[Solace Community](https://solace.community)**: Ask questions and get help
- **[Solace Developer Portal](https://solace.dev)**: Official documentation
- **[GitHub Issues](https://github.com/solacecommunity/sam-agentic-component-builder/issues)**: Report bugs and request features

### **Getting Help**
1. Check the documentation in this repository
2. Review existing issues and discussions
3. Ask questions in the Solace Community
4. Create a new issue for bugs or feature requests

## 📄 License

This project is licensed under the [LICENSE](LICENSE) file. See the file for details.

## ⚠️ Disclaimer

This is **not an officially supported Solace product**. It is a community-driven project that provides tools and patterns for building agents in the Solace Agent Mesh ecosystem.

## 🙏 Acknowledgments

- **Solace Labs** for the Solace Agent Mesh framework
- **Model Context Protocol** community for MCP standards
- **Contributors** who have helped build and improve this framework

---

**Ready to build your first SAM agent?** Start with the [Quick Start Guide](#-quick-start) above!
