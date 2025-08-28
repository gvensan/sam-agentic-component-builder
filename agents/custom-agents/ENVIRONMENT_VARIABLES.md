# Environment Variables Reference

This document outlines all the environment variables required for the SAM agent deployment.

## 🔧 Required Environment Variables

### Broker Configuration
```bash
# Solace Broker Connection
SOLACE_BROKER_URL="ws://localhost:8008"          # WebSocket URL for broker
SOLACE_BROKER_USERNAME="default"                 # Broker username
SOLACE_BROKER_PASSWORD="default"                 # Broker password
SOLACE_BROKER_VPN="default"                      # Broker VPN name
SOLACE_DEV_MODE="false"                          # Development mode flag
USE_TEMPORARY_QUEUES="true"                      # Use temporary queues
```

### LLM Service Configuration
```bash
# LLM Service Endpoints
LLM_SERVICE_ENDPOINT="http://localhost:8000"     # LLM service base URL
LLM_SERVICE_API_KEY="your-api-key"               # LLM service API key

# Model Names
LLM_SERVICE_PLANNING_MODEL_NAME="gpt-4"          # Planning model
LLM_SERVICE_GENERAL_MODEL_NAME="gpt-4"           # General model
LLM_REPORT_MODEL_NAME="gpt-4"                    # Report generation model

# Image Generation (Optional)
IMAGE_MODEL_NAME="dall-e-3"                      # Image generation model
IMAGE_SERVICE_ENDPOINT="http://localhost:8001"   # Image service URL
IMAGE_SERVICE_API_KEY="your-image-api-key"       # Image service API key
```

### SAM Configuration
```bash
# Namespace and General Settings
NAMESPACE="samv1"                                # Agent namespace
SOLACE_DEV_MODE="false"                          # Development mode
```

## 📋 Example .env File

```bash
# Copy this to your SAM installation directory as .env

# Broker Configuration
SOLACE_BROKER_URL="ws://localhost:8008"
SOLACE_BROKER_USERNAME="default"
SOLACE_BROKER_PASSWORD="default"
SOLACE_BROKER_VPN="default"
SOLACE_DEV_MODE="false"
USE_TEMPORARY_QUEUES="true"

# LLM Service Configuration
LLM_SERVICE_ENDPOINT="http://localhost:8000"
LLM_SERVICE_API_KEY="your-api-key"
LLM_SERVICE_PLANNING_MODEL_NAME="gpt-4"
LLM_SERVICE_GENERAL_MODEL_NAME="gpt-4"
LLM_REPORT_MODEL_NAME="gpt-4"

# Image Generation (Optional)
IMAGE_MODEL_NAME="dall-e-3"
IMAGE_SERVICE_ENDPOINT="http://localhost:8001"
IMAGE_SERVICE_API_KEY="your-image-api-key"

# SAM Configuration
NAMESPACE="samv1"
SOLACE_DEV_MODE="false"
```

## 🔍 Validation

To validate your environment variables, run:
```bash
# Check if all required variables are set
env | grep -E "(SOLACE_|LLM_|NAMESPACE|USE_TEMPORARY)"
```

## ⚠️ Important Notes

1. **Broker URL**: Must be a valid WebSocket URL (ws:// or wss://)
2. **Namespace**: Should not contain trailing slashes
3. **API Keys**: Keep these secure and never commit to version control
4. **Development Mode**: Set to "true" for development, "false" for production

## 🚀 Quick Setup

1. Copy the example .env content to your SAM installation directory
2. Update the values according to your setup
3. Restart SAM to load the new environment variables
