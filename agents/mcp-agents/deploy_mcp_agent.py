#!/usr/bin/env python3
"""
MCP Agent Deployment Script for SAM
This script deploys MCP agent configurations to your SAM installation directory

For MCP agents, deployment consists of:
1. YAML configuration files (agent config + shared config)
2. Future: src folder contents (when post-processing/customization is added)
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path


def deploy_mcp_agent_to_sam(sam_install_path: str, agent_name: str, agent_source_dir: str = None):
    """
    Deploy MCP agent to SAM installation directory
    
    Args:
        sam_install_path: Path to your SAM installation directory
        agent_name: Name for the agent in SAM
        agent_source_dir: Optional source directory name (defaults to agent_name)
    """
    print(f"🚀 Deploying MCP Agent: {agent_name} to SAM")
    print("=" * 50)
    
    # Get current directory (where this script is located)
    current_dir = Path(__file__).parent.absolute()
    
    # Determine source directory
    if agent_source_dir is None:
        agent_source_dir = agent_name
    
    # Define source and destination paths
    source_paths = {
        "agent_config": current_dir / "configs" / "agents" / f"{agent_source_dir}.yaml",
        "shared_config": current_dir / "configs" / "shared_config.yaml",
        "agent_source": current_dir / "src" / agent_source_dir  # For future use
    }
    
    # Define destination paths in SAM
    sam_configs_dir = Path(sam_install_path) / "configs" / "agents"
    sam_shared_configs_dir = Path(sam_install_path) / "configs"
    sam_agents_dir = Path(sam_install_path) / "src" / agent_name  # For future use
    
    try:
        # Check if agent already exists BEFORE creating directories
        config_dest = sam_configs_dir / f"{agent_name}.yaml"
        shared_config_dest = sam_shared_configs_dir / "shared_config.yaml"
        
        agent_exists = config_dest.exists()
        
        if agent_exists:
            print(f"⚠️  MCP Agent '{agent_name}' already exists!")
            print(f"   Config file: {config_dest}")
            
            while True:
                overwrite = input(f"\nDo you want to overwrite the existing agent? (y/N): ").strip().lower()
                if overwrite in ['y', 'yes']:
                    print(f"🔄 Overwriting existing agent...")
                    if config_dest.exists():
                        config_dest.unlink()
                    break
                elif overwrite in ['n', 'no', '']:
                    print(f"❌ Deployment cancelled. Agent '{agent_name}' was not overwritten.")
                    return False
                else:
                    print(f"Please enter 'y' to overwrite or 'n' to cancel.")
        
        # Create destination directories
        sam_configs_dir.mkdir(parents=True, exist_ok=True)
        sam_shared_configs_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Creating directories in SAM installation...")
        print(f"   Config directory: {sam_configs_dir}")
        print(f"   Shared config directory: {sam_shared_configs_dir}")
        
        # Copy and customize agent configuration
        if source_paths["agent_config"].exists():
            config_dest = sam_configs_dir / f"{agent_name}.yaml"
            
            # Read the original config and customize it
            with open(source_paths["agent_config"], 'r') as f:
                config_content = f.read()
            
            # Replace hard-coded agent names with the custom name
            agent_name_clean = agent_name.replace("-", "").replace("_", "")
            agent_name_underscore = agent_name.replace("-", "_").replace(" ", "_")
            source_name_clean = agent_source_dir.replace("-", "").replace("_", "")
            source_name_underscore = agent_source_dir.replace("-", "_").replace(" ", "_")
            
            # Replace agent names in config
            config_content = config_content.replace(source_name_clean, agent_name_clean)
            config_content = config_content.replace(agent_source_dir.replace("-", " ").replace("_", " "), agent_name.replace("-", " ").replace("_", " "))
            config_content = config_content.replace(agent_source_dir, agent_name)
            
            # Replace app names
            config_content = config_content.replace(f"{agent_source_dir}_app", f"{agent_name}_app")
            
            # Write the customized config
            with open(config_dest, 'w') as f:
                f.write(config_content)
            
            print(f"✅ Copied and customized agent config to: {config_dest}")
        else:
            print(f"❌ Agent config not found: {source_paths['agent_config']}")
            return False
        
        # Copy shared configuration (if it doesn't exist or is different)
        if source_paths["shared_config"].exists():
            shared_config_dest = sam_shared_configs_dir / "shared_config.yaml"
            
            # Check if shared config already exists
            if shared_config_dest.exists():
                # Compare files to see if they're different
                with open(source_paths["shared_config"], 'r') as f:
                    source_content = f.read()
                with open(shared_config_dest, 'r') as f:
                    dest_content = f.read()
                
                if source_content != dest_content:
                    print(f"⚠️  Shared config already exists but differs from source")
                    while True:
                        overwrite_shared = input(f"Overwrite existing shared config? (y/N): ").strip().lower()
                        if overwrite_shared in ['y', 'yes']:
                            shutil.copy2(source_paths["shared_config"], shared_config_dest)
                            print(f"✅ Updated shared config: {shared_config_dest}")
                            break
                        elif overwrite_shared in ['n', 'no', '']:
                            print(f"📁 Keeping existing shared config: {shared_config_dest}")
                            break
                        else:
                            print(f"Please enter 'y' to overwrite or 'n' to keep.")
                else:
                    print(f"📁 Shared config already exists and is identical: {shared_config_dest}")
            else:
                shutil.copy2(source_paths["shared_config"], shared_config_dest)
                print(f"✅ Copied shared config to: {shared_config_dest}")
        else:
            print(f"⚠️  Shared config not found: {source_paths['shared_config']}")
            print(f"   Make sure shared_config.yaml exists in configs/ directory")
        
        # TODO: Future - Copy agent source code when post-processing is added
        # For now, MCP agents are YAML-only
        print(f"📝 Note: MCP agents are currently YAML-only (no source code deployment needed)")
        
        # Create deployment info file
        deployment_info = {
            "agent_name": agent_name,
            "agent_type": "mcp_agent",
            "deployed_at": str(Path().cwd()),
            "sam_path": sam_install_path,
            "version": "1.0.0",
            "config_file": f"{agent_name}.yaml",
            "mcp_only": True,
            "source_code_deployed": False
        }
        
        info_file = sam_configs_dir / f"{agent_name}_deployment_info.txt"
        with open(info_file, 'w') as f:
            for key, value in deployment_info.items():
                f.write(f"{key}: {value}\n")
        
        print(f"✅ Created deployment info: {info_file}")
        
        print("\n" + "=" * 50)
        print("🎉 MCP Agent Deployment Completed Successfully!")
        print("=" * 50)
        print(f"Agent deployed to: {config_dest}")
        print(f"Agent name: {agent_name}")
        print(f"Agent type: MCP Agent (YAML-only)")
        print(f"📝 Note: No source code deployment needed for YAML-only MCP agents")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False


def verify_mcp_server_availability(agent_name: str):
    """
    Verify that the required MCP server is available
    
    Args:
        agent_name: Name of the agent to check
    
    Returns:
        bool: True if MCP server is available, False otherwise
    """
    # Map agent names to their MCP servers
    mcp_servers = {
        "text_mcp_agent": "@modelcontextprotocol/server-text",
        "filesystem_mcp_agent": "@modelcontextprotocol/server-filesystem",
        "system_mcp_agent": "@modelcontextprotocol/server-system"
    }
    
    mcp_server = mcp_servers.get(agent_name)
    if not mcp_server:
        print(f"⚠️  Unknown MCP agent: {agent_name}")
        return True  # Don't fail deployment for unknown agents
    
    print(f"🔍 Verifying MCP server availability: {mcp_server}")
    
    try:
        # Test MCP server startup
        cmd = ["npx", "-y", mcp_server]
        
        # Run with timeout to avoid hanging
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Most MCP servers exit with 0 or 1 after initialization
        if process.returncode in [0, 1]:
            print(f"✅ MCP server is available: {mcp_server}")
            return True
        else:
            print(f"❌ MCP server failed to start: {mcp_server}")
            print(f"   Exit code: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        # Timeout usually means server started successfully
        print(f"✅ MCP server is available (timeout): {mcp_server}")
        return True
    except FileNotFoundError:
        print(f"❌ npx command not found - Node.js/NPM not installed")
        print(f"   Please install Node.js and NPM to use MCP servers")
        return False
    except Exception as e:
        print(f"❌ Error testing MCP server: {str(e)}")
        return False


def print_help():
    """Print help information"""
    print("🚀 MCP Agent Deployment Tool for SAM")
    print("=" * 50)
    print()
    print("Usage:")
    print("  python deploy_mcp_agent.py <sam_path> [agent_name] [options]")
    print()
    print("Arguments:")
    print("  sam_path     Path to your SAM installation directory")
    print("  agent_name   Name of the MCP agent to deploy (optional, will prompt if not provided)")
    print()
    print("Options:")
    print("  --list       List available MCP agents for deployment")
    print("  --help, -h   Show this help message")
    print()
    print("Examples:")
    print("  # Deploy with interactive agent selection")
    print("  python deploy_mcp_agent.py /path/to/sam")
    print()
    print("  # Deploy specific MCP agent")
    print("  python deploy_mcp_agent.py /path/to/sam text_mcp_agent")
    print()
    print("  # List available MCP agents")
    print("  python deploy_mcp_agent.py /path/to/sam --list")
    print()
    print("Features:")
    print("  ✅ YAML configuration deployment")
    print("  ✅ Shared configuration management")
    print("  ✅ MCP server availability verification")
    print("  ✅ Agent name customization")
    print("  ✅ Comprehensive error handling")
    print("  ✅ Future-ready for source code deployment")


def list_available_mcp_agents():
    """
    List all available MCP agents in the configs/agents directory
    
    Returns:
        List of available MCP agent configurations
    """
    configs_dir = Path(__file__).parent / "configs" / "agents"
    agents = []
    
    if configs_dir.exists():
        for yaml_file in configs_dir.glob("*.yaml"):
            agent_name = yaml_file.stem
            agents.append({
                "name": agent_name,
                "config_file": str(yaml_file),
                "valid": True
            })
    
    return agents


def list_available_mcp_agents_for_deployment():
    """
    List all available MCP agents for deployment
    """
    print("📋 Available MCP agents for deployment")
    print("=" * 50)
    
    agents = list_available_mcp_agents()
    
    if not agents:
        print("❌ No MCP agents found in configs/agents/ directory")
        print()
        print("To create a new MCP agent:")
        print("1. Create config file: configs/agents/my_new_mcp_agent.yaml")
        print("2. Follow the YAML-only MCP agent pattern")
        print("3. Run: python deploy_mcp_agent.py <sam_path> my_new_mcp_agent")
        return
    
    print(f"Found {len(agents)} MCP agent(s):")
    print()
    for i, agent in enumerate(agents, 1):
        print(f"{i}. {agent['name']}")
        print(f"   Config: {agent['config_file']}")
        print()
    
    print("To deploy an MCP agent:")
    print("python deploy_mcp_agent.py <sam_path> [agent_name]")
    print("or")
    print("python deploy_mcp_agent.py <sam_path> (to select interactively)")


def create_sam_run_script(sam_install_path: str, agent_name: str):
    """Create a script to run the MCP agent with SAM"""
    script_content = f"""#!/bin/bash
# SAM Run Script for MCP Agent: {agent_name}
# Generated by deploy_mcp_agent.py

SAM_PATH="{sam_install_path}"
AGENT_CONFIG="$SAM_PATH/configs/agents/{agent_name}.yaml"

echo "🚀 Starting MCP Agent: {agent_name} with SAM..."
echo "SAM Path: $SAM_PATH"
echo "Agent Name: {agent_name}"
echo "Config: $AGENT_CONFIG"

# Change to SAM directory
cd "$SAM_PATH"

# Run the MCP agent
sam run "$AGENT_CONFIG"
"""
    
    script_path = Path(__file__).parent / "start_mcp_agent.sh"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(script_path, 0o755)
    
    print(f"✅ Created run script: {script_path}")
    return script_path


def main():
    """Main deployment function"""
    print("MCP Agent - SAM Deployment")
    print("=" * 40)
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    # Check for help flag
    if "--help" in args or "-h" in args:
        print_help()
        return
    
    # Get SAM installation path
    if len(args) > 0:
        sam_path = args[0]
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
    
    # Check if --list flag is provided
    if len(args) > 1 and args[1] == "--list":
        list_available_mcp_agents_for_deployment()
        return
    
    # Get agent name
    if len(args) > 1:
        agent_name = args[1]
    else:
        # List available agents and let user choose
        agents = list_available_mcp_agents()
        if not agents:
            print("❌ No MCP agents found in configs/agents/ directory")
            sys.exit(1)
        
        print("📋 Available MCP agents for deployment:")
        print("=" * 50)
        for i, agent in enumerate(agents, 1):
            print(f"{i}. {agent['name']}")
        print("0. Cancel")
        
        while True:
            try:
                choice = input(f"\nSelect MCP agent to deploy (0-{len(agents)}): ").strip()
                if choice == "0":
                    print("❌ Deployment cancelled.")
                    return
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(agents):
                    selected_agent = agents[choice_num - 1]
                    agent_name = selected_agent["name"]
                    agent_source_dir = selected_agent["name"]
                    break
                else:
                    print(f"Please enter a number between 0 and {len(agents)}")
            except ValueError:
                print("Please enter a valid number")
    
    print(f"🤖 MCP Agent Name: {agent_name}")
    
    # Get agent source directory (optional)
    if len(args) > 2:
        agent_source_dir = args[2]
    else:
        # Use the selected agent's directory name
        agent_source_dir = agent_name
    
    # Verify MCP server availability
    if not verify_mcp_server_availability(agent_name):
        print(f"⚠️  MCP server verification failed for {agent_name}")
        print(f"   The agent may not work properly without the required MCP server")
        print(f"   Continue with deployment anyway? (y/N): ", end="")
        continue_deploy = input().strip().lower()
        if continue_deploy not in ['y', 'yes']:
            print("❌ Deployment cancelled due to MCP server issues.")
            return
    
    # Deploy the MCP agent
    success = deploy_mcp_agent_to_sam(str(sam_path), agent_name, agent_source_dir)
    
    if success:
        # Create run script
        run_script = create_sam_run_script(str(sam_path), agent_name)
        
        print("\n" + "=" * 50)
        print("📋 Next Steps:")
        print("=" * 50)
        print("1. MCP Agent deployed successfully! ✅")
        print(f"   Config file: {sam_path}/configs/agents/{agent_name}.yaml")
        print()
        print("2. Run the MCP agent using the generated script:")
        print(f"   ./start_mcp_agent.sh")
        print()
        print("3. Or run manually:")
        print(f"   cd {sam_path}")
        print(f"   sam run configs/agents/{agent_name}.yaml")
        print()
        print("4. Test the MCP agent:")
        print("   - Test in SAM: Ask the agent questions through the SAM interface")
        print("   - Verify MCP tools are available and working")
        print("   - Check agent discovery and communication")
        print()
        print("5. For more information:")
        print(f"   - Read the MCP agent documentation")
        print(f"   - Check MCP server documentation for available tools")
        print()
        print("✅ MCP Agent is ready to use!")
    else:
        print("❌ Deployment failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
