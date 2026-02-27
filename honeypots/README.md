# Honeypot Setup Guide

## Overview

This directory contains Docker-based honeypot containers for catching attacker activity.

## Current Setup

### 1. Cowrie (SSH/Telnet Honeypot)
- **Container**: `securesight_cowrie`
- **Image**: `cowrie/cowrie:latest`
- **Ports**:
  - `2222` → SSH honeypot
  - `2223` → Telnet honeypot

### 2. Dionaea (Multi-Protocol Honeypot)
- **Container**: `securesight_dionaea`
- **Image**: `dinotools/dionaea:latest`
- **Ports** (mapped to avoid conflicts):
  - `2121` → FTP
  - `8080` → HTTP
  - `8443` → HTTPS
  - `10445` → SMB
  - `11433` → MSSQL
  - `13306` → MySQL
  - `59312` → IPMI

## Quick Start

### Check Status
```bash
cd honeypots
docker ps
```

### View Logs
```bash
# Cowrie logs
docker logs securesight_cowrie

# Dionaea logs
docker logs securesight_dionaea

# JSON attack logs
type cowrie\logs\cowrie.json
```

### Stop/Start
```bash
docker-compose down    # Stop
docker-compose up -d   # Start
```

## Testing the Honeypots

### Test Cowrie (SSH)
```bash
ssh -p 2222 root@localhost
# Use any username/password - they will be logged!
```

### Test Dionaea (HTTP)
```bash
curl http://localhost:8080
```

## Backend Integration

The backend reads honeypot logs from:
- `honeypots/cowrie/logs/cowrie.json`

API Endpoints:
- `GET /api/v1/enhancements/honeypot/status` - Get honeypot status
- `GET /api/v1/enhancements/honeypot/cowrie` - Get Cowrie logs
- `GET /api/v1/enhancements/honeypot/dionaea` - Get Dionaea logs
- `GET /api/v1/enhancements/honeypot/analytics` - Get attack analytics

## Catching Real Attacks

To catch real attacks from the internet:

1. **Open ports on your firewall** to allow incoming connections
2. **Port forward from your router** to this machine
3. **Or use a cloud VPS** with a public IP

## Services Each Honeypot Catches

| Honeypot | Protocol | Common Attacks |
|----------|----------|-----------------|
| Cowrie | SSH (22) | Brute force, credential stuffing |
| Cowrie | Telnet (23) | IoT attacks, default passwords |
| Dionaea | FTP (21) | Anonymous login attempts |
| Dionaea | HTTP (80) | Web vulnerabilities, malware uploads |
| Dionaea | SMB (445) | WannaCry, EternalBlue exploits |
| Dionaea | MSSQL (1433) | Database attacks |
| Dionaea | MySQL (3306) | Database attacks |

## Security Notes

- These honeypots are designed to be exposed to the internet
- They log all attack attempts but don't execute them
- Monitor logs regularly for suspicious activity
- Consider using a separate network interface/VLAN for honeypots
