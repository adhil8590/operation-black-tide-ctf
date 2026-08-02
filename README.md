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

## For Players

1. Visit the live URL above
2. Click **DOWNLOAD BREACH SCENE EVIDENCE** to get the forensic package
3. Solve the offline Stage 1 challenges on a Linux machine (Kali recommended)
4. Use your findings to access the web terminal and complete Stages 2 & 3

---

## Self-Hosting

### Requirements
- Node.js 18+ OR Docker / Container Runtime

### Run Locally (Node.js)

```bash
git clone https://github.com/YOUR_USERNAME/operation-black-tide-ctf
cd operation-black-tide-ctf
npm install
npm start
# Open http://localhost:3000
```

#### Running with Custom Environment Flags (Node.js)

**On Linux / macOS:**
```bash
FLAG1="AEGIS{CUSTOM-FLAG1-1234}" FLAG2="AEGIS{CUSTOM-FLAG2-5678}" FLAG3="AEGIS{CUSTOM-FLAG3-9012}" npm start
```

**On Windows (PowerShell):**
```powershell
$env:FLAG1="AEGIS{CUSTOM-FLAG1-1234}"
$env:FLAG2="AEGIS{CUSTOM-FLAG2-5678}"
$env:FLAG3="AEGIS{CUSTOM-FLAG3-9012}"
npm start
```

---

## 🐳 Running via Docker

### 1. Build Docker Image

```bash
docker build -t aegis-ctf .
```

### 2. Run Container (Default Flags)

```bash
docker run -d -p 3000:3000 --name aegis-ctf-node aegis-ctf
```
Access the application at `http://localhost:3000`.

### 3. Run Container with Custom Flags

```bash
docker run -d -p 3000:3000 \
  -e FLAG1="AEGIS{MY-CUSTOM-FLAG1-001}" \
  -e FLAG2="AEGIS{MY-CUSTOM-FLAG2-002}" \
  -e FLAG3="AEGIS{MY-CUSTOM-FLAG3-003}" \
  --name aegis-ctf-node aegis-ctf
```

### 4. Stop and Remove Container

```bash
docker stop aegis-ctf-node
docker rm aegis-ctf-node
```

---

## Deploy to Cloud

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Fork this repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select this repo — Railway auto-detects Node.js / Dockerfile
4. Set environment variables `FLAG1`, `FLAG2`, `FLAG3` in Railway variables (optional)
5. Done! Get your public URL.

---

## Tech Stack
- **Backend:** Node.js + Express (also includes standalone `server.py`)
- **Frontend:** Vanilla HTML/CSS/JS (Dynamic Flag Tracking)
- **Containerization:** Docker (Alpine Linux base)
- **CTF Engine:** In-memory virtual Linux filesystem with command emulation

---

*Aegis Secure // Operation Black Tide // Project Chimera CTF — v4.0*
