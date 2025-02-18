#!/bin/bash
set -e

echo "Updating package lists..."
apt update -y

echo "Installing required packages..."
apt install -y curl wget git nano lsof net-tools htop unzip jq build-essential

echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "Downloading Llama3 model..."
ollama pull llama3.2

echo "Setup Complete!"
