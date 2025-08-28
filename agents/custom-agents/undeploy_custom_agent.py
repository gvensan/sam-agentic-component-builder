#!/usr/bin/env python3
"""
Generic undeployment script for any agent from SAM
This script removes agent files from your SAM installation directory
"""

import os
import shutil
import sys
from pathlib import Path


def undeploy_from_sam(sam_install_path: str, agent_name: str):
    """
    Undeploy any agent from SAM installation directory
    
    Args:
        sam_install_path: Path to your SAM installation directory
        agent_name: Name of the agent to remove from SAM
    """
    print(f"🗑️  Undeploying {agent_name} from SAM")
    print("=" * 50)
    
    # Define paths in SAM
    sam_agents_dir = Path(sam_install_path) / "src" / agent_name
    sam_configs_dir = Path(sam_install_path) / "configs" / "agents"
    config_dest = sam_configs_dir / f"{agent_name}.yaml"
    
    try:
        # Check if agent exists
        agent_exists = sam_agents_dir.exists() or config_dest.exists()
        
        if not agent_exists:
            print(f"❌ Agent '{agent_name}' not found in SAM installation")
            print(f"   Agent directory: {sam_agents_dir}")
            print(f"   Config file: {config_dest}")
            return False
        
        # Show what will be removed
        print(f"📁 Agent found in SAM installation:")
        if sam_agents_dir.exists():
            print(f"   Agent directory: {sam_agents_dir}")
        if config_dest.exists():
            print(f"   Config file: {config_dest}")
        
        # Confirm removal
        while True:
            confirm = input(f"\nDo you want to remove agent '{agent_name}'? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                print(f"🗑️  Removing agent '{agent_name}'...")
                break
            elif confirm in ['n', 'no', '']:
                print(f"❌ Undeployment cancelled. Agent '{agent_name}' was not removed.")
                return False
            else:
                print(f"Please enter 'y' to remove or 'n' to cancel.")
        
        # Remove agent directory
        if sam_agents_dir.exists():
            shutil.rmtree(sam_agents_dir)
            print(f"✅ Removed agent directory: {sam_agents_dir}")
        
        # Remove config file
        if config_dest.exists():
            config_dest.unlink()
            print(f"✅ Removed config file: {config_dest}")
        
        # Check if shared config is still needed by other agents
        shared_config_path = Path(sam_install_path) / "configs" / "shared_config.yaml"
        if shared_config_path.exists():
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
                        shared_config_path.unlink()
                        print(f"✅ Removed shared config: {shared_config_path}")
                        break
                    elif remove_shared in ['n', 'no', '']:
                        print(f"📁 Keeping shared config: {shared_config_path}")
                        break
                    else:
                        print(f"Please enter 'y' to remove or 'n' to keep.")
            else:
                print(f"📁 Keeping shared config (used by: {', '.join(other_agents)})")
        
        print("\n" + "=" * 50)
        print("🎉 Undeployment Completed Successfully!")
        print("=" * 50)
        print(f"Agent '{agent_name}' has been removed from SAM")
        print(f"Agent directory: {sam_agents_dir}")
        print(f"Config file: {config_dest}")
        
        return True
        
    except Exception as e:
        print(f"❌ Undeployment failed: {e}")
        return False


def list_deployed_agents(sam_install_path: str):
    """
    List all deployed agents in SAM installation
    
    Args:
        sam_install_path: Path to your SAM installation directory
    """
    print(f"📋 Listing deployed agents in SAM")
    print("=" * 50)
    
    sam_agents_dir = Path(sam_install_path) / "src"
    sam_configs_dir = Path(sam_install_path) / "configs" / "agents"
    
    agents = []
    
    # Check agent directories
    if sam_agents_dir.exists():
        for agent_dir in sam_agents_dir.iterdir():
            if agent_dir.is_dir():
                agent_name = agent_dir.name
                
                # Skip non-agent directories
                if agent_name in ["__pycache__", ".pytest_cache", ".git", ".vscode", "node_modules"]:
                    continue
                
                # Skip hidden directories
                if agent_name.startswith("."):
                    continue
                
                config_file = sam_configs_dir / f"{agent_name}.yaml"
                
                status = []
                if agent_dir.exists():
                    status.append("📁 Source")
                if config_file.exists():
                    status.append("⚙️ Config")
                
                agents.append({
                    "name": agent_name,
                    "status": " | ".join(status),
                    "path": str(agent_dir)
                })
    
    if not agents:
        print("❌ No agents found in SAM installation")
        return []
    
    print(f"Found {len(agents)} deployed agent(s):")
    print()
    for i, agent in enumerate(agents, 1):
        print(f"{i}. {agent['name']}")
        print(f"   Status: {agent['status']}")
        print(f"   Path: {agent['path']}")
        print()
    
    return agents


def main():
    """Main undeployment function"""
    print("Generic Agent - SAM Undeployment")
    print("=" * 40)
    
    # Get SAM installation path
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
    
    # Check if --list flag is provided
    if len(sys.argv) > 2 and sys.argv[2] == "--list":
        list_deployed_agents(str(sam_path))
        return
    
    # Get agent name
    if len(sys.argv) > 2:
        agent_name = sys.argv[2]
    else:
        # List available agents and let user choose
        agents = list_deployed_agents(str(sam_path))
        if not agents:
            sys.exit(1)
        
        print("Select agent to undeploy:")
        for i, agent in enumerate(agents, 1):
            print(f"{i}. {agent['name']}")
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
    
    print(f"🤖 Agent to undeploy: {agent_name}")
    
    # Undeploy the agent
    success = undeploy_from_sam(str(sam_path), agent_name)
    
    if success:
        print("\n" + "=" * 50)
        print("📋 Undeployment Summary:")
        print("=" * 50)
        print(f"✅ Agent '{agent_name}' has been successfully removed")
        print()
        print("To verify removal, you can:")
        print("1. List deployed agents:")
        print(f"   python undeploy_agent.py {sam_path} --list")
        print()
        print("2. Check SAM installation manually:")
        print(f"   ls {sam_path}/src/")
        print(f"   ls {sam_path}/configs/agents/")
        print()
        print("3. If you need to redeploy the agent:")
        print(f"   python deploy_agent.py {sam_path} {agent_name}")
        print()
        print("✅ Undeployment completed!")
    else:
        print("❌ Undeployment failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
