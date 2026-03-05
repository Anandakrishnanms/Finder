#!/bin/bash

echo "[*] Updating system..."
sudo apt update -y

echo "[*] Installing system dependencies..."
sudo apt install -y python3 python3-pip git curl golang

echo "[*] Installing Subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

echo "[*] Installing Assetfinder..."
go install github.com/tomnomnom/assetfinder@latest

echo "[*] Installing httprobe..."
go install github.com/tomnomnom/httprobe@latest

echo "[*] Installing Sublist3r..."
pip3 install sublist3r

echo "[*] Adding Go bin to PATH..."
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc

echo "[✔] Installation completed!"
echo "[!] Restart terminal or run: source ~/.bashrc"
