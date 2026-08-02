# 🛡️ Operation Black Tide: Project Chimera — CTF Challenge

> **An expert-level, story-driven Capture The Flag cybersecurity challenge.**

[![Live Demo](https://img.shields.io/badge/Play%20Now-Live-brightgreen?style=for-the-badge)](https://your-app.up.railway.app)

---

## About

**Operation Black Tide** is an immersive, multi-stage CTF challenge built around a fictional cyber breach. Players take on the role of a digital forensics investigator tasked with recovering **Project Chimera** — a classified weapon system stolen by the anonymous threat group *Black Tide*.

### 🎯 Challenge Stages

| Stage | Domain | Technique |
|---|---|---|
| **Stage 1** | Kali Linux (offline) | Polyglot JPEG/ZIP forensics, RSA shattered prime reconstruction, 91-Monolith Grid cipher, AES decryption |
| **Stage 2** | Web Terminal | Linux enumeration, SUID binary analysis, ROT13 cipher, privilege escalation |
| **Stage 3** | Web Terminal (root) | Multi-stage hash synthesis: `SHA256(FLAG1:FLAG2:TIMESTAMP)` |

### 🚩 Flags & Environment Variables

The application dynamically accepts flags passed via environment variables. If no environment variables are provided, the server falls back to default flags.

| Flag Variable | Default Fallback Value | Description |
|---|---|---|
| `FLAG1` (or `FLAG_1`) | `AEGIS{ENTRY-7D9A-88E2}` | Initial Foothold (Stage 1) |
| `FLAG2` (or `FLAG_2`) | `AEGIS{PRIV-C4F8-15B7}` | Root Access (Stage 2) |
| `FLAG3` (or `FLAG_3`) | `AEGIS{CHMR-E1A6-9D40}` | Project Chimera (Stage 3) |

---

## Self-Hosting

### Requirements
- Python 3.8+ (Uses standard library only, no external pip packages required) OR Docker

### Run Locally (Python 3)

```bash
git clone https://github.com/YOUR_USERNAME/operation-black-tide-ctf
cd operation-black-tide-ctf
python3 server.py
# Open http://localhost:3000
```

#### Running with Custom Environment Flags (Python 3)

**On Linux / macOS:**
```bash
FLAG1="AEGIS{CUSTOM-FLAG1-1234}" FLAG2="AEGIS{CUSTOM-FLAG2-5678}" FLAG3="AEGIS{CUSTOM-FLAG3-9012}" python3 server.py
```

**On Windows (PowerShell):**
```powershell
$env:FLAG1="AEGIS{CUSTOM-FLAG1-1234}"
$env:FLAG2="AEGIS{CUSTOM-FLAG2-5678}"
$env:FLAG3="AEGIS{CUSTOM-FLAG3-9012}"
python server.py
```

---

## 🐳 Running via Docker (Python 3)

### 1. Build Docker Image

```bash
docker build -t aegis-ctf-python .
```

### 2. Run Container (Default Flags)

```bash
docker run -d -p 3000:3000 --name aegis-ctf-app aegis-ctf-python
```
Access the application at `http://localhost:3000` (or `http://<YOUR_LOCAL_IP>:3000`).

### 3. Run Container with Custom Flags

```bash
docker run -d -p 3000:3000 \
  -e FLAG1="AEGIS{MY-CUSTOM-FLAG1-001}" \
  -e FLAG2="AEGIS{MY-CUSTOM-FLAG2-002}" \
  -e FLAG3="AEGIS{MY-CUSTOM-FLAG3-003}" \
  --name aegis-ctf-app aegis-ctf-python
```

### 4. Stop and Remove Container

```bash
docker stop aegis-ctf-app
docker rm aegis-ctf-app
```

---

## Deploy to Cloud

### Deploy to Railway / Render / Fly.io
1. Push this repo to GitHub.
2. Select Python 3 environment (or Dockerfile deployment).
3. Set environment variables `FLAG1`, `FLAG2`, `FLAG3` (optional).
4. Done!

---

## Tech Stack
- **Backend:** Python 3 (`http.server`, zero dependencies)
- **Frontend:** Vanilla HTML/CSS/JS (Dynamic Flag Tracking)
- **Containerization:** Docker (`python:3.11-alpine`)
- **CTF Engine:** In-memory virtual Linux filesystem with command emulation

---

*Aegis Secure // Operation Black Tide // Project Chimera CTF — v4.0*
