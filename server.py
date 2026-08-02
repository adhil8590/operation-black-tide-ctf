#!/usr/bin/env python3
"""
Aegis Secure CTF Web Server & Terminal Emulation Engine (EXPERT / HARDCORE EDITION)
Operation Black Tide: Project Chimera
"""
import os
import sys
import json
import urllib.parse
import hashlib
import uuid
import threading
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 3000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

# -------------------------------------------------------------
# CTF Target Flags & Constants
# -------------------------------------------------------------
FLAG1 = os.environ.get("FLAG1") or os.environ.get("FLAG_1") or "AEGIS{ENTRY-7D9A-88E2}"
FLAG2 = os.environ.get("FLAG2") or os.environ.get("FLAG_2") or "AEGIS{PRIV-C4F8-15B7}"
FLAG3 = os.environ.get("FLAG3") or os.environ.get("FLAG_3") or "AEGIS{CHMR-E1A6-9D40}"

FINAL_MESSAGE = "Congratulations, Investigator. You successfully reconstructed Black Tide's attack chain and recovered Project Chimera before it was permanently lost. The world may never know how close it came to disaster—but thanks to your skills, the mission was a success."

# In-memory session store
sessions = {}

# -------------------------------------------------------------
# Simulated Virtual Filesystem (EXPERT EDITION)
# -------------------------------------------------------------
FILESYSTEM = {
    "/home/analyst": {
        "readme_staging.txt": """==================================================
AEGIS STAGING NODE-04 — INTERCEPTED OPERATIONAL LOG
==================================================
Log Entry #409-B: Operative Black Tide breached staging sector 'aegis-staging-node-04'.

CRYPTIC INVESTIGATION DOSSIER:
• "Shadows lurk in the central audit logs of /var/log where intercepted memory traces whisper of the forbidden vault."
• "The root key lies guarded behind the AST-Lambda entity residing in the sacred binary paths of /opt/aegis/bin."
• "When the crown of elevated authority is seized, the subterranean vaults of /var/backups will yield the Chimera vessel."
==================================================""",
        ".bash_history": """cat /etc/issue
id
uname -a
ls -la /opt/aegis/bin
/opt/aegis/bin/vault_check
cat /var/log/blacktide_audit.log
strings /opt/aegis/bin/vault_check
export TEMP_KEY=test
export AEGIS_AUTH=123
export VAULT_KEY=???
python3 old_script.py
""",
        "notes.txt": "[CODED TRANSMISSION MEMO #77]\n'The guardian binary at /opt/aegis/bin/vault_check seeks an invisible aura in the environment known to operatives as VAULT_KEY. Seek the audit footprints recorded in /var/log to decipher its secret resonance.'",
        "old_script.py": "# STAGED RECOVERY SCRIPT — PHANTOM BUILD (2025)\n# DECRYPTION_VECTOR = 'AEGIS_OLD_STAGING_KEY_2025'\n# BUILD STATUS: decommissioned — see /var/backups for active vessel"
    },
    "/opt/aegis/bin": {
        "vault_check": """[OBFUSCATED AST-LAMBDA SUID BINARY - AEGIS VAULT VERIFIER v4.2]
(lambda _:(lambda __:(lambda ___:___(___)))(lambda ___:lambda ____:____(lambda _____:___(___)(____)(_____))))(lambda _:lambda __:lambda ___:___ if __ == 0 else _(_ - 1)(__)(___))(24)
Owned by root:root (rwsr-xr-x)
Cryptic Inscription: "The AST gate measures 24 glyphs in length. Pass the environmental vector VAULT_KEY to awaken the root spirit."
"""
    },
    "/opt/aegis/tools": {
        "decrypt_chimera.py": """# Aegis Project Chimera Recovery Tool v4.0 (EXPERT DUAL-FLAG + TIME SEEDED SHA-256)
# Usage: python3 /opt/aegis/tools/decrypt_chimera.py --key <DERIVED_HASH_KEY>
# The Iron Forge leaves sixty-four marks upon every worthy seal. Bind First and Second Sigils with the Ancient Clock, joined by twin-dot monoliths.
"""
    },
    "/var/log": {
        "blacktide_audit.log": """[2026-07-30 02:14:09] ALERT: Unauthorized intrusion attempt on the AST-Lambda guardian (/opt/aegis/bin/vault_check).
[2026-07-30 02:14:15] AUDIT: Operative Black Tide injected dynamic environment vector VAULT_KEY.
[2026-07-30 02:15:01] INTERCEPTED MEMORY TRACE: "The AST gate measures 24 glyphs in length. Operative Echo inscribed the key by reflecting the cipher 'BlackTide_Root_Override' through the 13th mirror of Caesar..."
[2026-07-30 02:15:44] SYSTEM RECORD: Royal clearance unlocks the sanctuary chamber at /root/privilege_flag.txt.
""",
        "auth_failure_old.log": "[2026-07-29 18:22:01] FAILED LOGIN: user admin from IP 192.168.1.100 (Token AEGIS{FAKE-ENTRY-TOKEN-99})"
    },
    "/var/backups": {
        "project_chimera_v4.enc": "[SEALED CHIMERA VESSEL — IRON-LOCKED ARCHIVE — 48.2 MB]\nStatus: BOUND BY BLACK TIDE",
        "chimera_clue_manifest.txt": """==================================================
PROJECT CHIMERA — THE SEAL OF DUAL TRUTHS
==================================================
The First Sigil (FLAG 1) and Second Sigil (FLAG 2) were never meant to stand alone.
The forgotten clock time from the first trial remembers their meeting.

The Guardian watches with two eyes.

To unseal Chimera's chest in /var/backups:
1. Combine the First Sigil (FLAG 1), the Second Sigil (FLAG 2), and the Ancient Clock Seed recovered from Stage 1.
2. Join all three in order using the twin-dot monoliths (':') as separators:
   "FLAG1:FLAG2:CLOCK_SEED"
3. Pass the combined string through the 256-bit Iron Forge (producing a 64-character hex key).
4. Present the resulting key to the Chimera recovery vessel:
   python3 /opt/aegis/tools/decrypt_chimera.py --key <SIXTY_FOUR_MARK_IRON_SEAL>
==================================================
""",
        "chimera_v3_old.bak": "[CORRUPTED DECOY ARCHIVE - INVALID HEADER]",
        "unused_env.conf": "# UNUSED DATABASE CONFIG\nDATABASE_PASS=Admin_Unused_123!"
    },
    "/root": {
        "privilege_flag.txt": f"==================================================\nFLAG 2 (PRIVILEGE ESCALATION RECOVERED):\n{FLAG2}\n==================================================\n\nSanctuary Record: Root clearance achieved! Proceed to /var/backups and synthesize the dual-flag seal combined with the ancient clock seed to unseal Project Chimera!",
        "master_audit.db": "[SQLITE3 DATABASE - 14 TABLES] Confidential Security Audit Data"
    }
}

# -------------------------------------------------------------
# Terminal Command Engine Logic
# -------------------------------------------------------------
def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "authenticated": False,
            "user": "analyst",
            "is_root": False,
            "cwd": "/home/analyst",
            "env": {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/aegis/bin"},
            "solved_flags": []
        }
    return sessions[session_id]

def mirror_shift(s, n=13):
    """Caesar mirror — shifts each letter by n positions (13 by default)"""
    out = []
    for c in s:
        if 'a' <= c <= 'z':
            out.append(chr((ord(c) - ord('a') + n) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            out.append(chr((ord(c) - ord('A') + n) % 26 + ord('A')))
        else:
            out.append(c)
    return "".join(out)

def process_terminal_command(session, cmd_str):
    cmd_str = cmd_str.strip()
    if not cmd_str:
        return ""

    parts = cmd_str.split()
    cmd = parts[0]
    args = parts[1:]

    if cmd_str.startswith("export "):
        eq_part = cmd_str[7:].strip()
        if "=" in eq_part:
            k, v = eq_part.split("=", 1)
            session["env"][k.strip()] = v.strip().strip('"').strip("'")
            return f"Environment variable {k.strip()} set."
        else:
            return "Usage: export KEY=VALUE"

    if cmd == "env":
        return "\n".join([f"{k}={v}" for k, v in session["env"].items()])

    if cmd == "clear":
        return "__CLEAR__"

    if cmd == "whoami":
        return session["user"]

    if cmd == "id":
        if session["is_root"]:
            return "uid=0(root) gid=0(root) groups=0(root)"
        else:
            return "uid=1001(analyst) gid=1001(analyst) groups=1001(analyst),27(sudo)"

    if cmd == "pwd":
        return session["cwd"]

    if cmd == "sudo" and len(args) > 0 and args[0] == "-l":
        return """Matching Defaults entries for analyst on aegis-staging:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\\:/usr/local/bin\\:/usr/sbin\\:/usr/bin\\:/sbin\\:/bin\\:/opt/aegis/bin

User analyst may run the following commands on aegis-staging:
    (root) NOPASSWD: /opt/aegis/bin/vault_check
"""

    if cmd == "cd":
        target = args[0] if args else "/home/analyst"
        if target == "..":
            if session["cwd"] != "/":
                session["cwd"] = os.path.dirname(session["cwd"])
                if session["cwd"] == "":
                    session["cwd"] = "/"
            return ""
        elif target.startswith("/"):
            new_path = target
        else:
            new_path = os.path.normpath(os.path.join(session["cwd"], target)).replace("\\", "/")
        
        if new_path == "/root" and not session["is_root"]:
            return "bash: cd: /root: Permission denied"
        if new_path in FILESYSTEM or new_path in ["/", "/home", "/opt", "/opt/aegis", "/var"]:
            session["cwd"] = new_path
            return ""
        else:
            return f"bash: cd: {target}: No such file or directory"

    if cmd == "ls":
        target = session["cwd"]
        if args and not args[0].startswith("-"):
            target = args[0]
            if not target.startswith("/"):
                target = os.path.normpath(os.path.join(session["cwd"], target)).replace("\\", "/")
        
        if target == "/root" and not session["is_root"]:
            return "ls: cannot open directory '/root': Permission denied"

        if target in FILESYSTEM:
            files = list(FILESYSTEM[target].keys())
            if "-la" in args or "-l" in args:
                lines = ["total 24", "drwxr-xr-x 2 analyst analyst 4096 Jul 30 02:00 .", "drwxr-xr-x 4 root    root    4096 Jul 30 02:00 .."]
                for f in files:
                    perm = "-rwsr-xr-x 1 root root" if f == "vault_check" else "-rw-r--r-- 1 analyst analyst"
                    lines.append(f"{perm} 2048 Jul 30 02:15 {f}")
                return "\n".join(lines)
            return "  ".join(files)
        elif target in ["/", "/home", "/opt", "/var"]:
            dirs = {
                "/": ["home", "opt", "var", "root", "etc", "tmp"],
                "/home": ["analyst"],
                "/opt": ["aegis"],
                "/var": ["log", "backups"]
            }
            return "  ".join(dirs.get(target, []))
        else:
            return f"ls: cannot access '{target}': No such file or directory"

    if cmd == "cat":
        if not args:
            return "Usage: cat <filename>"
        fname = args[0]
        if "/" in fname:
            path_dir = os.path.dirname(fname)
            file_basename = os.path.basename(fname)
        else:
            path_dir = session["cwd"]
            file_basename = fname

        if path_dir == "/root" and not session["is_root"]:
            return f"cat: {fname}: Permission denied"

        if path_dir in FILESYSTEM and file_basename in FILESYSTEM[path_dir]:
            content = FILESYSTEM[path_dir][file_basename]
            if file_basename == "privilege_flag.txt" and session["is_root"]:
                if FLAG2 not in session["solved_flags"]:
                    session["solved_flags"].append(FLAG2)
            return content
        else:
            return f"cat: {fname}: No such file or directory"

    if cmd in ["strings", "/opt/aegis/bin/vault_check", "./vault_check", "vault_check"]:
        if "vault_check" in cmd_str:
            target_val1 = mirror_shift("BlackTide_Root_Override")
            target_val2 = "OynpxGvqr_Ebbg_Bireevqr"
            target_val3 = "BlackTide_Root_7d9a88e2_24"
            current_vk = session["env"].get("VAULT_KEY", "")

            if cmd == "strings":
                return """/lib64/ld-linux-x86-64.so.2
__gmon_start__
AEGIS_VAULT_SECURITY_CORE_v4.2 (AST-LAMBDA EVAL ENGINE)
Reading environment aura: VAULT_KEY...
INSCRIPTION: "The name they used to break in — seen backwards through Caesar's thirteenth mirror — is the only key this gate will accept."
Aura verified. Awakening root spirit.
"""
            
            if current_vk in [target_val1, target_val2, target_val3, "BlackTide_Root_Override"] or len(current_vk) == 24:
                session["is_root"] = True
                session["user"] = "root"
                if FLAG2 not in session["solved_flags"]:
                    session["solved_flags"].append(FLAG2)
                return f"""[+] The AST-Lambda gate accepted the aura.
[+] Root spirit awakened within the Aegis Security Core.
[+] The crown of the system now rests on your head.

[SECOND SIGIL RECOVERED]: {FLAG2}

[BLACK TIDE WHISPER]: "You earned that. Not many reach this far.
 The final chest lies in the forgotten vault at /var/backups.
 Everything you have recovered must be bound together before it opens."
"""
            else:
                return f"""[-] The gate rejected the aura.
Presented aura: '{current_vk}'
[The gate is silent. The answer lies in the memory fragments scattered through the server logs, and in the words carved into the binary itself.]"""

    if cmd == "find":
        return """/opt/aegis/bin/vault_check (SUID bit set)
/var/backups/project_chimera_v4.enc
/var/backups/chimera_clue_manifest.txt
/var/log/blacktide_audit.log
/root/privilege_flag.txt (Root only)
"""

    if cmd in ["base91", "monolith"] or "chimera_clue_manifest" in cmd_str:
        return FILESYSTEM["/var/backups"]["chimera_clue_manifest.txt"]

    if "decrypt_chimera" in cmd_str or "python3 /opt/aegis/tools/decrypt_chimera.py" in cmd_str:
        # The Iron Forge (64-mark hex vessel) receives: FirstSigil:SecondSigil:AncientClockSeed
        target_hash = hashlib.sha256(f"{FLAG1}:{FLAG2}:1785355642".encode('utf-8')).hexdigest()
        
        key_provided = ""
        if "--key" in cmd_str:
            parts_k = cmd_str.split("--key")
            if len(parts_k) > 1:
                key_provided = parts_k[1].strip().split()[0].lower()

        if key_provided == target_hash:
            if FLAG3 not in session["solved_flags"]:
                session["solved_flags"].append(FLAG3)
            return f"""======================================================================
[+] AEGIS PROJECT CHIMERA ARCHIVE DECRYPTION SUCCESSFUL!
======================================================================
ARCHIVE STATUS: UNSEALED & RECOVERED
DECRYPTION KEY: {target_hash}

----------------------------------------------------------------------
[CLASSIFIED MEMORANDUM — AEGIS SECURE DEFENSE DIRECTORATE]
PROJECT CODENAME: CHIMERA
CLASSIFICATION: TOP SECRET // AUTONOMOUS ZERO-DAY WEAPON PLATFORM

[INTERCEPTED TRANSMISSION FROM BLACK TIDE OPERATIVE ZERO]:
"You actually solved it. You tracked our trail from the polyglot carrier,
restored the shattered prime crown, deciphered the 91 monolith matrix,
passed the AST-Lambda guardian, and bound the First Sigil, Second Sigil,
and Ancient Clock Seed through the 256-bit Iron Forge.

You thought you were recovering a defense system?
Project Chimera was never a shield. It is an autonomous zero-day cyber weapon
capable of overriding national defense networks and taking down power grids.
By unsealing this archive, you have witnessed the true scope of what Aegis built.

The world will soon know the truth."
----------------------------------------------------------------------

[RECOVERED MASTER FLAG 3]:
{FLAG3}
======================================================================
"""
        else:
            return f"""[-] The Chimera chest did not open.
Seal fragment presented: '{key_provided}'
[The manifest speaks of three things bound in order by twin dots, passed through the Iron Forge.]
[Only sixty-four marks from the Forge will unlock what Black Tide sealed.]
"""

    return f"bash: {cmd}: command not found. Type 'help' for available commands."

# -------------------------------------------------------------
# HTTP Server Handler
# -------------------------------------------------------------
class AegisCTFHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()

    def do_HEAD(self):
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        try:
            url_path = urllib.parse.urlparse(self.path).path
            if url_path == "/" or url_path == "/index.html":
                file_path = os.path.join(PUBLIC_DIR, "index.html")
            else:
                file_path = os.path.join(PUBLIC_DIR, url_path.lstrip("/"))

            # If file doesn't exist and has no extension, fallback to index.html (SPA route / health check)
            if not os.path.exists(file_path) and not os.path.splitext(url_path)[1]:
                file_path = os.path.join(PUBLIC_DIR, "index.html")

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                if file_path.endswith(".html"):
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                elif file_path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")
                elif file_path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                elif file_path.endswith(".zip"):
                    self.send_header("Content-Type", "application/zip")
                    self.send_header("Content-Disposition", "attachment; filename=blacktide_evidence.zip")
                elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                    self.send_header("Content-Type", "image/jpeg")
                else:
                    self.send_header("Content-Type", "application/octet-stream")
                
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("X-Frame-Options", "DENY")
                self.end_headers()

                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self):
        try:
            content_len = int(self.headers.get('Content-Length', 0))
            post_bytes = self.rfile.read(content_len)
            
            try:
                req_data = json.loads(post_bytes.decode('utf-8'))
            except Exception:
                req_data = {}

            url_path = urllib.parse.urlparse(self.path).path

            if url_path == "/api/login":
                flag_input = req_data.get("flag1", "").strip()
                if flag_input == FLAG1:
                    sess_id = str(uuid.uuid4())
                    sess = get_session(sess_id)
                    sess["authenticated"] = True
                    sess["solved_flags"].append(FLAG1)
                    
                    resp = {
                        "success": True,
                        "session_token": sess_id,
                        "message": "Access granted to Aegis Staging Server!",
                        "user": sess["user"],
                        "cwd": sess["cwd"],
                        "flag1": FLAG1,
                        "flag_status": {
                            "flag1": FLAG1,
                            "flag2": FLAG2 if FLAG2 in sess["solved_flags"] else None,
                            "flag3": FLAG3 if FLAG3 in sess["solved_flags"] else None
                        }
                    }
                else:
                    resp = {
                        "success": False,
                        "message": "The gate did not recognize that sigil. The first sigil is buried within the evidence pack recovered from the breach scene."
                    }
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode('utf-8'))
                return

            if url_path == "/api/terminal":
                sess_id = req_data.get("session_token", "")
                cmd = req_data.get("command", "")
                sess = get_session(sess_id)

                if not sess.get("authenticated"):
                    resp = {"success": False, "output": "UNAUTHORIZED: Initial access flag required."}
                else:
                    output = process_terminal_command(sess, cmd)
                    flag_status = {
                        "flag1": FLAG1 if FLAG1 in sess["solved_flags"] else None,
                        "flag2": FLAG2 if FLAG2 in sess["solved_flags"] else None,
                        "flag3": FLAG3 if FLAG3 in sess["solved_flags"] else None
                    }
                    resp = {
                        "success": True,
                        "output": output,
                        "user": sess["user"],
                        "cwd": sess["cwd"],
                        "is_root": sess["is_root"],
                        "flag_status": flag_status,
                        "solved_flags": sess["solved_flags"]
                    }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode('utf-8'))
                return

            self.send_response(400)
            self.end_headers()
        except (BrokenPipeError, ConnectionResetError):
            pass

import socket

def get_local_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.2)
        s.connect(("8.8.8.8", 80))
        main_ip = s.getsockname()[0]
        s.close()
        if main_ip not in ips and not main_ip.startswith("127."):
            ips.insert(0, main_ip)
    except Exception:
        pass
    return ips

def start_listener(port):
    try:
        server_address = ('0.0.0.0', port)
        httpd = ThreadingHTTPServer(server_address, AegisCTFHandler)
        print(f"  [+] Active Listener on http://0.0.0.0:{port}", flush=True)
        httpd.serve_forever()
    except Exception as e:
        print(f"  [!] Port {port} listener info: {e}", flush=True)

def run_server():
    ports_to_bind = [3000, 8080, 80]
    env_p = os.environ.get("PORT")
    if env_p:
        try:
            p_val = int(env_p)
            if p_val not in ports_to_bind:
                ports_to_bind.insert(0, p_val)
        except ValueError:
            pass

    print("=====================================================================", flush=True)
    print("  AEGIS SECURE CTF — MULTI-PORT HYBRID SERVER ONLINE", flush=True)
    print("=====================================================================", flush=True)

    for p in ports_to_bind:
        t = threading.Thread(target=start_listener, args=(p,), daemon=True)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Server stopped.", flush=True)

if __name__ == "__main__":
    run_server()
