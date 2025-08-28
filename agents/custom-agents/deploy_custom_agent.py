#!/usr/bin/env python3
"""
Generic deployment script for any agent to SAM
This script copies agent files to your SAM installation directory

During deployment, the following files/directories are automatically skipped:
- tests/ (test files)
- __pycache__/ (Python cache)
- .pyc files (compiled Python files)
- .pytest_cache/ (pytest cache)
- .git/ (version control)
- .env (environment files)
- .env.sample (environment sample files)
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path


def deploy_to_sam(sam_install_path: str, agent_name: str, agent_source_dir: str = None, skip_deps: bool = False):
    """
    Deploy any agent to SAM installation directory
    
    Args:
        sam_install_path: Path to your SAM installation directory
        agent_name: Name for the agent in SAM
        agent_source_dir: Optional source directory name (defaults to agent_name)
        skip_deps: Skip automatic dependency installation
    """
    print(f"🚀 Deploying {agent_name} to SAM")
    print("=" * 50)
    
    # Get current directory (where this script is located)
    current_dir = Path(__file__).parent.absolute()
    
    # Determine source directory
    if agent_source_dir is None:
        agent_source_dir = agent_name
    
    # Define source and destination paths
    source_paths = {
        "agent_source": current_dir / "src" / agent_source_dir,
        "agent_config": current_dir / "configs" / "agents" / f"{agent_source_dir}.yaml",
        "requirements": current_dir / "src" / agent_source_dir / "requirements.txt"
    }
    
    # Define destination paths in SAM
    sam_agents_dir = Path(sam_install_path) / "src" / agent_name
    sam_configs_dir = Path(sam_install_path) / "configs" / "agents"
    sam_shared_configs_dir = Path(sam_install_path) / "configs"
    
    try:
        # Check if agent already exists BEFORE creating directories
        agent_dest = sam_agents_dir
        config_dest = sam_configs_dir / f"{agent_name}.yaml"
        
        agent_exists = agent_dest.exists() or config_dest.exists()
        
        if agent_exists:
            print(f"⚠️  Agent '{agent_name}' already exists!")
            print(f"   Agent directory: {agent_dest}")
            print(f"   Config file: {config_dest}")
            
            while True:
                overwrite = input(f"\nDo you want to overwrite the existing agent? (y/N): ").strip().lower()
                if overwrite in ['y', 'yes']:
                    print(f"🔄 Overwriting existing agent...")
                    if agent_dest.exists():
                        shutil.rmtree(agent_dest)
                    if config_dest.exists():
                        config_dest.unlink()
                    break
                elif overwrite in ['n', 'no', '']:
                    print(f"❌ Deployment cancelled. Agent '{agent_name}' was not overwritten.")
                    return False
                else:
                    print(f"Please enter 'y' to overwrite or 'n' to cancel.")
        
        # Create destination directories AFTER checking existence
        sam_agents_dir.mkdir(parents=True, exist_ok=True)
        sam_configs_dir.mkdir(parents=True, exist_ok=True)
        sam_shared_configs_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Creating directories in SAM installation...")
        print(f"   Agent directory: {sam_agents_dir}")
        print(f"   Config directory: {sam_configs_dir}")
        
        # Copy and customize agent source code
        if source_paths["agent_source"].exists():
            # Remove existing directory if it exists (we already checked and got user confirmation)
            if agent_dest.exists():
                shutil.rmtree(agent_dest)
            
            # Define patterns to ignore during copy
            def ignore_patterns(dir, files):
                ignored = []
                for file in files:
                    # Skip __pycache__ directories
                    if file == "__pycache__":
                        ignored.append(file)
                    # Skip test directories
                    elif file == "tests":
                        ignored.append(file)
                    # Skip .pyc files
                    elif file.endswith(".pyc"):
                        ignored.append(file)
                    # Skip .pytest_cache and any pytest-related directories
                    elif file == ".pytest_cache" or "pytest" in file.lower():
                        ignored.append(file)
                    # Skip .git directories
                    elif file == ".git":
                        ignored.append(file)
                    # Skip .env files (should not be deployed)
                    elif file == ".env":
                        ignored.append(file)
                    # Skip .env.sample files (documentation only)
                    elif file == ".env.sample":
                        ignored.append(file)
                    # Skip any cache-related directories
                    elif "cache" in file.lower() and file.startswith("."):
                        ignored.append(file)
                return ignored
            
            shutil.copytree(source_paths["agent_source"], agent_dest, ignore=ignore_patterns)
            
            # Customize lifecycle functions with the agent name
            lifecycle_file = agent_dest / "lifecycle.py"
            if lifecycle_file.exists():
                with open(lifecycle_file, 'r') as f:
                    lifecycle_content = f.read()
                
                # Replace function names with agent-specific names
                agent_name_clean = agent_name.replace("-", "_").replace(" ", "_")
                source_name_clean = agent_source_dir.replace("-", "_").replace(" ", "_")
                
                # Replace original function names with new ones
                lifecycle_content = lifecycle_content.replace(
                    f"initialize_{source_name_clean}", 
                    f"initialize_{agent_name_clean}"
                )
                lifecycle_content = lifecycle_content.replace(
                    f"cleanup_{source_name_clean}", 
                    f"cleanup_{agent_name_clean}"
                )
                
                # Write the customized lifecycle file
                with open(lifecycle_file, 'w') as f:
                    f.write(lifecycle_content)
                
                print(f"✅ Customized lifecycle functions for {agent_name}")
            
            print(f"✅ Copied and customized agent source code to: {agent_dest}")
        else:
            print(f"❌ Agent source not found: {source_paths['agent_source']}")
            return False
        
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
            
            # Fix shared config include syntax
            config_content = config_content.replace("shared_config: !include", "!include")
            
            # Update lifecycle function references
            config_content = config_content.replace(
                f"initialize_{source_name_underscore}", 
                f"initialize_{agent_name_underscore}"
            )
            config_content = config_content.replace(
                f"cleanup_{source_name_underscore}", 
                f"cleanup_{agent_name_underscore}"
            )
            
            # Add missing sections if they don't exist
            if "artifact_management" not in config_content:
                # Extract tool information from the config to create proper agent card
                import re
                tool_pattern = r'function_name:\s*"([^"]+)"\s*\n\s*tool_description:\s*"([^"]+)"'
                tools = re.findall(tool_pattern, config_content)
                
                # Generate skills for agent card
                skills_section = ""
                for function_name, description in tools:
                    skill_name = function_name.replace("_", " ").title()
                    skills_section += f"""          - id: "{function_name}"
            name: "{skill_name}"
            description: "{description}"
"""
                
                # Add missing sections
                missing_sections = f"""
        # Built-in artifact tools for file operations
        - tool_type: builtin-group
          group_name: "artifact_management"
    
      session_service: *default_session_service
      artifact_service: *default_artifact_service

      artifact_handling_mode: "reference"
      enable_embed_resolution: true
      enable_artifact_content_instruction: true
      
      # Agent card
      agent_card:
        description: "Professional {agent_name.replace('-', ' ').title()} agent providing comprehensive services"
        defaultInputModes: ["text"]
        defaultOutputModes: ["text", "file"]
        skills:
{skills_section}
      # Discovery & Communication
      agent_card_publishing: 
        interval_seconds: 10
      agent_discovery: 
        enabled: true

      inter_agent_communication:
        allow_list: ["*"] 
        deny_list: [] 
        request_timeout_seconds: 600
"""
                
                # Find where to insert (after the last tool)
                lines = config_content.split('\n')
                insert_index = -1
                
                # Find the last tool entry
                for i, line in enumerate(lines):
                    if "tool_description:" in line:
                        insert_index = i + 1
                
                if insert_index > 0:
                    # Insert the missing sections
                    lines.insert(insert_index, missing_sections)
                    config_content = '\n'.join(lines)
            
            # Write the customized config
            with open(config_dest, 'w') as f:
                f.write(config_content)
            
            print(f"✅ Copied and customized agent config to: {config_dest}")
        else:
            print(f"❌ Agent config not found: {source_paths['agent_config']}")
            return False
        
        # Copy requirements
        if source_paths["requirements"].exists():
            requirements_dest = sam_agents_dir / "requirements.txt"
            shutil.copy2(source_paths["requirements"], requirements_dest)
            print(f"✅ Copied requirements to: {requirements_dest}")
        else:
            print(f"❌ Requirements not found: {source_paths['requirements']}")
            return False
        
        # Install dependencies automatically (unless skipped)
        if not skip_deps:
            print(f"📦 Installing dependencies for {agent_name}...")
            install_success = install_agent_dependencies(sam_install_path, agent_name)
            if not install_success:
                print(f"⚠️  Dependency installation failed, but deployment completed")
                print(f"   You may need to install dependencies manually:")
                print(f"   cd {sam_install_path}")
                print(f"   pip install -r src/{agent_name}/requirements.txt")
        else:
            print(f"⏭️  Skipping dependency installation (--skip-deps flag used)")
            print(f"   Install dependencies manually:")
            print(f"   cd {sam_install_path}")
            print(f"   pip install -r src/{agent_name}/requirements.txt")
        
        # Create deployment info file
        deployment_info = {
            "agent_name": agent_name,
            "deployed_at": str(Path().cwd()),
            "sam_path": sam_install_path,
            "version": "1.0.0",
            "config_file": f"{agent_name}.yaml"
        }
        
        info_file = sam_agents_dir / "deployment_info.txt"
        with open(info_file, 'w') as f:
            for key, value in deployment_info.items():
                f.write(f"{key}: {value}\n")
        
        print(f"✅ Created deployment info: {info_file}")
        
        print("\n" + "=" * 50)
        print("🎉 Deployment Completed Successfully!")
        print("=" * 50)
        print(f"Agent deployed to: {sam_agents_dir}")
        print(f"Config deployed to: {config_dest}")
        print(f"Agent name: {agent_name}")
        print(f"📝 Note: Tests, __pycache__, and development files were skipped")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False


def install_agent_dependencies(sam_install_path: str, agent_name: str):
    """
    Install dependencies for the deployed agent
    
    Args:
        sam_install_path: Path to SAM installation
        agent_name: Name of the deployed agent
    
    Returns:
        bool: True if installation successful, False otherwise
    """
    try:
        # Check if agent has its own requirements.txt
        agent_requirements = Path(sam_install_path) / "src" / agent_name / "requirements.txt"
        
        if not agent_requirements.exists():
            print(f"   ℹ️  No agent-specific requirements found: {agent_requirements}")
            return True
        
        print(f"   📦 Installing agent-specific dependencies from: {agent_requirements}")
        
        # Change to SAM directory for installation
        original_cwd = os.getcwd()
        os.chdir(sam_install_path)
        
        try:
            # Run pip install
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(agent_requirements)
            ], capture_output=True, text=True, check=True)
            
            print(f"   ✅ Dependencies installed successfully")
            if result.stdout:
                print(f"   📋 Installation output:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        print(f"      {line}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Dependency installation failed:")
            print(f"      Error: {e}")
            if e.stdout:
                print(f"      stdout: {e.stdout}")
            if e.stderr:
                print(f"      stderr: {e.stderr}")
            return False
            
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
            
    except Exception as e:
        print(f"   ❌ Error during dependency installation: {e}")
        return False


def print_help():
    """Print help information"""
    print("🚀 SAM Agent Deployment Tool")
    print("=" * 40)
    print()
    print("Usage:")
    print("  python deploy_agent.py <sam_path> [agent_name] [options]")
    print()
    print("Arguments:")
    print("  sam_path     Path to your SAM installation directory")
    print("  agent_name   Name of the agent to deploy (optional, will prompt if not provided)")
    print()
    print("Options:")
    print("  --skip-deps  Skip automatic dependency installation")
    print("  --list       List available agents for deployment")
    print("  --help, -h   Show this help message")
    print()
    print("Examples:")
    print("  # Deploy with interactive agent selection")
    print("  python deploy_agent.py /path/to/sam")
    print()
    print("  # Deploy specific agent")
    print("  python deploy_agent.py /path/to/sam country_information_agent")
    print()
    print("  # Deploy without installing dependencies")
    print("  python deploy_agent.py /path/to/sam country_information_agent --skip-deps")
    print()
    print("  # List available agents")
    print("  python deploy_agent.py /path/to/sam --list")
    print()
    print("Features:")
    print("  ✅ Automatic dependency installation")
    print("  ✅ Agent source code customization")
    print("  ✅ Configuration file generation")
    print("  ✅ Run script creation")
    print("  ✅ Comprehensive error handling")
    print("  ✅ Skips tests, __pycache__, and other development files")


def list_available_agents():
    """
    List all available agents in the src directory
    
    Returns:
        List of available agent directories
    """
    src_dir = Path(__file__).parent / "src"
    agents = []
    
    if src_dir.exists():
        for d in src_dir.iterdir():
            if d.is_dir():
                dir_name = d.name
                # Skip non-agent directories
                if dir_name in ["__pycache__", ".pytest_cache", ".git", ".vscode", "node_modules"]:
                    continue
                # Skip hidden directories
                if dir_name.startswith("."):
                    continue
                
                # Check if it's a valid agent directory
                agent_files = ["__init__.py", "tools.py", "lifecycle.py"]
                has_required_files = all((d / file).exists() for file in agent_files)
                
                agents.append({
                    "name": dir_name,
                    "path": str(d),
                    "valid": has_required_files
                })
    
    return agents


def list_available_agents_for_deployment():
    """
    List all available agents for deployment
    """
    print("📋 Available agents for deployment")
    print("=" * 50)
    
    agents = list_available_agents()
    
    if not agents:
        print("❌ No agents found in src/ directory")
        print()
        print("To create a new agent:")
        print("1. Create directory: mkdir -p src/my_new_agent")
        print("2. Add required files: __init__.py, tools.py, lifecycle.py")
        print("3. Create config: configs/agents/my_new_agent.yaml")
        print("4. Run: python deploy_agent.py <sam_path> my_new_agent")
        return
    
    print(f"Found {len(agents)} agent(s):")
    print()
    for i, agent in enumerate(agents, 1):
        status = "✅ Valid" if agent["valid"] else "⚠️  Missing files"
        print(f"{i}. {agent['name']} - {status}")
        if not agent["valid"]:
            print(f"   Missing required files: __init__.py, tools.py, lifecycle.py")
        print(f"   Path: {agent['path']}")
        print()
    
    print("To deploy an agent:")
    print("python deploy_agent.py <sam_path> [agent_name] [--skip-deps]")
    print("or")
    print("python deploy_agent.py <sam_path> (to select interactively)")
    print()
    print("Options:")
    print("  --skip-deps    Skip automatic dependency installation")
    print("  --list         List available agents")


def create_sam_run_script(sam_install_path: str, agent_name: str):
    """Create a script to run the agent with SAM"""
    script_content = f"""#!/bin/bash
# SAM Run Script for {agent_name}
# Generated by deploy_to_sam.py

SAM_PATH="{sam_install_path}"
AGENT_CONFIG="$SAM_PATH/configs/agents/{agent_name}.yaml"

echo "🚀 Starting {agent_name} with SAM..."
echo "SAM Path: $SAM_PATH"
echo "Agent Name: {agent_name}"
echo "Config: $AGENT_CONFIG"

# Change to SAM directory
cd "$SAM_PATH"

# Run the agent
sam run "$AGENT_CONFIG"
"""
    
    script_path = Path(__file__).parent / "start_agent.sh"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(script_path, 0o755)
    
    print(f"✅ Created run script: {script_path}")
    return script_path


def main():
    """Main deployment function"""
    print("Generic Agent - SAM Deployment")
    print("=" * 40)
    
    # Parse command line arguments
    args = sys.argv[1:]
    skip_deps = False
    
    # Check for help flag
    if "--help" in args or "-h" in args:
        print_help()
        return
    
    # Check for --skip-deps flag
    if "--skip-deps" in args:
        skip_deps = True
        args.remove("--skip-deps")
    
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
        list_available_agents_for_deployment()
        return
    
    # Get agent name
    if len(args) > 1:
        agent_name = args[1]
    else:
        # List available agents and let user choose
        agents = list_available_agents()
        if not agents:
            print("❌ No agents found in src/ directory")
            sys.exit(1)
        
        print("📋 Available agents for deployment:")
        print("=" * 50)
        for i, agent in enumerate(agents, 1):
            status = "✅ Valid" if agent["valid"] else "⚠️  Missing files"
            print(f"{i}. {agent['name']} - {status}")
        print("0. Cancel")
        
        while True:
            try:
                choice = input(f"\nSelect agent to deploy (0-{len(agents)}): ").strip()
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
    
    print(f"🤖 Agent Name: {agent_name}")
    
    # Get agent source directory (optional)
    if len(args) > 2:
        agent_source_dir = args[2]
    else:
        # Use the selected agent's directory name
        agent_source_dir = agent_name
    
    # Deploy the agent
    success = deploy_to_sam(str(sam_path), agent_name, agent_source_dir, skip_deps)
    
    if success:
        # Create run script
        run_script = create_sam_run_script(str(sam_path), agent_name)
        
        print("\n" + "=" * 50)
        print("📋 Next Steps:")
        print("=" * 50)
        if skip_deps:
            print("1. Install dependencies manually:")
            print(f"   cd {sam_path}")
            print(f"   pip install -r src/{agent_name}/requirements.txt")
            print()
        else:
            print("1. Dependencies have been automatically installed! ✅")
            print(f"   Agent-specific dependencies installed from: src/{agent_name}/requirements.txt")
            print()
        print("2. Run the agent using the generated script:")
        print(f"   ./start_agent.sh")
        print()
        print("3. Or run manually:")
        print(f"   cd {sam_path}")
        print(f"   sam run configs/agents/{agent_name}.yaml")
        print()
        print("4. Test the agent:")
        print("   - Test in SAM: Ask the agent questions through the SAM interface")
        print("   - Run tests from source directory: cd src/{agent_name}/tests && python -m pytest -v")
        print("   - Note: Tests are not deployed to SAM (development files only)")
        print()
        print("5. For more information:")
        print(f"   - Read the agent README: src/{agent_name}/README.md")
        print(f"   - Check API reference: src/{agent_name}/API_REFERENCE.md")
        print()
        print("✅ Agent is ready to use!")
    else:
        print("❌ Deployment failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
