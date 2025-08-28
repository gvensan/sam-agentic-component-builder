#!/usr/bin/env python3
"""
MCP Agent Undeployment Script for SAM
This script removes MCP agent configurations from your SAM installation directory

For MCP agents, undeployment consists of:
1. YAML configuration files (agent config)
2. Shared configuration (if not used by other agents)
3. Future: src folder contents (when post-processing/customization is added)
"""

import os
import shutil
import sys
from pathlib import Path


def undeploy_mcp_agent_from_sam(sam_install_path: str, agent_name: str):
    """
    Undeploy MCP agent from SAM installation directory
    
    Args:
        sam_install_path: Path to your SAM installation directory
        agent_name: Name of the agent to remove from SAM
    """
    print(f"🗑️  Undeploying MCP Agent: {agent_name} from SAM")
    print("=" * 50)
    
    # Define paths in SAM
    sam_configs_dir = Path(sam_install_path) / "configs" / "agents"
    sam_shared_configs_dir = Path(sam_install_path) / "configs"
    config_dest = sam_configs_dir / f"{agent_name}.yaml"
    shared_config_dest = sam_shared_configs_dir / "shared_config.yaml"
    
    try:
        # Check if agent exists
        agent_exists = config_dest.exists()
        
        if not agent_exists:
            print(f"❌ MCP Agent '{agent_name}' not found in SAM installation")
            print(f"   Config file: {config_dest}")
            return False
        
        # Show what will be removed
        print(f"📁 MCP Agent found in SAM installation:")
        print(f"   Config file: {config_dest}")
        
        # Check for deployment info file
        info_file = sam_configs_dir / f"{agent_name}_deployment_info.txt"
        if info_file.exists():
            print(f"   Deployment info: {info_file}")
        
        # Confirm removal
        while True:
            confirm = input(f"\nDo you want to remove MCP agent '{agent_name}'? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                print(f"🗑️  Removing MCP agent '{agent_name}'...")
                break
            elif confirm in ['n', 'no', '']:
                print(f"❌ Undeployment cancelled. MCP agent '{agent_name}' was not removed.")
                return False
            else:
                print(f"Please enter 'y' to remove or 'n' to cancel.")
        
        # Remove config file
        if config_dest.exists():
            config_dest.unlink()
            print(f"✅ Removed config file: {config_dest}")
        
        # Remove deployment info file
        if info_file.exists():
            info_file.unlink()
            print(f"✅ Removed deployment info: {info_file}")
        
        # Check if shared config is still needed by other agents
        if shared_config_dest.exists():
            # Check if any other agents are using the shared config
            other_agents = []
            for config_file in sam_configs_dir.glob("*.yaml"):
                if config_file.name != f"{agent_name}.yaml":
                    try:
                        with open(config_file, 'r') as f:
                            content = f.read()
                            if "!include ../shared_config.yaml" in content:
                                other_agent = config_file.stem
                                other_agents.append(other_agent)
                    except Exception:
                        pass
            
            if not other_agents:
                print(f"⚠️  No other agents found using shared config")
                while True:
                    remove_shared = input(f"Remove shared config file? (y/N): ").strip().lower()
                    if remove_shared in ['y', 'yes']:
                        shared_config_dest.unlink()
                        print(f"✅ Removed shared config: {shared_config_dest}")
                        break
                    elif remove_shared in ['n', 'no', '']:
                        print(f"📁 Keeping shared config: {shared_config_dest}")
                        break
                    else:
                        print(f"Please enter 'y' to remove or 'n' to keep.")
            else:
                print(f"📁 Keeping shared config (used by: {', '.join(other_agents)})")
        
        # TODO: Future - Remove agent source code when post-processing is added
        # For now, MCP agents are YAML-only
        print(f"📝 Note: MCP agents are currently YAML-only (no source code to remove)")
        
        print("\n" + "=" * 50)
        print("🎉 MCP Agent Undeployment Completed Successfully!")
        print("=" * 50)
        print(f"MCP Agent '{agent_name}' has been removed from SAM")
        print(f"Config file: {config_dest}")
        print(f"Agent type: MCP Agent (YAML-only)")
        
        return True
        
    except Exception as e:
        print(f"❌ Undeployment failed: {e}")
        return False


def list_deployed_mcp_agents(sam_install_path: str):
    """
    List all deployed MCP agents in SAM installation
    
    Args:
        sam_install_path: Path to your SAM installation directory
    """
    print(f"📋 Listing deployed MCP agents in SAM")
    print("=" * 50)
    
    sam_configs_dir = Path(sam_install_path) / "configs" / "agents"
    
    agents = []
    
    # Check for MCP agent config files
    if sam_configs_dir.exists():
        for config_file in sam_configs_dir.glob("*.yaml"):
            agent_name = config_file.stem
            
            # Skip non-agent files
            if agent_name in ["shared_config"]:
                continue
            
            # Check if it's an MCP agent by looking for MCP tools
            is_mcp_agent = False
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                    if "tool_type: mcp" in content:
                        is_mcp_agent = True
            except Exception:
                pass
            
            if is_mcp_agent:
                # Check for deployment info
                info_file = sam_configs_dir / f"{agent_name}_deployment_info.txt"
                deployment_info = {}
                if info_file.exists():
                    try:
                        with open(info_file, 'r') as f:
                            for line in f:
                                if ':' in line:
                                    key, value = line.strip().split(':', 1)
                                    deployment_info[key.strip()] = value.strip()
                    except Exception:
                        pass
                
                agent_type = deployment_info.get('agent_type', 'Unknown')
                mcp_only = deployment_info.get('mcp_only', 'Unknown')
                
                agents.append({
                    "name": agent_name,
                    "config_file": str(config_file),
                    "agent_type": agent_type,
                    "mcp_only": mcp_only,
                    "deployment_info": deployment_info
                })
    
    if not agents:
        print("❌ No MCP agents found in SAM installation")
        return []
    
    print(f"Found {len(agents)} deployed MCP agent(s):")
    print()
    for i, agent in enumerate(agents, 1):
        print(f"{i}. {agent['name']}")
        print(f"   Type: {agent['agent_type']}")
        print(f"   MCP Only: {agent['mcp_only']}")
        print(f"   Config: {agent['config_file']}")
        print()
    
    return agents


def print_help():
    """Print help information"""
    print("🗑️  MCP Agent Undeployment Tool for SAM")
    print("=" * 50)
    print()
    print("Usage:")
    print("  python undeploy_mcp_agent.py <sam_path> [agent_name] [options]")
    print()
    print("Arguments:")
    print("  sam_path     Path to your SAM installation directory")
    print("  agent_name   Name of the MCP agent to undeploy (optional, will prompt if not provided)")
    print()
    print("Options:")
    print("  --list       List deployed MCP agents in SAM")
    print("  --help, -h   Show this help message")
    print()
    print("Examples:")
    print("  # Undeploy with interactive agent selection")
    print("  python undeploy_mcp_agent.py /path/to/sam")
    print()
    print("  # Undeploy specific MCP agent")
    print("  python undeploy_mcp_agent.py /path/to/sam text_mcp_agent")
    print()
    print("  # List deployed MCP agents")
    print("  python undeploy_mcp_agent.py /path/to/sam --list")
    print()
    print("Features:")
    print("  ✅ YAML configuration removal")
    print("  ✅ Shared configuration management")
    print("  ✅ Deployment info cleanup")
    print("  ✅ Safe shared config handling")
    print("  ✅ Comprehensive error handling")
    print("  ✅ Future-ready for source code removal")


def main():
    """Main undeployment function"""
    print("MCP Agent - SAM Undeployment")
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
        list_deployed_mcp_agents(str(sam_path))
        return
    
    # Get agent name
    if len(args) > 1:
        agent_name = args[1]
    else:
        # List available agents and let user choose
        agents = list_deployed_mcp_agents(str(sam_path))
        if not agents:
            sys.exit(1)
        
        print("Select MCP agent to undeploy:")
        for i, agent in enumerate(agents, 1):
            print(f"{i}. {agent['name']} ({agent['agent_type']})")
        print("0. Cancel")
        
        while True:
            try:
                choice = input(f"\nEnter choice (0-{len(agents)}): ").strip()
                if choice == "0":
                    print("❌ Undeployment cancelled.")
                    return
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(agents):
                    agent_name = agents[choice_num - 1]['name']
                    break
                else:
                    print(f"Please enter a number between 0 and {len(agents)}")
            except ValueError:
                print("Please enter a valid number")
    
    print(f"🤖 MCP Agent to undeploy: {agent_name}")
    
    # Undeploy the MCP agent
    success = undeploy_mcp_agent_from_sam(str(sam_path), agent_name)
    
    if success:
        print("\n" + "=" * 50)
        print("📋 Undeployment Summary:")
        print("=" * 50)
        print(f"✅ MCP Agent '{agent_name}' has been successfully removed")
        print()
        print("To verify removal, you can:")
        print("1. List deployed MCP agents:")
        print(f"   python undeploy_mcp_agent.py {sam_path} --list")
        print()
        print("2. Check SAM installation manually:")
        print(f"   ls {sam_path}/configs/agents/")
        print()
        print("3. If you need to redeploy the MCP agent:")
        print(f"   python deploy_mcp_agent.py {sam_path} {agent_name}")
        print()
        print("✅ Undeployment completed!")
    else:
        print("❌ Undeployment failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
