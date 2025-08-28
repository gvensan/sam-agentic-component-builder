#!/usr/bin/env python3
"""
Verification script for MCP agent deployment
This script checks if the MCP agent was deployed correctly to SAM
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Any


def load_config_with_includes(config_path: Path) -> Dict[str, Any]:
    """Load YAML config file and resolve !include directives"""
    if not config_path.exists():
        return {}
    
    # Read the main config file
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Handle the !include directive by reading the shared config
    if '!include ../shared_config.yaml' in content:
        shared_config_path = config_path.parent.parent / "shared_config.yaml"
        if shared_config_path.exists():
            with open(shared_config_path, 'r') as f:
                shared_content = f.read()
            
            # Replace the include directive with the actual shared config content
            content = content.replace('!include ../shared_config.yaml', shared_content)
        else:
            # If shared config doesn't exist, comment out the include
            content = content.replace('!include ../shared_config.yaml', '# !include ../shared_config.yaml')
    
    # Parse the merged content
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError:
        return {}


def verify_deployment(sam_path: str, agent_name: str):
    """Verify that the MCP agent was deployed correctly"""
    print(f"🔍 Verifying {agent_name} MCP Agent Deployment")
    print("=" * 60)
    
    sam_path = Path(sam_path)
    
    # Define expected paths for MCP agents
    expected_paths = {
        "agent_config": sam_path / "configs" / "agents" / f"{agent_name}.yaml",
        "shared_config": sam_path / "configs" / "shared_config.yaml",
        "deployment_info": sam_path / "src" / agent_name / "deployment_info.txt",
        "start_script": sam_path / "start_mcp_agent.sh"
    }
    
    all_good = True
    
    # Check main paths
    print("📁 Checking deployment paths...")
    for name, path in expected_paths.items():
        if path.exists():
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (MISSING)")
            all_good = False
    
    # Check agent configuration
    print(f"\n🔍 Checking agent configuration...")
    config_file = expected_paths["agent_config"]
    if config_file.exists():
        config = load_config_with_includes(config_file)
        
        if config:
            # Check for required sections
            if 'apps' in config:
                print(f"✅ apps section found")
                
                # Find the MCP agent app
                app_found = False
                for app in config['apps']:
                    if app.get('name') == f"{agent_name}_app":
                        app_found = True
                        app_config = app.get('app_config', {})
                        
                        # Check required app config fields
                        required_fields = ['agent_name', 'display_name', 'model', 'tools', 'instruction']
                        for field in required_fields:
                            if field in app_config:
                                print(f"✅ {field} field present")
                            else:
                                print(f"❌ {field} field missing")
                                all_good = False
                        
                        # Check MCP tools configuration
                        tools = app_config.get('tools', [])
                        mcp_tools = [t for t in tools if t.get('tool_type') == 'mcp']
                        if mcp_tools:
                            print(f"✅ MCP tools configured ({len(mcp_tools)} tools)")
                            
                            # Check MCP tool configuration
                            mcp_tool = mcp_tools[0]
                            conn_params = mcp_tool.get('connection_params', {})
                            
                            if conn_params.get('type') == 'stdio':
                                print(f"✅ stdio connection type configured")
                            else:
                                print(f"❌ stdio connection type not configured")
                                all_good = False
                            
                            if 'command' in conn_params and 'args' in conn_params:
                                print(f"✅ MCP server command and args configured")
                            else:
                                print(f"❌ MCP server command/args missing")
                                all_good = False
                        else:
                            print(f"❌ No MCP tools configured")
                            all_good = False
                        
                        # Check agent card
                        agent_card = app_config.get('agent_card', {})
                        if agent_card:
                            print(f"✅ Agent card configured")
                            
                            required_card_fields = ['description', 'defaultInputModes', 'defaultOutputModes', 'skills']
                            for field in required_card_fields:
                                if field in agent_card:
                                    print(f"✅ agent_card.{field} present")
                                else:
                                    print(f"❌ agent_card.{field} missing")
                                    all_good = False
                        else:
                            print(f"❌ Agent card not configured")
                            all_good = False
                        
                        break
                
                if not app_found:
                    print(f"❌ {agent_name}_app not found in configuration")
                    all_good = False
            else:
                print(f"❌ apps section missing from configuration")
                all_good = False
        else:
            print(f"❌ Failed to parse agent configuration")
            all_good = False
    else:
        print(f"❌ Agent configuration file not found")
        all_good = False
    
    # Check shared configuration
    print(f"\n🔍 Checking shared configuration...")
    shared_config_file = expected_paths["shared_config"]
    if shared_config_file.exists():
        try:
            with open(shared_config_file, 'r') as f:
                shared_config = yaml.safe_load(f)
            
            if shared_config:
                # Check for required shared config sections
                required_sections = ['broker_connection', 'models', 'services']
                for section in required_sections:
                    if section in shared_config:
                        print(f"✅ {section} section present")
                    else:
                        print(f"❌ {section} section missing")
                        all_good = False
                
                # Check model configuration
                models = shared_config.get('models', {})
                if 'general' in models:
                    print(f"✅ general model configured")
                else:
                    print(f"❌ general model not configured")
                    all_good = False
                
                if 'planning' in models:
                    print(f"✅ planning model configured")
                else:
                    print(f"❌ planning model not configured")
                    all_good = False
            else:
                print(f"❌ Failed to parse shared configuration")
                all_good = False
        except yaml.YAMLError as e:
            print(f"❌ Shared configuration YAML error: {e}")
            all_good = False
    else:
        print(f"❌ Shared configuration file not found")
        all_good = False
    
    # Check deployment info
    print(f"\n📄 Checking deployment information...")
    info_file = expected_paths["deployment_info"]
    if info_file.exists():
        print(f"✅ Deployment info file exists")
        with open(info_file, 'r') as f:
            print(f"   Deployment details:")
            for line in f:
                print(f"   {line.strip()}")
    else:
        print(f"❌ Deployment info file not found")
        all_good = False
    
    # Check start script
    start_script = expected_paths["start_script"]
    if start_script.exists():
        print(f"✅ Start script exists")
        with open(start_script, 'r') as f:
            content = f.read()
            if agent_name in content:
                print(f"✅ Start script configured for {agent_name}")
            else:
                print(f"❌ Start script not configured for {agent_name}")
                all_good = False
    else:
        print(f"❌ Start script not found")
        all_good = False
    
    # Summary
    print(f"\n" + "=" * 60)
    if all_good:
        print("🎉 MCP Agent Deployment Verification: SUCCESS")
        print("✅ All files and configurations are in place")
        print("✅ MCP agent is ready to run with SAM")
        
        print(f"\n📋 Next Steps:")
        print(f"1. Ensure MCP server is available:")
        print(f"   # Check if the required MCP server package is installed")
        print(f"   npx -y @modelcontextprotocol/server-filesystem --help")
        print(f"")
        print(f"2. Run the MCP agent:")
        print(f"   cd {sam_path}")
        print(f"   ./start_mcp_agent.sh")
        print(f"   # Or manually:")
        print(f"   sam run configs/agents/{agent_name}.yaml")
        print(f"")
        print(f"3. Test the MCP agent:")
        print(f"   # Run configuration tests")
        print(f"   cd src/{agent_name} && python -m pytest tests/test_{agent_name}.py -v")
        print(f"   # Test in SAM: Ask the agent questions through the SAM interface")
        
    else:
        print("❌ MCP Agent Deployment Verification: FAILED")
        print("❌ Some files or configurations are missing")
        print("❌ Please re-run the deployment script")
        return False
    
    return True


def check_mcp_server_availability(agent_name: str):
    """Check if the required MCP server is available"""
    print(f"\n🔧 Checking MCP Server Availability")
    print("=" * 40)
    
    # Map agent names to their MCP servers
    mcp_servers = {
        "text_mcp_agent": "@modelcontextprotocol/server-text",
        "filesystem_mcp_agent": "@modelcontextprotocol/server-filesystem", 
        "system_mcp_agent": "@modelcontextprotocol/server-system"
    }
    
    mcp_server = mcp_servers.get(agent_name)
    if not mcp_server:
        print(f"❌ Unknown MCP agent: {agent_name}")
        print(f"   Supported agents: {list(mcp_servers.keys())}")
        return False
    
    print(f"🔍 Checking MCP server: {mcp_server}")
    
    try:
        # Try to run the MCP server with help to check availability
        if "filesystem" in mcp_server:
            # Filesystem server needs a directory argument
            cmd = ["npx", "-y", mcp_server, "/tmp"]
        else:
            cmd = ["npx", "-y", mcp_server, "--help"]
        
        # Run with timeout to avoid hanging
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Most MCP servers exit with 0 or 1 after initialization
        if process.returncode in [0, 1]:
            print(f"✅ MCP server {mcp_server} is available")
            return True
        else:
            print(f"❌ MCP server {mcp_server} failed to start")
            print(f"   Exit code: {process.returncode}")
            if process.stderr:
                print(f"   Error: {process.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        # Timeout usually means server started successfully
        print(f"✅ MCP server {mcp_server} is available (started successfully)")
        return True
    except FileNotFoundError:
        print(f"❌ npx command not found - Node.js/NPM not installed")
        return False
    except Exception as e:
        print(f"❌ Error checking MCP server: {str(e)}")
        return False


def check_sam_environment(sam_path: str):
    """Check SAM environment setup"""
    print(f"\n🔧 Checking SAM Environment")
    print("=" * 30)
    
    sam_path = Path(sam_path)
    
    # Check if SAM CLI is available
    try:
        # First try the system PATH
        result = subprocess.run(["sam", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ SAM CLI available: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    # Try in the virtual environment
    venv_sam = sam_path / ".venv" / "bin" / "sam"
    if venv_sam.exists():
        try:
            result = subprocess.run([str(venv_sam), "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ SAM CLI available in virtual environment: {result.stdout.strip()}")
                return True
        except Exception:
            pass
    
    print(f"❌ SAM CLI not found in PATH or virtual environment")
    print(f"   Expected locations:")
    print(f"   - System PATH")
    print(f"   - {venv_sam}")
    return False


def main():
    """Main verification function"""
    print("MCP Agent - Deployment Verification")
    print("=" * 50)
    
    # Check for help option
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        print("Usage: python verify_mcp_agent.py [SAM_PATH] [AGENT_NAME]")
        print("")
        print("Arguments:")
        print("  SAM_PATH     Path to your SAM installation (required)")
        print("  AGENT_NAME   Name of the MCP agent to verify (optional)")
        print("               Default: filesystem_mcp_agent")
        print("")
        print("Supported MCP agents:")
        print("  - text_mcp_agent")
        print("  - filesystem_mcp_agent")
        print("  - system_mcp_agent")
        print("")
        print("Examples:")
        print("  python verify_mcp_agent.py /path/to/sam")
        print("  python verify_mcp_agent.py /path/to/sam filesystem_mcp_agent")
        print("  python verify_mcp_agent.py /path/to/sam text_mcp_agent")
        sys.exit(0)
    
    # Get SAM path
    if len(sys.argv) > 1:
        sam_path = sys.argv[1]
    else:
        sam_path = input("Enter your SAM installation path: ").strip()
    
    if not sam_path:
        print("❌ SAM installation path is required")
        sys.exit(1)
    
    sam_path = Path(sam_path).resolve()
    
    if not sam_path.exists():
        print(f"❌ SAM installation path does not exist: {sam_path}")
        sys.exit(1)
    
    print(f"📁 SAM Installation Path: {sam_path}")
    
    # Get agent name
    if len(sys.argv) > 2:
        agent_name = sys.argv[2]
    else:
        agent_name = input("Enter MCP agent name (default: filesystem_mcp_agent): ").strip()
        if not agent_name:
            agent_name = "filesystem_mcp_agent"
    
    print(f"🤖 MCP Agent Name: {agent_name}")
    
    # Verify deployment
    deployment_ok = verify_deployment(str(sam_path), agent_name)
    
    # Check MCP server availability
    mcp_server_ok = check_mcp_server_availability(agent_name)
    
    # Check SAM environment
    environment_ok = check_sam_environment(str(sam_path))
    
    # Final summary
    print(f"\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Deployment: {'✅ SUCCESS' if deployment_ok else '❌ FAILED'}")
    print(f"MCP Server: {'✅ AVAILABLE' if mcp_server_ok else '❌ UNAVAILABLE'}")
    print(f"Environment: {'✅ READY' if environment_ok else '❌ ISSUES'}")
    
    if deployment_ok and mcp_server_ok and environment_ok:
        print(f"\n🎉 Everything is ready! You can now run the MCP agent.")
    elif deployment_ok and not mcp_server_ok:
        print(f"\n⚠️  Agent is deployed but MCP server is not available.")
        print(f"   Please install the required MCP server package.")
    elif deployment_ok and not environment_ok:
        print(f"\n⚠️  Agent is deployed but SAM environment needs configuration.")
    else:
        print(f"\n❌ Issues found. Please fix them before running the MCP agent.")


if __name__ == "__main__":
    main()
