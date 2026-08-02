#!/usr/bin/env node
/**
 * Aegis Secure CTF Web Server & Terminal Emulation Engine
 * Operation Black Tide: Project Chimera — Node.js/Express Edition
 * Deployable to Railway, Render, Fly.io, Glitch, etc.
 */

'use strict';

const express = require('express');
const crypto  = require('crypto');
const path    = require('path');
const { v4: uuidv4 } = require('uuid');

const app  = express();
const PORT = process.env.PORT || 3000;

// ─── Paths ────────────────────────────────────────────────────────────────────
const PUBLIC_DIR = path.join(__dirname, 'public');

// ─── CTF Constants ────────────────────────────────────────────────────────────
const FLAG1 = 'AEGIS{ENTRY-7D9A-88E2}';
const FLAG2 = 'AEGIS{PRIV-C4F8-15B7}';
const FLAG3 = 'AEGIS{CHMR-E1A6-9D40}';

const CORRECT_VAULT_KEY  = rot13('BlackTide_Root_Override');   // OynpxGvqr_Ebbg_Bireevqr
const TARGET_CHIMERA_HASH = sha256(`${FLAG1}:${FLAG2}:1785355642`);

// ─── In-Memory Session Store ──────────────────────────────────────────────────
const sessions = {};

// ─── Virtual Filesystem ───────────────────────────────────────────────────────
const FILESYSTEM = {
  '/home/analyst': {
    'readme_staging.txt': `==================================================
AEGIS STAGING NODE-04 — INTERCEPTED OPERATIONAL LOG
==================================================
Log Entry #409-B: Operative Black Tide breached staging sector 'aegis-staging-node-04'.

CRYPTIC INVESTIGATION DOSSIER:
• "Shadows lurk in the central audit logs of /var/log where intercepted memory traces whisper of the forbidden vault."
• "The root key lies guarded behind the AST-Lambda entity residing in the sacred binary paths of /opt/aegis/bin."
• "When the crown of elevated authority is seized, the subterranean vaults of /var/backups will yield the Chimera vessel."
==================================================`,
    '.bash_history': `cat /etc/issue
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
`,
    'notes.txt': `[CODED TRANSMISSION MEMO #77]
'The guardian binary at /opt/aegis/bin/vault_check seeks an invisible aura in the environment known to operatives as VAULT_KEY. Seek the audit footprints recorded in /var/log to decipher its secret resonance.'`,
    'old_script.py': `# STAGED RECOVERY SCRIPT — PHANTOM BUILD (2025)
# DECRYPTION_VECTOR = 'AEGIS_OLD_STAGING_KEY_2025'
# BUILD STATUS: decommissioned — see /var/backups for active vessel`,
  },
  '/opt/aegis/bin': {
    'vault_check': `[OBFUSCATED AST-LAMBDA SUID BINARY - AEGIS VAULT VERIFIER v4.2]
(lambda _:(lambda __:(lambda ___:___(___)))(lambda ___:lambda ____:____(lambda _____:___(___)(____)(_____))))(lambda _:lambda __:lambda ___:___ if __ == 0 else _(_ - 1)(__)(___))(24)
Owned by root:root (rwsr-xr-x)
Cryptic Inscription: "The AST gate measures 24 glyphs in length. Pass the environmental vector VAULT_KEY to awaken the root spirit."
`,
  },
  '/opt/aegis/tools': {
    'decrypt_chimera.py': `# Aegis Project Chimera Recovery Tool v4.0 (EXPERT DUAL-FLAG + TIME SEEDED SHA-256)
# Usage: python3 /opt/aegis/tools/decrypt_chimera.py --key <DERIVED_HASH_KEY>
# The Iron Forge leaves sixty-four marks upon every worthy seal. Bind First and Second Sigils with the Ancient Clock, joined by twin-dot monoliths.
`,
  },
  '/var/log': {
    'blacktide_audit.log': `[2026-07-30 02:14:09] ALERT: Unauthorized intrusion attempt on the AST-Lambda guardian (/opt/aegis/bin/vault_check).
[2026-07-30 02:14:15] AUDIT: Operative Black Tide injected dynamic environment vector VAULT_KEY.
[2026-07-30 02:15:01] INTERCEPTED MEMORY TRACE: "The AST gate measures 24 glyphs in length. Operative Echo inscribed the key by reflecting the cipher 'BlackTide_Root_Override' through the 13th mirror of Caesar..."
[2026-07-30 02:15:44] SYSTEM RECORD: Royal clearance unlocks the sanctuary chamber at /root/privilege_flag.txt.
`,
    'auth_failure_old.log': `[2026-07-29 18:22:01] FAILED LOGIN: user admin from IP 192.168.1.100 (Token AEGIS{FAKE-ENTRY-TOKEN-99})`,
  },
  '/var/backups': {
    'project_chimera_v4.enc': `[SEALED CHIMERA VESSEL — IRON-LOCKED ARCHIVE — 48.2 MB]
Status: BOUND BY BLACK TIDE`,
    'chimera_clue_manifest.txt': `==================================================
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
`,
    'chimera_v3_old.bak': `[CORRUPTED DECOY ARCHIVE - INVALID HEADER]`,
    'unused_env.conf': `# UNUSED DATABASE CONFIG\nDATABASE_PASS=Admin_Unused_123!`,
  },
  '/root': {
    'privilege_flag.txt': `==================================================
FLAG 2 (PRIVILEGE ESCALATION RECOVERED):
${FLAG2}
==================================================

Sanctuary Record: Root clearance achieved! Proceed to /var/backups and synthesize the dual-flag seal combined with the ancient clock seed to unseal Project Chimera!`,
    'master_audit.db': `[SQLITE3 DATABASE - 14 TABLES] Confidential Security Audit Data`,
  },
};

// ─── Helpers ─────────────────────────────────────────────────────────────────
function sha256(str) {
  return crypto.createHash('sha256').update(str, 'utf8').digest('hex');
}

function rot13(str) {
  return str.replace(/[a-zA-Z]/g, (c) => {
    const base = c <= 'Z' ? 65 : 97;
    return String.fromCharCode(((c.charCodeAt(0) - base + 13) % 26) + base);
  });
}

function getSession(sessionId) {
  if (!sessions[sessionId]) {
    sessions[sessionId] = {
      authenticated: false,
      user: 'analyst',
      isRoot: false,
      cwd: '/home/analyst',
      env: { PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/aegis/bin' },
      solvedFlags: [],
    };
  }
  return sessions[sessionId];
}

function resolvePath(sess, target) {
  if (!target) return sess.cwd;
  if (target.startsWith('/')) return target;
  return path.posix.normalize(path.posix.join(sess.cwd, target));
}

// ─── Terminal Command Engine ──────────────────────────────────────────────────
function processCommand(sess, cmdStr) {
  cmdStr = cmdStr.trim();
  if (!cmdStr) return '';

  const parts  = cmdStr.split(/\s+/);
  const cmd    = parts[0];
  const args   = parts.slice(1);

  // export KEY=VALUE
  if (cmdStr.startsWith('export ')) {
    const eq = cmdStr.slice(7).trim();
    const eqIdx = eq.indexOf('=');
    if (eqIdx === -1) return 'Usage: export KEY=VALUE';
    const k = eq.slice(0, eqIdx).trim();
    const v = eq.slice(eqIdx + 1).trim().replace(/^['"]|['"]$/g, '');
    sess.env[k] = v;
    return `Environment variable ${k} set.`;
  }

  if (cmd === 'env') {
    return Object.entries(sess.env).map(([k, v]) => `${k}=${v}`).join('\n');
  }

  if (cmd === 'clear') return '__CLEAR__';

  if (cmd === 'whoami') return sess.user;

  if (cmd === 'id') {
    return sess.isRoot
      ? 'uid=0(root) gid=0(root) groups=0(root)'
      : 'uid=1001(analyst) gid=1001(analyst) groups=1001(analyst),27(sudo)';
  }

  if (cmd === 'pwd') return sess.cwd;

  if (cmd === 'uname') {
    return args.includes('-a')
      ? 'Linux aegis-staging-node-04 5.15.0-101-generic #111-Ubuntu SMP x86_64 GNU/Linux'
      : 'Linux';
  }

  if (cmd === 'sudo' && args[0] === '-l') {
    return `Matching Defaults entries for analyst on aegis-staging:
    env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/aegis/bin

User analyst may run the following commands on aegis-staging:
    (root) NOPASSWD: /opt/aegis/bin/vault_check`;
  }

  if (cmd === 'cd') {
    const target = args[0] || '/home/analyst';
    let newPath;
    if (target === '..') {
      newPath = path.posix.dirname(sess.cwd) || '/';
    } else {
      newPath = resolvePath(sess, target);
    }
    if (newPath === '/root' && !sess.isRoot)
      return 'bash: cd: /root: Permission denied';
    const validDirs = Object.keys(FILESYSTEM).concat(['/', '/home', '/opt', '/opt/aegis', '/var']);
    if (validDirs.includes(newPath)) {
      sess.cwd = newPath;
      return '';
    }
    return `bash: cd: ${target}: No such file or directory`;
  }

  if (cmd === 'ls') {
    let target = sess.cwd;
    const nonFlagArgs = args.filter(a => !a.startsWith('-'));
    if (nonFlagArgs.length > 0) target = resolvePath(sess, nonFlagArgs[0]);

    if (target === '/root' && !sess.isRoot)
      return "ls: cannot open directory '/root': Permission denied";

    const longFormat = args.includes('-la') || args.includes('-l') || args.includes('-a');

    if (FILESYSTEM[target]) {
      const files = Object.keys(FILESYSTEM[target]);
      if (longFormat) {
        const lines = [
          'total 24',
          'drwxr-xr-x 2 analyst analyst 4096 Jul 30 02:00 .',
          'drwxr-xr-x 4 root    root    4096 Jul 30 02:00 ..',
        ];
        // Include hidden files only with -a/-la
        for (const f of files) {
          if (f.startsWith('.') && !longFormat) continue;
          const perm = f === 'vault_check'
            ? '-rwsr-xr-x 1 root    root'
            : '-rw-r--r-- 1 analyst analyst';
          lines.push(`${perm}    2048 Jul 30 02:15 ${f}`);
        }
        return lines.join('\n');
      }
      return files.filter(f => !f.startsWith('.')).join('  ');
    }

    const pseudoDirs = {
      '/':     ['home', 'opt', 'var', 'root', 'etc', 'tmp'],
      '/home': ['analyst'],
      '/opt':  ['aegis'],
      '/var':  ['log', 'backups'],
    };
    if (pseudoDirs[target]) return pseudoDirs[target].join('  ');
    return `ls: cannot access '${target}': No such file or directory`;
  }

  if (cmd === 'cat') {
    if (!args[0]) return 'Usage: cat <filename>';
    const fname = args[0];
    let dir, base;
    if (fname.includes('/')) {
      dir  = path.posix.dirname(fname);
      base = path.posix.basename(fname);
    } else {
      dir  = sess.cwd;
      base = fname;
    }
    if (dir === '/root' && !sess.isRoot)
      return `cat: ${fname}: Permission denied`;
    if (FILESYSTEM[dir] && FILESYSTEM[dir][base] !== undefined) {
      const content = FILESYSTEM[dir][base];
      if (base === 'privilege_flag.txt' && sess.isRoot) {
        if (!sess.solvedFlags.includes(FLAG2)) sess.solvedFlags.push(FLAG2);
      }
      return content;
    }
    return `cat: ${fname}: No such file or directory`;
  }

  // strings vault_check
  if (cmd === 'strings' && cmdStr.includes('vault_check')) {
    return `/lib64/ld-linux-x86-64.so.2
__gmon_start__
AEGIS_VAULT_SECURITY_CORE_v4.2 (AST-LAMBDA EVAL ENGINE)
Reading environment aura: VAULT_KEY...
INSCRIPTION: "The name they used to break in — seen backwards through Caesar's thirteenth mirror — is the only key this gate will accept."
Aura verified. Awakening root spirit.`;
  }

  // vault_check execution
  if (
    cmd === '/opt/aegis/bin/vault_check' ||
    cmd === './vault_check' ||
    cmd === 'vault_check' ||
    cmdStr === '/opt/aegis/bin/vault_check'
  ) {
    const currentVK = sess.env['VAULT_KEY'] || '';
    const accepted  =
      currentVK === CORRECT_VAULT_KEY ||           // OynpxGvqr_Ebbg_Bireevqr
      currentVK === 'BlackTide_Root_Override' ||   // source text (also accepted)
      currentVK.length === 24;                     // length-based fallback

    if (accepted) {
      sess.isRoot = true;
      sess.user   = 'root';
      if (!sess.solvedFlags.includes(FLAG2)) sess.solvedFlags.push(FLAG2);
      return `[+] The AST-Lambda gate accepted the aura.
[+] Root spirit awakened within the Aegis Security Core.
[+] The crown of the system now rests on your head.

[SECOND SIGIL RECOVERED]: ${FLAG2}

[BLACK TIDE WHISPER]: "You earned that. Not many reach this far.
 The final chest lies in the forgotten vault at /var/backups.
 Everything you have recovered must be bound together before it opens."`;
    }

    return `[-] The gate rejected the aura.
Presented aura: '${currentVK}'
[The gate is silent. The answer lies in the memory fragments scattered through the server logs, and in the words carved into the binary itself.]`;
  }

  // find
  if (cmd === 'find') {
    return `/opt/aegis/bin/vault_check (SUID bit set)
/var/backups/project_chimera_v4.enc
/var/backups/chimera_clue_manifest.txt
/var/log/blacktide_audit.log
/root/privilege_flag.txt (Root only)`;
  }

  // decrypt_chimera
  if (cmdStr.includes('decrypt_chimera')) {
    let keyProvided = '';
    const keyMatch = cmdStr.match(/--key\s+([a-f0-9]+)/i);
    if (keyMatch) keyProvided = keyMatch[1].toLowerCase();

    if (keyProvided === TARGET_CHIMERA_HASH) {
      if (!sess.solvedFlags.includes(FLAG3)) sess.solvedFlags.push(FLAG3);
      return `======================================================================
[+] AEGIS PROJECT CHIMERA ARCHIVE DECRYPTION SUCCESSFUL!
======================================================================
ARCHIVE STATUS: UNSEALED & RECOVERED
DECRYPTION KEY: ${TARGET_CHIMERA_HASH}

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

[RECOVERED CHIMERA VESSEL SIGIL]:
${FLAG3}
======================================================================`;
    }

    return `[-] The Chimera chest did not open.
Seal fragment presented: '${keyProvided}'
[The manifest speaks of three things bound in order by twin dots, passed through the Iron Forge.]
[Only sixty-four marks from the Forge will unlock what Black Tide sealed.]`;
  }

  // help
  if (cmd === 'help') {
    return `Available commands:
  ls [-la] [dir]    — list directory contents
  cat <file>        — read a file
  cd <dir>          — change directory
  pwd               — print working directory
  whoami / id       — show current user
  find              — locate notable files
  env               — show environment variables
  export KEY=VALUE  — set environment variable
  strings <binary>  — extract readable strings from binary
  sudo -l           — list sudo permissions
  uname -a          — system information
  clear             — clear terminal
  /opt/aegis/bin/vault_check — execute the vault guardian binary`;
  }

  return `bash: ${cmd}: command not found. Type 'help' for available commands.`;
}

// ─── Middleware ───────────────────────────────────────────────────────────────
app.use(express.json());
app.use(express.static(PUBLIC_DIR));

// Security headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Powered-By', 'Aegis-Secure-CTF/4.0');
  next();
});

// ─── API Routes ───────────────────────────────────────────────────────────────

// POST /api/login — submit FLAG1 to get terminal access
app.post('/api/login', (req, res) => {
  const flagInput = (req.body.flag1 || '').trim();
  if (flagInput === FLAG1) {
    const sessId = uuidv4();
    const sess   = getSession(sessId);
    sess.authenticated = true;
    sess.solvedFlags.push(FLAG1);
    return res.json({
      success: true,
      session_token: sessId,
      message: 'Access granted to Aegis Staging Server!',
      user: sess.user,
      cwd:  sess.cwd,
    });
  }
  return res.json({
    success: false,
    message: 'The gate did not recognize that sigil. The first sigil is buried within the evidence pack recovered from the breach scene.',
  });
});

// POST /api/terminal — execute a terminal command
app.post('/api/terminal', (req, res) => {
  const sessId = req.body.session_token || '';
  const cmd    = req.body.command || '';
  const sess   = getSession(sessId);

  if (!sess.authenticated) {
    return res.json({ success: false, output: 'UNAUTHORIZED: Initial access flag required.' });
  }

  const output = processCommand(sess, cmd);
  return res.json({
    success:      true,
    output:       output,
    user:         sess.user,
    cwd:          sess.cwd,
    is_root:      sess.isRoot,
    solved_flags: sess.solvedFlags,
  });
});

// ─── Catch-all → serve index.html ────────────────────────────────────────────
app.get('*', (req, res) => {
  res.sendFile(path.join(PUBLIC_DIR, 'index.html'));
});

// ─── Start ────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log('=====================================================================');
  console.log('  AEGIS SECURE CTF — OPERATION BLACK TIDE');
  console.log(`  Local : http://localhost:${PORT}`);
  console.log('=====================================================================');
});
