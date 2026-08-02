# 🚀 OPERATION BLACK TIDE: PROJECT CHIMERA
## Complete Deployment & Hosting Operational Guide

This document provides step-by-step instructions for hosting, deploying, and configuring **Operation Black Tide CTF** across any environment — including Localhost, Docker containers, and Cloud Hosting platforms (Railway, Render, Fly.io, VPS).

---

## 📋 Table of Contents
1. [Overview & Features](#-overview--features)
2. [Method 1: Running Locally via Python 3](#-method-1-running-locally-via-python-3)
3. [Method 2: Docker Container Deployment (Recommended)](#-method-2-docker-container-deployment-recommended)
4. [Method 3: Deploying to Cloud Platforms (Railway / Render / VPS)](#-method-3-deploying-to-cloud-platforms)
5. [How Dynamic Flag Synchronization Works](#-how-dynamic-flag-synchronization-works)
6. [Troubleshooting & Best Practices](#-troubleshooting--best-practices)

---

## ℹ️ Overview & Features

- **Multi-Stage Architecture**: Stage 1 (Evidence Pack Forensics), Stage 2 (Web Terminal PrivEsc), Stage 3 (Project Chimera Unsealing).
- **Dynamic Flag Support**: Supports custom CTF flags configured via `Dockerfile` or runtime Environment Variables (`FLAG1`, `FLAG2`, `FLAG3`).
- **Auto-Sync Evidence Builder**: On server startup, `server.py` automatically rebuilds `blacktide_evidence.zip` so that offline cracking results **always match** the server's live flags.
- **Zero External Dependencies**: Pure Python implementation — runs out-of-the-box on standard Python 3.8+ or Alpine Linux containers.

---

## 🐍 Method 1: Running Locally via Python 3

### Prerequisites
- Python 3.8 or higher installed on your system.

### 1. Default Execution
Clone the repository and start the server:
```bash
git clone https://github.com/adhil8590/operation-black-tide-ctf.git
cd operation-black-tide-ctf
python server.py
```
Open your browser and navigate to: `http://localhost:3000` (or `http://<YOUR_LOCAL_IP>:3000`).

---

### 2. Running with Custom Flags

#### On Linux / macOS (Terminal):
```bash
FLAG1="AEGIS{MY-CUSTOM-FLAG1-1234}" FLAG2="AEGIS{MY-CUSTOM-FLAG2-5678}" FLAG3="AEGIS{MY-CUSTOM-FLAG3-9012}" python3 server.py
```

#### On Windows (PowerShell):
```powershell
$env:FLAG1="AEGIS{MY-CUSTOM-FLAG1-1234}"
$env:FLAG2="AEGIS{MY-CUSTOM-FLAG2-5678}"
$env:FLAG3="AEGIS{MY-CUSTOM-FLAG3-9012}"
python server.py
```

#### On Windows (Command Prompt / CMD):
```cmd
set FLAG1=AEGIS{MY-CUSTOM-FLAG1-1234} && set FLAG2=AEGIS{MY-CUSTOM-FLAG2-5678} && set FLAG3=AEGIS{MY-CUSTOM-FLAG3-9012} && python server.py
```

---

## 🐳 Method 2: Docker Container Deployment (Recommended)

Docker provides an isolated, reliable environment for hosting CTF events.

### Step 1: Configuring Flags (Two Options)

#### Option A: Edit the `Dockerfile` directly
Open `Dockerfile` and update lines 15–17:
```dockerfile
ENV FLAG1="AEGIS{YOUR-CUSTOM-FLAG-1}"
ENV FLAG2="AEGIS{YOUR-CUSTOM-FLAG-2}"
ENV FLAG3="AEGIS{YOUR-CUSTOM-FLAG-3}"
```

#### Option B: Pass flags at container launch (No editing required)
You can leave `Dockerfile` as is and supply custom flags at runtime via `-e` flags.

---

### Step 2: Build the Docker Image
Run the following command in the project root directory:
```bash
docker build -t aegis-ctf-app .
```

To force a fresh rebuild without caching:
```bash
docker build --no-cache -t aegis-ctf-app .
```

---

### Step 3: Run the Docker Container

#### Default Flags:
```bash
docker run -d -p 3000:3000 --name aegis-ctf-instance aegis-ctf-app
```

#### Custom Flags via Runtime Environment Variables:
```bash
docker run -d -p 3000:3000 \
  -e FLAG1="AEGIS{ENTRY-CUSTOM-001}" \
  -e FLAG2="AEGIS{PRIV-CUSTOM-002}" \
  -e FLAG3="AEGIS{CHMR-CUSTOM-003}" \
  --name aegis-ctf-instance aegis-ctf-app
```

Access the CTF at `http://localhost:3000` or `http://<SERVER_IP>:3000`.

---

### Step 4: Useful Docker Commands

- **View Live Server Logs**:
  ```bash
  docker logs -f aegis-ctf-instance
  ```
- **Stop the Container**:
  ```bash
  docker stop aegis-ctf-instance
  ```
- **Restart the Container**:
  ```bash
  docker restart aegis-ctf-instance
  ```
- **Remove Container**:
  ```bash
  docker rm -f aegis-ctf-instance
  ```

---

## ☁️ Method 3: Deploying to Cloud Platforms

### 1. Railway.app (Easiest Cloud Setup)
1. Push your CTF repository to GitHub.
2. Log in to [Railway.app](https://railway.app) and create a **New Project** -> **Deploy from GitHub repo**.
3. Railway automatically detects the `Dockerfile`.
4. Navigate to **Variables** tab in Railway dashboard and add:
   - `FLAG1` = `AEGIS{YOUR-CUSTOM-FLAG1}`
   - `FLAG2` = `AEGIS{YOUR-CUSTOM-FLAG2}`
   - `FLAG3` = `AEGIS{YOUR-CUSTOM-FLAG3}`
5. Railway automatically sets `$PORT` and exposes your CTF URL.

---

### 2. Render.com
1. Create a **New Web Service** on [Render.com](https://render.com).
2. Connect your GitHub repository.
3. Select **Docker** as the Environment.
4. Under **Environment Variables**, add `FLAG1`, `FLAG2`, and `FLAG3`.
5. Click **Deploy**.

---

### 3. VPS Deployment (Ubuntu / Debian Server with Docker Compose)

Create a `docker-compose.yml` file on your VPS:
```yaml
version: '3.8'
services:
  aegis-ctf:
    build: .
    ports:
      - "80:3000"
    environment:
      - FLAG1=AEGIS{ENTRY-PROD-9901}
      - FLAG2=AEGIS{PRIV-PROD-9902}
      - FLAG3=AEGIS{CHMR-PROD-9903}
    restart: always
```

Start the CTF service:
```bash
docker-compose up -d --build
```

---

## 🔄 How Dynamic Flag Synchronization Works

A common failure in CTFs occurs when a participant cracks an offline evidence zip, gets a flag, but the website rejects it because the server was started with a different flag.

**Operation Black Tide eliminates this error automatically:**
1. Whenever `server.py` starts (locally, in Docker, or in the cloud), it checks `FLAG1`, `FLAG2`, and `FLAG3`.
2. It executes `build_evidence.py` during startup to dynamically re-encrypt `encrypted_entry.bin` using the active `FLAG1`.
3. It updates `public/downloads/blacktide_evidence.zip`.
4. When a player downloads the evidence package and runs `python3 decrypt_entry.py BT_COPPERSMITH_AES_2026!`, the output **guarantees** exact alignment with the server's live flag.

---

## 🛡️ Troubleshooting & Best Practices

| Common Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Port 3000 already in use** | Another service is using port 3000 | Set `PORT=8080` environment variable or run `docker run -p 8080:3000 ...` |
| **Docker build uses old cached files** | Docker layer caching | Build using `docker build --no-cache -t aegis-ctf-app .` |
| **Players cannot connect over LAN** | Firewall blocking port 3000 | Allow inbound TCP traffic on port 3000 in host firewall settings. |
| **Container stops immediately** | Unhandled runtime exception | Run `docker logs aegis-ctf-instance` to view exact error traceback. |

---

*Operation Black Tide CTF — Deployment & Operations Guide v4.0*
