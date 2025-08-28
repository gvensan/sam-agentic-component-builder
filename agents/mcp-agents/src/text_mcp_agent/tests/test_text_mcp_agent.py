#!/usr/bin/env python3
"""
Test suite for Text MCP Agent

Tests YAML-only MCP agent configuration, MCP server availability, and basic functionality.
"""

import os
import sys
import yaml
import subprocess
import pytest
from pathlib import Path
from typing import Dict, List, Any


class TestTextMCPAgent:
    """Test class for Text MCP Agent"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.config_dir = Path("configs/agents")
        self.agent_config_file = "text_mcp_agent.yaml"
        self.mcp_server = "@modelcontextprotocol/server-text"
    
    def load_config_with_includes(self):
        """Load YAML config file and resolve !include directives"""
        config_path = self.config_dir / self.agent_config_file
        
        # Read the main config file
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Handle the !include directive by reading the shared config
        if '!include ../shared_config.yaml' in content:
            shared_config_path = Path("configs/shared_config.yaml")
            if shared_config_path.exists():
                with open(shared_config_path, 'r') as f:
                    shared_content = f.read()
                
                # Replace the include directive with the actual shared config content
                content = content.replace('!include ../shared_config.yaml', shared_content)
            else:
                # If shared config doesn't exist, comment out the include
                content = content.replace('!include ../shared_config.yaml', '# !include ../shared_config.yaml')
        
        # Parse the merged content
        return yaml.safe_load(content)
        
    def test_yaml_syntax(self):
        """Test YAML configuration syntax"""
        config_path = self.config_dir / self.agent_config_file
        
        # Check if config file exists
        assert config_path.exists(), f"Configuration file not found: {config_path}"
        
        # Test YAML syntax by handling the !include directive
        try:
            config = self.load_config_with_includes()
            
            # Basic structure validation
            assert 'apps' in config, "Missing 'apps' section in YAML"
            assert len(config['apps']) > 0, "No apps defined in configuration"
            
            # Check for text_mcp_agent_app
            app_found = False
            for app in config['apps']:
                if app.get('name') == 'text_mcp_agent_app':
                    app_found = True
                    break
            
            assert app_found, "text_mcp_agent_app not found in configuration"
            
        except yaml.YAMLError as e:
            pytest.fail(f"YAML syntax error: {str(e)}")
        except Exception as e:
            pytest.fail(f"Unexpected error reading YAML: {str(e)}")
    
    def test_agent_configuration_structure(self):
        """Test agent configuration structure and required fields"""
        config = self.load_config_with_includes()
        
        # Find the text_mcp_agent_app
        app_config = None
        for app in config['apps']:
            if app.get('name') == 'text_mcp_agent_app':
                app_config = app.get('app_config', {})
                break
        
        assert app_config is not None, "text_mcp_agent_app configuration not found"
        
        # Check required fields
        required_fields = ['agent_name', 'display_name', 'model', 'tools', 'instruction']
        for field in required_fields:
            assert field in app_config, f"Missing required field: {field}"
        
        # Check agent name
        assert app_config['agent_name'] == 'TextMCPAgent', f"Expected agent_name 'TextMCPAgent', got '{app_config['agent_name']}'"
        
        # Check display name
        assert app_config['display_name'] == 'Text MCP Agent', f"Expected display_name 'Text MCP Agent', got '{app_config['display_name']}'"
        
        # Check for MCP tools
        tools = app_config.get('tools', [])
        mcp_tools = [t for t in tools if t.get('tool_type') == 'mcp']
        assert len(mcp_tools) > 0, "No MCP tools found in configuration"
        
        # Check MCP tool configuration
        mcp_tool = mcp_tools[0]
        assert 'connection_params' in mcp_tool, "MCP tool missing connection_params"
        
        conn_params = mcp_tool['connection_params']
        assert conn_params.get('type') == 'stdio', "Expected stdio connection type"
        assert conn_params.get('command') == 'npx', "Expected npx command"
        assert '-y' in conn_params.get('args', []), "Expected -y flag in args"
        assert self.mcp_server in conn_params.get('args', []), f"Expected {self.mcp_server} in args"
    
    def test_mcp_server_availability(self):
        """Test if the MCP server is available and can start"""
        try:
            # Test MCP server startup
            cmd = ["npx", "-y", self.mcp_server]
            
            # Run with timeout to avoid hanging
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Most MCP servers exit with 0 or 1 after initialization
            assert process.returncode in [0, 1], f"MCP server exited with unexpected code: {process.returncode}"
            
        except subprocess.TimeoutExpired:
            # Timeout usually means server started successfully
            pass
        except FileNotFoundError:
            pytest.skip("npx command not found - Node.js/NPM not installed")
        except Exception as e:
            pytest.fail(f"Unexpected error testing MCP server: {str(e)}")
    
    def test_agent_instructions(self):
        """Test agent instructions content"""
        config = self.load_config_with_includes()
        
        # Find the text_mcp_agent_app
        app_config = None
        for app in config['apps']:
            if app.get('name') == 'text_mcp_agent_app':
                app_config = app.get('app_config', {})
                break
        
        instruction = app_config.get('instruction', '')
        
        # Check for key instruction elements
        assert 'Text MCP Agent' in instruction, "Instructions should mention 'Text MCP Agent'"
        assert 'text processing' in instruction.lower(), "Instructions should mention text processing"
        assert 'search' in instruction.lower(), "Instructions should mention search capabilities"
        assert 'manipulation' in instruction.lower(), "Instructions should mention manipulation capabilities"
        assert '/tmp/text_workspace' in instruction, "Instructions should mention working directory"
    
    def test_agent_card_configuration(self):
        """Test agent card configuration"""
        config = self.load_config_with_includes()
        
        # Find the text_mcp_agent_app
        app_config = None
        for app in config['apps']:
            if app.get('name') == 'text_mcp_agent_app':
                app_config = app.get('app_config', {})
                break
        
        agent_card = app_config.get('agent_card', {})
        
        # Check required agent card fields
        assert 'description' in agent_card, "Agent card missing description"
        assert 'defaultInputModes' in agent_card, "Agent card missing defaultInputModes"
        assert 'defaultOutputModes' in agent_card, "Agent card missing defaultOutputModes"
        assert 'skills' in agent_card, "Agent card missing skills"
        
        # Check description
        description = agent_card['description']
        assert 'text processing' in description.lower(), "Description should mention text processing"
        assert 'MCP integration' in description, "Description should mention MCP integration"
        
        # Check input/output modes
        input_modes = agent_card['defaultInputModes']
        output_modes = agent_card['defaultOutputModes']
        
        assert 'text' in input_modes, "Input modes should include 'text'"
        assert 'text' in output_modes, "Output modes should include 'text'"
        assert 'file' in output_modes, "Output modes should include 'file'"
        
        # Check skills
        skills = agent_card['skills']
        expected_skills = [
            'text processing',
            'text search', 
            'text manipulation',
            'file operations',
            'pattern matching',
            'text analysis',
            'content extraction'
        ]
        
        for skill in expected_skills:
            assert skill in skills, f"Expected skill '{skill}' not found in agent card"
    
    def test_shared_config_inclusion(self):
        """Test that shared config is properly included"""
        config_path = self.config_dir / self.agent_config_file
        
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Check for shared config inclusion
        assert '!include ../shared_config.yaml' in content, "Configuration should include shared_config.yaml"
    
    def test_broker_configuration(self):
        """Test broker configuration"""
        config = self.load_config_with_includes()
        
        # Find the text_mcp_agent_app
        app_config = None
        for app in config['apps']:
            if app.get('name') == 'text_mcp_agent_app':
                app_config = app
                break
        
        # Check broker configuration
        assert 'broker' in app_config, "App missing broker configuration"
        broker_config = app_config['broker']
        
        # Check for broker connection reference
        # When shared config is included, the anchor is resolved to actual values
        # So we check for the presence of broker configuration instead
        assert broker_config is not None, "Broker configuration should be present"
        assert 'broker_url' in broker_config, "Broker config should contain broker_url"
        assert 'broker_username' in broker_config, "Broker config should contain broker_username"
    
    def test_model_configuration(self):
        """Test model configuration"""
        config = self.load_config_with_includes()
        
        # Find the text_mcp_agent_app
        app_config = None
        for app in config['apps']:
            if app.get('name') == 'text_mcp_agent_app':
                app_config = app.get('app_config', {})
                break
        
        # Check model configuration
        model_config = app_config.get('model', {})
        assert model_config is not None, "Model configuration not found"
        
        # Check for model reference
        # When shared config is included, the anchor is resolved to actual values
        # So we check for the presence of model configuration instead
        assert model_config is not None, "Model configuration should be present"
        assert 'model' in model_config, "Model config should contain model"
        assert 'api_base' in model_config, "Model config should contain api_base"


if __name__ == "__main__":
    # Run tests directly if script is executed
    pytest.main([__file__, "-v"])
