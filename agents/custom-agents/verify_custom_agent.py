#!/usr/bin/env python3
"""
Verification script for any agent deployment
This script checks if the agent was deployed correctly to SAM
"""

import os
import sys
from pathlib import Path


def verify_deployment(sam_path: str, agent_name: str, agent_source_dir: str = None):
    """Verify that the agent was deployed correctly"""
    print(f"🔍 Verifying {agent_name} Deployment")
    print("=" * 50)
    
    sam_path = Path(sam_path)
    
    # Determine source directory
    if agent_source_dir is None:
        agent_source_dir = agent_name
    
    # Define expected paths (agent-specific only)
    expected_paths = {
        "agent_source": sam_path / "src" / agent_name,
        "agent_config": sam_path / "configs" / "agents" / f"{agent_name}.yaml",
        "requirements": sam_path / "src" / agent_name / "requirements.txt",
        "deployment_info": sam_path / "src" / agent_name / "deployment_info.txt"
    }
    
    all_good = True
    
    # Check main paths (agent-specific only)
    print("📁 Checking deployment paths...")
    for name, path in expected_paths.items():
        if path.exists():
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (MISSING)")
            all_good = False
    
    # Check agent source files dynamically
    print(f"\n📄 Checking agent source files...")
    agent_source = expected_paths["agent_source"]
    if agent_source.exists():
        # Check for core required files
        core_files = ["__init__.py", "tools.py", "lifecycle.py"]
        for file_name in core_files:
            file_path = agent_source / file_name
            if file_path.exists():
                print(f"✅ {file_name}")
            else:
                print(f"❌ {file_name} (MISSING)")
                all_good = False
        
        # Check services directory and its contents
        services_dir = agent_source / "services"
        if services_dir.exists() and services_dir.is_dir():
            print(f"✅ services/ (directory)")
            
            # Check for services/__init__.py
            services_init = services_dir / "__init__.py"
            if services_init.exists():
                print(f"✅ services/__init__.py")
            else:
                print(f"❌ services/__init__.py (MISSING)")
                all_good = False
            
            # Check for all Python files in services directory
            service_files = list(services_dir.glob("*.py"))
            if service_files:
                for service_file in service_files:
                    if service_file.name != "__init__.py":
                        print(f"✅ services/{service_file.name}")
            else:
                print(f"⚠️  No service files found in services/ directory")
        else:
            print(f"❌ services/ (MISSING)")
            all_good = False
        
        # Check for any additional directories or files
        additional_items = []
        for item in agent_source.iterdir():
            if item.is_dir() and item.name not in ["services", "__pycache__"]:
                additional_items.append(f"{item.name}/ (directory)")
            elif item.is_file() and item.suffix in [".py", ".md", ".txt"] and item.name not in ["__init__.py", "tools.py", "lifecycle.py"]:
                additional_items.append(item.name)
        
        if additional_items:
            print(f"\n📁 Additional files found:")
            for item in additional_items:
                print(f"✅ {item}")
    else:
        print(f"❌ Agent source directory not found")
        all_good = False
    
    # Check file contents
    print(f"\n🔍 Checking file contents...")
    
    # Check requirements.txt
    requirements_file = expected_paths["requirements"]
    if requirements_file.exists():
        with open(requirements_file, 'r') as f:
            content = f.read()
            if "solace-agent-mesh" in content and "httpx" in content:
                print(f"✅ requirements.txt contains required packages")
            else:
                print(f"❌ requirements.txt missing required packages")
                all_good = False
    else:
        print(f"❌ requirements.txt not found")
        all_good = False
    
    # Check lifecycle functions customization
    lifecycle_file = expected_paths["agent_source"] / "lifecycle.py"
    if lifecycle_file.exists():
        with open(lifecycle_file, 'r') as f:
            content = f.read()
            agent_name_underscore = agent_name.replace("-", "_").replace(" ", "_")
            source_name_underscore = agent_source_dir.replace("-", "_").replace(" ", "_")
            if f"initialize_{agent_name_underscore}" in content and f"cleanup_{agent_name_underscore}" in content:
                print(f"✅ Lifecycle functions customized for {agent_name}")
            else:
                print(f"❌ Lifecycle functions not customized for {agent_name}")
                all_good = False
    else:
        print(f"❌ Lifecycle file not found")
        all_good = False
    
    # Check agent config
    config_file = expected_paths["agent_config"]
    if config_file.exists():
        with open(config_file, 'r') as f:
            content = f.read()
            # Check for various forms of the agent name
            agent_name_clean = agent_name.replace("-", "").replace("_", "")
            agent_name_camel = "".join(word.capitalize() for word in agent_name.replace("-", " ").split())
            source_name_clean = agent_source_dir.replace("-", "").replace("_", "")
            
            # Check if any form of the agent name is in the config
            if (agent_name_clean in content or 
                agent_name_camel in content or 
                source_name_clean in content or
                agent_name in content):
                print(f"✅ Agent config contains required settings")
            else:
                print(f"❌ Agent config missing required settings")
                print(f"   Looking for: {agent_name_clean}, {agent_name_camel}, {source_name_clean}, or {agent_name}")
                all_good = False
    else:
        print(f"❌ Agent config not found")
        all_good = False
    
    # Check deployment info
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
    
    # Summary
    print(f"\n" + "=" * 50)
    if all_good:
        print("🎉 Deployment Verification: SUCCESS")
        print("✅ All files and directories are in place")
        print("✅ Agent is ready to run with SAM")
        
        print(f"\n📋 Next Steps:")
        print(f"1. Install dependencies:")
        print(f"   cd {sam_path}")
        print(f"   # Install base dependencies (if not already installed)")
        print(f"   pip install -r requirements.txt")
        print(f"   # Install agent-specific dependencies")
        print(f"   pip install -r src/{agent_name}/requirements.txt")
        print(f"")
        print(f"2. Run the agent:")
        print(f"   sam run configs/agents/{agent_name}.yaml")
        print(f"")
        print(f"3. Test the agent:")
        print(f"   # Run API tests")
        print(f"   cd src/{agent_name} && python tests/test_{agent_name}_api.py")
        print(f"   # Run unit tests")
        print(f"   cd src/{agent_name} && python -m pytest tests/test_{agent_name}.py -v")
        print(f"   # Test in SAM: Ask the agent questions through the SAM interface")
        
    else:
        print("❌ Deployment Verification: FAILED")
        print("❌ Some files or directories are missing")
        print("❌ Please re-run the deployment script")
        return False
    
    return True


def check_sam_environment(sam_path: str):
    """Check SAM environment setup"""
    print(f"\n🔧 Checking SAM Environment")
    print("=" * 30)
    
    sam_path = Path(sam_path)
    
    # Check if SAM CLI is available
    try:
        import subprocess
        
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
    
    # Check environment variables
    required_env_vars = [
        "SOLACE_HOST",
        "SOLACE_PORT", 
        "SOLACE_USERNAME",
        "SOLACE_PASSWORD",
        "OPENAI_API_KEY"
    ]
    
    print(f"\n🌍 Checking environment variables...")
    for var in required_env_vars:
        value = os.environ.get(var)
        if value:
            if "PASSWORD" in var or "KEY" in var:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
    
    return True


def main():
    """Main verification function"""
    print("Generic Agent - Deployment Verification")
    print("=" * 50)
    
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
        agent_name = input("Enter agent name (default: find_my_ip_agent): ").strip()
        if not agent_name:
            agent_name = "find_my_ip_agent"
    
    print(f"🤖 Agent Name: {agent_name}")
    
    # Get agent source directory (optional)
    agent_source_dir = None
    if len(sys.argv) > 3:
        agent_source_dir = sys.argv[3]
    
    # Verify deployment
    deployment_ok = verify_deployment(str(sam_path), agent_name, agent_source_dir)
    
    # Check SAM environment
    environment_ok = check_sam_environment(str(sam_path))
    
    # Final summary
    print(f"\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Deployment: {'✅ SUCCESS' if deployment_ok else '❌ FAILED'}")
    print(f"Environment: {'✅ READY' if environment_ok else '❌ ISSUES'}")
    
    if deployment_ok and environment_ok:
        print(f"\n🎉 Everything is ready! You can now run the agent.")
    elif deployment_ok and not environment_ok:
        print(f"\n⚠️  Agent is deployed but environment needs configuration.")
        print(f"   Please set up the required environment variables.")
    else:
        print(f"\n❌ Issues found. Please fix them before running the agent.")


if __name__ == "__main__":
    main()
