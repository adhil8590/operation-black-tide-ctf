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

### 🚩 Flags to Recover
- `AEGIS{ENTRY-7D9A-88E2}` — Initial Foothold (Stage 1)
- `AEGIS{PRIV-C4F8-15B7}` — Root Access (Stage 2)
- `AEGIS{CHMR-E1A6-9D40}` — Project Chimera (Stage 3)

---

## For Players

1. Visit the live URL above
2. Click **DOWNLOAD BREACH SCENE EVIDENCE** to get the forensic package
3. Solve the offline Stage 1 challenges on a Linux machine (Kali recommended)
4. Use your findings to access the web terminal and complete Stages 2 & 3

---

## Self-Hosting

### Requirements
- Node.js 18+
- A Kali Linux VM (for players — for the offline Stage 1 evidence pack)

### Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/operation-black-tide-ctf
cd operation-black-tide-ctf
npm install
npm start
# Open http://localhost:3000
```

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Fork this repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select this repo — Railway auto-detects Node.js
4. Done! Get your public URL.

---

## Tech Stack
- **Backend:** Node.js + Express
- **Frontend:** Vanilla HTML/CSS/JS
- **CTF Engine:** In-memory virtual Linux filesystem with command emulation

---

*Aegis Secure // Operation Black Tide // Project Chimera CTF — v4.0*
