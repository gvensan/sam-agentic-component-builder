# Generic Agent Deployment Guide

This guide explains how the `deploy_agent.py` script works as a **generic deployment tool** for any agent in this workspace.

## 🎯 What the Script Does

### **Purpose**
The `deploy_agent.py` script is a **generic deployment tool** that can deploy any agent from this workspace to a SAM installation. It's not limited to just the IP agent - it can handle any agent you create.

### **Key Features**
1. **Generic**: Works with any agent, not just IP agents
2. **Auto-detection**: Automatically finds agent source code
3. **Dynamic customization**: Replaces agent-specific references
4. **Flexible naming**: Supports custom agent names
5. **Smart configuration**: Updates config files automatically

## 🔍 How It Works

### **1. Source Detection**
```bash
# The script looks in src/ directory for agent code
src/
├── find_my_ip_agent/          # IP Agent
├── weather_agent/             # Weather Agent (example)
├── stock_agent/               # Stock Agent (example)
└── any_other_agent/           # Any other agent
```

### **2. Auto-Discovery**
- **Single agent**: If only one agent exists, it's auto-detected
- **Multiple agents**: You're prompted to choose which one
- **Custom source**: You can specify the source directory manually

### **3. Dynamic Customization**
The script automatically:
- Replaces agent names in configuration files
- Updates lifecycle function names
- Customizes directory structures
- Generates agent-specific run scripts

## 🚀 Usage Examples

### **Example 1: List Available Agents**
```bash
# List all available agents for deployment
python deploy_agent.py /opt/sam --list
```

### **Example 2: Interactive Agent Selection**
```bash
# Deploy with interactive agent selection
python deploy_agent.py /opt/sam
# This will show a list of available agents and let you choose
```

### **Example 3: Deploy Specific Agent**
```bash
# Deploy IP agent with custom name
python deploy_agent.py /opt/sam my-ip-agent

# Deploy with explicit source directory
python deploy_agent.py /opt/sam my-ip-agent find_my_ip_agent
```

### **Example 4: Deploy Weather Agent**
```bash
# Deploy weather agent
python deploy_agent.py /opt/sam my-weather-agent weather_trend_agent
```

### **Example 5: Deploy Any Agent**
```bash
# Generic deployment for any agent
python deploy_agent.py /opt/sam my-custom-agent custom_agent_name
```

## 🗑️ Undeployment Examples

### **Example 1: List Deployed Agents**
```bash
# List all deployed agents in SAM
python undeploy_agent.py /opt/sam --list
```

### **Example 2: Interactive Undeployment**
```bash
# Undeploy with interactive agent selection
python undeploy_agent.py /opt/sam
# This will show a list of deployed agents and let you choose
```

### **Example 3: Undeploy Specific Agent**
```bash
# Undeploy IP agent
python undeploy_agent.py /opt/sam my-ip-agent

# Undeploy weather agent
python undeploy_agent.py /opt/sam my-weather-service
```

### **Example 4: Undeploy Multiple Agents**
```bash
# Undeploy agents one by one
python undeploy_agent.py /opt/sam my-ip-agent
python undeploy_agent.py /opt/sam my-weather-service
python undeploy_agent.py /opt/sam country-info-agent
```

## 📁 Expected Workspace Structure

```
workspace/
├── src/
│   ├── find_my_ip_agent/          # IP Agent source
│   │   ├── __init__.py
│   │   ├── tools.py
│   │   ├── lifecycle.py
│   │   └── services/
│   ├── weather_agent/             # Weather Agent source
│   │   ├── __init__.py
│   │   ├── tools.py
│   │   └── lifecycle.py
│   └── any_other_agent/           # Any other agent
├── configs/
│   ├── agents/
│   │   ├── find_my_ip_agent.yaml  # IP Agent config
│   │   ├── weather_agent.yaml     # Weather Agent config
│   │   └── any_other_agent.yaml   # Any other agent config
│   └── shared_config.yaml
├── requirements.txt
├── deploy_agent.py               # Generic deployment script
└── verify_deployment.py           # Generic verification script
```

## 🔧 Command-Line Arguments

### **deploy_agent.py**
```bash
# List available agents
python deploy_agent.py <sam_path> --list

# Interactive agent selection
python deploy_agent.py <sam_path>

# Deploy specific agent
python deploy_agent.py <sam_path> [agent_name] [source_dir]

# Arguments:
#   sam_path     - Path to SAM installation (required)
#   agent_name   - Name for the deployed agent (optional, interactive selection)
#   source_dir   - Source directory name (optional, auto-detected)
```

### **Interactive Features**
The deploy script now supports interactive agent selection:

1. **List Available Agents**: `--list` flag shows all available agents with validation status
2. **Interactive Selection**: Run without agent name to choose from a numbered list
3. **Validation**: Checks for required files (__init__.py, tools.py, lifecycle.py)
4. **Error Handling**: Robust input validation and error messages
5. **Cancel Option**: Option 0 allows cancelling the deployment

### **undeploy_agent.py**
```bash
# List deployed agents
python undeploy_agent.py <sam_path> --list

# Interactive agent selection for undeployment
python undeploy_agent.py <sam_path>

# Undeploy specific agent
python undeploy_agent.py <sam_path> [agent_name]

# Arguments:
#   sam_path     - Path to SAM installation (required)
#   agent_name   - Name of the deployed agent to remove (optional, interactive selection)
```

### **Interactive Undeployment Features**
The undeploy script supports interactive agent selection:

1. **List Deployed Agents**: `--list` flag shows all deployed agents with status
2. **Interactive Selection**: Run without agent name to choose from a numbered list
3. **Status Information**: Shows source and config file status for each agent
4. **Confirmation**: Requires user confirmation before removing agents
5. **Shared Config Management**: Intelligently handles shared configuration files

### **verify_agent.py**
```bash
python verify_agent.py <sam_path> [agent_name] [source_dir]

# Arguments:
#   sam_path     - Path to SAM installation (required)
#   agent_name   - Name of the deployed agent (optional)
#   source_dir   - Original source directory name (optional)
```

## ⚙️ Configuration

### **Environment Variables**
The scripts support configuration via environment variables:

```bash
# Set SAM installation path
export SAM_PATH=/path/to/your/sam/installation

# Set default agent name
export AGENT_NAME=my-custom-agent

# Use with scripts
./start_agent.sh
python deploy_agent.py /path/to/sam my-agent
```

### **Configuration File (.env)**
Create a `.env` file in the project directory for persistent configuration:

```bash
# Copy the example configuration
cp env.example .env

# Edit the configuration
nano .env
```

Example `.env` file:
```bash
# SAM Installation Path
SAM_PATH=/path/to/your/sam/installation

# Default Agent Name
AGENT_NAME=find_my_ip_agent
```

### **Auto-Detection**
The `start_agent.sh` script automatically searches for SAM installations in common locations:
- `$HOME/sam/v1`
- `$HOME/.sam`
- `/opt/sam`
- `/usr/local/sam`

## 🎨 Customization Examples

### **IP Agent Deployment**
```bash
# Original: find_my_ip_agent
# Deployed as: my-ip-agent
python deploy_agent.py /opt/sam my-ip-agent find_my_ip_agent

# Results in:
# - Config: my-ip-agent.yaml
# - Functions: initialize_my_ip_agent, cleanup_my_ip_agent
# - Directory: /opt/sam/agents/my-ip-agent/
```

### **Weather Agent Deployment**
```bash
# Original: weather_agent
# Deployed as: my-weather-service
python deploy_agent.py /opt/sam my-weather-service weather_agent

# Results in:
# - Config: my-weather-service.yaml
# - Functions: initialize_my_weather_service, cleanup_my_weather_service
# - Directory: /opt/sam/agents/my-weather-service/
```

### **Stock Agent Deployment**
```bash
# Original: stock_agent
# Deployed as: stock-tracker
python deploy_agent.py /opt/sam stock-tracker stock_agent

# Results in:
# - Config: stock-tracker.yaml
# - Functions: initialize_stock_tracker, cleanup_stock_tracker
# - Directory: /opt/sam/agents/stock-tracker/
```

## 🔄 What Gets Customized

### **1. Configuration Files**
```yaml
# Original: find_my_ip_agent.yaml
agent_name: "FindMyIPAgent"
display_name: "Find My IP Agent"

# Deployed as: my-ip-agent.yaml
agent_name: "MyIpAgent"
display_name: "my-ip-agent"
```

### **2. Lifecycle Functions**
```python
# Original: lifecycle.py
def initialize_find_my_ip_agent(host_component):
    pass

def cleanup_find_my_ip_agent(host_component):
    pass

# Deployed as: lifecycle.py
def initialize_my_ip_agent(host_component):
    pass

def cleanup_my_ip_agent(host_component):
    pass
```

### **3. Run Scripts**
```bash
# Generated: start_agent.sh
AGENT_CONFIG="$SAM_PATH/configs/agents/my-ip-agent.yaml"
echo "🚀 Starting my-ip-agent with SAM..."
```

## 📦 Dependency Management

### **Agent-Specific Dependencies**
Each agent now has its own `requirements.txt` file with specific dependencies:

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
pip install -r src/my-ip-agent/requirements.txt
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

## ✅ Verification

### **Generic Verification**
```bash
# Verify any agent deployment
python verify_deployment.py /opt/sam my-ip-agent find_my_ip_agent
python verify_deployment.py /opt/sam my-weather-service weather_agent
python verify_deployment.py /opt/sam stock-tracker stock_agent
```

### **What Gets Verified**
- ✅ Agent source code deployment
- ✅ Configuration file customization
- ✅ Lifecycle function customization
- ✅ Requirements file presence
- ✅ Deployment info creation
- ✅ SAM environment setup
- ✅ Agent-specific dependencies availability

## 🗑️ What Gets Removed During Undeployment

### **Agent Files Removed**
When you undeploy an agent, the following files and directories are removed:

```bash
# Agent source code directory
/opt/sam/src/my-ip-agent/          # Complete agent directory
├── __init__.py
├── tools.py
├── lifecycle.py
├── requirements.txt
├── services/
├── tests/
├── README.md
└── API_REFERENCE.md

# Agent configuration file
/opt/sam/configs/agents/my-ip-agent.yaml
```

### **Shared Configuration Handling**
The undeploy script intelligently manages shared configuration files:

```bash
# If shared_config.yaml is used by other agents
/opt/sam/configs/shared_config.yaml  # KEPT (other agents depend on it)

# If shared_config.yaml is not used by any other agents
/opt/sam/configs/shared_config.yaml  # REMOVED (with user confirmation)
```

### **Confirmation Process**
The undeploy script requires confirmation before removing files:

```bash
Do you want to remove agent 'my-ip-agent'? (y/N): y
🗑️  Removing agent 'my-ip-agent'...
✅ Removed agent directory: /opt/sam/src/my-ip-agent
✅ Removed config file: /opt/sam/configs/agents/my-ip-agent.yaml
```

## 🎯 Benefits of Generic Design

### **1. Reusability**
- Same script works for any agent
- No need to create agent-specific deployment scripts
- Consistent deployment process

### **2. Flexibility**
- Support any naming convention
- Handle different agent types
- Customize deployment as needed

### **3. Maintainability**
- Single script to maintain
- Consistent behavior across agents
- Easy to extend and improve

### **4. Automation**
- Auto-detection of agent source
- Automatic customization
- Reduced manual configuration

## 🧪 Post-Deployment Testing

### **Testing Strategy**
After deployment and dependency installation, test your agent:

```bash
# 1. Navigate to agent directory
cd /opt/sam/src/my-ip-agent

# 2. Run API tests (test external APIs directly)
python tests/test_my_ip_agent_api.py

# 3. Run unit tests (test agent logic with mocked dependencies)
python -m pytest tests/test_my_ip_agent.py -v --asyncio-mode=auto

# 4. Test in SAM runtime
cd /opt/sam
sam run configs/agents/my-ip-agent.yaml
```

## 🔄 Undeployment Workflow

### **Pre-Undeployment Checklist**
Before undeploying an agent, consider the following:

1. **Backup Important Data**: If the agent has generated any important data
2. **Check Dependencies**: Ensure no other agents depend on this agent
3. **Verify Configuration**: Check if shared configurations are used by other agents
4. **Test Alternative**: Deploy a replacement agent if needed

### **Undeployment Process**
```bash
# 1. List deployed agents
python undeploy_agent.py /opt/sam --list

# 2. Choose agent to undeploy (interactive or direct)
python undeploy_agent.py /opt/sam my-ip-agent

# 3. Confirm removal when prompted
Do you want to remove agent 'my-ip-agent'? (y/N): y

# 4. Verify removal
python undeploy_agent.py /opt/sam --list
```

### **Post-Undeployment Verification**
After undeploying, verify the removal was successful:

```bash
# Check agent directory is removed
ls /opt/sam/src/ | grep my-ip-agent

# Check config file is removed
ls /opt/sam/configs/agents/ | grep my-ip-agent

# Verify SAM still works with other agents
sam run configs/agents/other-agent.yaml
```

### **Test Coverage**
Each agent should have comprehensive test coverage:
- **API Tests**: Test external APIs directly
- **Unit Tests**: Test agent logic with mocked dependencies
- **Integration Tests**: Test agent in SAM environment
- **Error Handling**: Test error cases and edge cases

### **Common Test Commands**
```bash
# Weather Trend Agent
cd src/weather_trend_agent
python tests/test_weather_api.py
python -m pytest tests/test_weather_agent.py -v --asyncio-mode=auto

# Find My IP Agent
cd src/find_my_ip_agent
python tests/test_find_my_ip_api.py
python -m pytest tests/test_find_my_ip_agent.py -v --asyncio-mode=auto

# Country Information Agent
cd src/country_information_agent
python tests/test_country_information_api.py
python -m pytest tests/test_country_agent.py -v --asyncio-mode=auto

# News Snapshot Agent
cd src/news_snapshot_agent
python tests/test_news_snapshot_api.py
python -m pytest tests/test_news_agent.py -v --asyncio-mode=auto
```

## 🚀 Creating New Agents

### **Step 1: Create Agent Structure**
```bash
mkdir -p src/my_new_agent
touch src/my_new_agent/__init__.py
touch src/my_new_agent/tools.py
touch src/my_new_agent/lifecycle.py
touch src/my_new_agent/requirements.txt  # Add agent-specific dependencies
```

### **Step 2: Create Configuration**
```bash
touch configs/agents/my_new_agent.yaml
```

### **Step 3: Create Tests**
```bash
mkdir -p src/my_new_agent/tests
touch src/my_new_agent/tests/test_my_new_agent_api.py
touch src/my_new_agent/tests/test_my_new_agent.py
```

### **Step 4: Deploy**
```bash
python deploy_agent.py /opt/sam my-deployed-agent my_new_agent
```

### **Step 5: Install Dependencies and Test**
```bash
cd /opt/sam
pip install -r src/my-deployed-agent/requirements.txt
cd src/my-deployed-agent
python tests/test_my_new_agent_api.py
python -m pytest tests/test_my_new_agent.py -v --asyncio-mode=auto
```

## 🔧 Troubleshooting Undeployment Issues

### **Common Issues and Solutions**

#### **Issue 1: Agent Not Found**
```bash
❌ Agent 'my-ip-agent' not found in SAM installation
```
**Solution**: Use the `--list` flag to see available agents:
```bash
python undeploy_agent.py /opt/sam --list
```

#### **Issue 2: Permission Denied**
```bash
❌ Permission denied when removing agent files
```
**Solution**: Check file permissions and ownership:
```bash
ls -la /opt/sam/src/my-ip-agent/
sudo chown -R $USER:$USER /opt/sam/src/my-ip-agent/
```

#### **Issue 3: Shared Config Conflicts**
```bash
⚠️  No other agents found using shared config
Remove shared config file? (y/N):
```
**Solution**: Check if other agents actually use the shared config:
```bash
grep -r "shared_config.yaml" /opt/sam/configs/agents/
```

#### **Issue 4: Partial Removal**
```bash
✅ Removed agent directory: /opt/sam/src/my-ip-agent
❌ Failed to remove config file: /opt/sam/configs/agents/my-ip-agent.yaml
```
**Solution**: Manually remove the remaining files:
```bash
rm -f /opt/sam/configs/agents/my-ip-agent.yaml
```

### **Recovery Procedures**

#### **Recover from Failed Undeployment**
If undeployment fails partway through:

```bash
# 1. Check what was removed
ls -la /opt/sam/src/ | grep my-ip-agent
ls -la /opt/sam/configs/agents/ | grep my-ip-agent

# 2. Manually remove remaining files
rm -rf /opt/sam/src/my-ip-agent
rm -f /opt/sam/configs/agents/my-ip-agent.yaml

# 3. Verify cleanup
python undeploy_agent.py /opt/sam --list
```

#### **Restore Deleted Agent**
If you accidentally undeployed an agent:

```bash
# 1. Redeploy the agent
python deploy_agent.py /opt/sam my-ip-agent find_my_ip_agent

# 2. Reinstall dependencies
cd /opt/sam
pip install -r src/my-ip-agent/requirements.txt

# 3. Verify restoration
python verify_agent.py /opt/sam my-ip-agent find_my_ip_agent
```

## 📋 Summary

The `deploy_agent.py` script is a **truly generic deployment tool** that:

- ✅ Works with any agent in the workspace
- ✅ Auto-detects agent source code
- ✅ Dynamically customizes all references
- ✅ Supports flexible naming conventions
- ✅ Provides comprehensive verification
- ✅ Enables easy agent management

## 📋 Best Practices

### **Deployment Best Practices**
1. **Test Before Deploy**: Always run tests before deployment
2. **Use Descriptive Names**: Choose meaningful agent names
3. **Document Changes**: Keep track of deployed agents
4. **Version Control**: Use version control for agent source code
5. **Backup Configurations**: Backup important configurations

### **Undeployment Best Practices**
1. **Verify Dependencies**: Check if other agents depend on the one being removed
2. **Backup Data**: Backup any important data before undeployment
3. **Test After Removal**: Verify other agents still work after undeployment
4. **Clean Up Dependencies**: Remove unused dependencies if needed
5. **Document Changes**: Keep track of undeployed agents

### **Maintenance Best Practices**
1. **Regular Audits**: Periodically review deployed agents
2. **Update Dependencies**: Keep agent dependencies up to date
3. **Monitor Performance**: Track agent performance and usage
4. **Clean Up**: Remove unused or obsolete agents
5. **Documentation**: Keep deployment and configuration documentation current

**It's designed to be the one deployment tool you need for all your SAM agents!** 🎉
