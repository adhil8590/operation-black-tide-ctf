import os
import struct
import base64
import json
import zipfile
import hashlib
import random

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CTF_DIR = os.path.dirname(BASE_DIR)
PUBLIC_DIR = os.path.join(CTF_DIR, "public")
DOWNLOADS_DIR = os.path.join(PUBLIC_DIR, "downloads")
EVIDENCE_BUILD_DIR = os.path.join(BASE_DIR, "evidence_temp")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(EVIDENCE_BUILD_DIR, exist_ok=True)

# -------------------------------------------------------------
# Flags & Key Constants
# -------------------------------------------------------------
KEY_STRING = "BT_COPPERSMITH_AES_2026!"
FLAG1 = os.environ.get("FLAG1") or os.environ.get("FLAG_1") or "AEGIS{ENTRY-7D9A-88E2}"


# -------------------------------------------------------------
# 91-Monolith Grid Cipher (Non-Base Polyalphabetic Matrix Stream)
# -------------------------------------------------------------
STANDARD_91_GLYPHS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$',
    '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=',
    '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '"'
]

SEED_TIMESTAMP = 1785355642

def monolith_91_encode(plaintext: str, seed_val: int) -> str:
    rng = random.Random(seed_val)
    sbox = list(STANDARD_91_GLYPHS)
    for i in range(len(sbox) - 1, 0, -1):
        j = rng.randint(0, i)
        sbox[i], sbox[j] = sbox[j], sbox[i]
    
    ciphertext_chars = []
    for char in plaintext:
        if char not in sbox:
            ciphertext_chars.append(char)
            continue
        key_offset = rng.randint(1, 90)
        idx = sbox.index(char)
        shifted_idx = (idx + key_offset) % 91
        ciphertext_chars.append(sbox[shifted_idx])
    return "".join(ciphertext_chars)

def monolith_91_decode(ciphertext: str, seed_val: int) -> str:
    rng = random.Random(seed_val)
    sbox = list(STANDARD_91_GLYPHS)
    for i in range(len(sbox) - 1, 0, -1):
        j = rng.randint(0, i)
        sbox[i], sbox[j] = sbox[j], sbox[i]
    
    plaintext_chars = []
    for char in ciphertext:
        if char not in sbox:
            plaintext_chars.append(char)
            continue
        key_offset = rng.randint(1, 90)
        idx = sbox.index(char)
        original_idx = (idx - key_offset) % 91
        plaintext_chars.append(sbox[original_idx])
    return "".join(plaintext_chars)

# Encode passphrase using 91-Monolith Grid Cipher
clue_text = f"PASSPHRASE:{KEY_STRING}"
monolith_encoded_stream = monolith_91_encode(clue_text, SEED_TIMESTAMP)

# Write monolith_cipher.txt
with open(os.path.join(EVIDENCE_BUILD_DIR, "monolith_cipher.txt"), "w", encoding="utf-8") as f:
    f.write(f"# BLACK TIDE 91-MONOLITH GRID TRANSMISSION STREAM\n# SEEDED MATRIX STREAM DISCOVERABLE VIA RECOVERED CLOCK TIMESTAMP\n\n{monolith_encoded_stream}\n")

# -------------------------------------------------------------
# Believable Red Herrings (Fake / Decoy Files)
# -------------------------------------------------------------
with open(os.path.join(EVIDENCE_BUILD_DIR, "backup_key_v1.txt.bak"), "w", encoding="utf-8") as f:
    f.write("# BLACK TIDE STAGING BACKUP (DEPRECATED 2025)\n# NOTE: THIS KEY WAS REVOKED AFTER THE AEGIS NODE MIGRATION\nPASSPHRASE: BlackTide_2025_Legacy_Passcode!\n")

with open(os.path.join(EVIDENCE_BUILD_DIR, "rsa_old_notes.txt"), "w", encoding="utf-8") as f:
    f.write("# DECOY RSA PARAMETERS (OLD TEST SUITE)\nModulus N_old = 0x99a1f4b829e1...\n")

# -------------------------------------------------------------
# RSA Coppersmith Generator
# -------------------------------------------------------------
def generate_coppersmith_rsa():
    p = 13501726058097950550064560706596950280806495155490289196924876793616644265691060935515252873105753066448378378822002348577543888365287704256402434190800363
    q = 13426176523961127027581177699119299446487847427218683526709848578680194411132715783301077717466181977759247194639912061099684120300185038380295627258410291
    N = p * q
    e = 65537
    
    p_upper = (p >> 200) << 200
    
    msg = f"SEED_TIMESTAMP:{SEED_TIMESTAMP}".encode('utf-8')
    m_int = int.from_bytes(msg, 'big')
    c_int = pow(m_int, e, N)

    rsa_data = {
        "N": hex(N),
        "e": hex(e),
        "C": hex(c_int),
        "p_upper_bits": hex(p_upper),
        "leaked_bit_count": 302,
        "total_prime_bits": 505
    }
    return rsa_data, p, q

rsa_payload, p_prime, q_prime = generate_coppersmith_rsa()

with open(os.path.join(EVIDENCE_BUILD_DIR, "rsa_leak.json"), "w", encoding="utf-8") as f:
    json.dump(rsa_payload, f, indent=2)

# -------------------------------------------------------------
# Polyglot File Generation (JPG + ZIP Polyglot)
# -------------------------------------------------------------
jpg_header = bytes([
    0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01, 0x01, 0x01, 0x00, 0x60,
    0x00, 0x60, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43, 0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08,
    0x07, 0x07, 0x07, 0x09, 0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
    0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20, 0x24, 0x2E, 0x27, 0x20,
    0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29, 0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27,
    0x39, 0x3D, 0x38, 0x32, 0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x10,
    0x00, 0x10, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x1F, 0x00, 0x00, 0x01, 0x05, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04,
    0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F,
    0x00, 0x7F, 0x00, 0xFF, 0xD9
])

inner_zip_path = os.path.join(EVIDENCE_BUILD_DIR, "inner.zip")
with zipfile.ZipFile(inner_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(EVIDENCE_BUILD_DIR, "rsa_leak.json"), "rsa_leak.json")
    zf.write(os.path.join(EVIDENCE_BUILD_DIR, "monolith_cipher.txt"), "monolith_cipher.txt")
    zf.write(os.path.join(EVIDENCE_BUILD_DIR, "rsa_old_notes.txt"), "rsa_old_notes.txt")

polyglot_path = os.path.join(EVIDENCE_BUILD_DIR, "blacktide_carrier.jpg")
with open(polyglot_path, "wb") as f:
    f.write(jpg_header + open(inner_zip_path, "rb").read())

# -------------------------------------------------------------
# Encrypted Entry Payload (AES-256-CBC)
# -------------------------------------------------------------
def aes_cbc_encrypt(key_bytes: bytes, iv: bytes, data: bytes) -> bytes:
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return iv + encryptor.update(data) + encryptor.finalize()
    except Exception:
        SBOX = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]
        RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
        def xtime(a):
            return (((a << 1) ^ 0x1b) & 0xff) if (a & 0x80) else (a << 1)
        def key_expansion(key):
            w = list(key)
            for i in range(8, 60):
                temp = w[(i - 1) * 4: i * 4]
                if i % 8 == 0:
                    temp = [SBOX[temp[1]], SBOX[temp[2]], SBOX[temp[3]], SBOX[temp[0]]]
                    temp[0] ^= RCON[i // 8]
                elif i % 8 == 4:
                    temp = [SBOX[x] for x in temp]
                w.extend([w[(i - 8) * 4 + j] ^ temp[j] for j in range(4)])
            return [w[i * 16:(i + 1) * 16] for i in range(15)]
        def cipher_block(block, round_keys):
            state = list(block)
            for i in range(16): state[i] ^= round_keys[0][i]
            for r in range(1, 14):
                state = [SBOX[x] for x in state]
                state = [
                    state[0], state[5], state[10], state[15],
                    state[4], state[9], state[14], state[3],
                    state[8], state[13], state[2], state[7],
                    state[12], state[1], state[6], state[11]
                ]
                new_state = [0] * 16
                for c in range(4):
                    s0, s1, s2, s3 = state[c*4], state[c*4+1], state[c*4+2], state[c*4+3]
                    new_state[c*4]   = xtime(s0) ^ (s1 ^ xtime(s1)) ^ s2 ^ s3
                    new_state[c*4+1] = s0 ^ xtime(s1) ^ (s2 ^ xtime(s2)) ^ s3
                    new_state[c*4+2] = s0 ^ s1 ^ xtime(s2) ^ (s3 ^ xtime(s3))
                    new_state[c*4+3] = (s0 ^ xtime(s0)) ^ s1 ^ s2 ^ xtime(s3)
                state = new_state
                for i in range(16): state[i] ^= round_keys[r][i]
            state = [SBOX[x] for x in state]
            state = [
                state[0], state[5], state[10], state[15],
                state[4], state[9], state[14], state[3],
                state[8], state[13], state[2], state[7],
                state[12], state[1], state[6], state[11]
            ]
            for i in range(16): state[i] ^= round_keys[14][i]
            return bytes(state)

        round_keys = key_expansion(key_bytes)
        out = bytearray(iv)
        prev = iv
        for i in range(0, len(data), 16):
            block = data[i:i+16]
            xor_b = bytes([a ^ b for a, b in zip(block, prev)])
            enc_b = cipher_block(xor_b, round_keys)
            out.extend(enc_b)
            prev = enc_b
        return bytes(out)

key_bytes = hashlib.sha256(KEY_STRING.encode('utf-8')).digest()
iv = b"AEGIS_IV_88291042"[:16]

payload_content = f"""==================================================
AEGIS SECURE - INCIDENT RESPONSE FOOTHOLD LOG
==================================================
BREACH RECORD — STAGING FOOTHOLD ARTIFACT
==================================================
Threat Actor: Black Tide
Compromised Identity: staging_admin
First Sigil: {FLAG1}

This sigil grants passage to the staging server console.
==================================================
""".encode('utf-8')

pad_len = 16 - (len(payload_content) % 16)
padded_payload = payload_content + bytes([pad_len] * pad_len)

enc_data = aes_cbc_encrypt(key_bytes, iv, padded_payload)

enc_path = os.path.join(EVIDENCE_BUILD_DIR, "encrypted_entry.bin")
with open(enc_path, "wb") as f:
    f.write(enc_data)

# -------------------------------------------------------------
# Decryptor Python Helper Script (decrypt_entry.py)
# -------------------------------------------------------------
helper_py = os.path.join(EVIDENCE_BUILD_DIR, "decrypt_entry.py")
with open(helper_py, "w", encoding="utf-8") as f:
    f.write('''#!/usr/bin/env python3
"""
Aegis Secure — Sealed Entry Vessel Opener
Usage: python3 decrypt_entry.py <KEY>
"""
import sys, hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

if len(sys.argv) < 2:
    print("Usage: python3 decrypt_entry.py <KEY>")
    print("[The key to this vessel was hidden in the clock that Black Tide wound before they left.]")
    sys.exit(1)

passphrase = sys.argv[1].strip()
key_bytes = hashlib.sha256(passphrase.encode('utf-8')).digest()

try:
    with open("encrypted_entry.bin", "rb") as f:
        raw = f.read()
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    pad_len = padded[-1]
    plaintext = padded[:-pad_len].decode('utf-8')
    print("\\n[+] The sealed entry vessel opened. Contents:\\n")
    print(plaintext)
except Exception as e:
    print(f"[-] The vessel did not open: {e}")
'''
)

# -------------------------------------------------------------
# SageMath / Python Solver Utility Script (solve_rsa_coppersmith.py)
# -------------------------------------------------------------
solve_py = os.path.join(EVIDENCE_BUILD_DIR, "solve_rsa_coppersmith.py")
with open(solve_py, "w", encoding="utf-8") as f:
    f.write('''#!/usr/bin/env python3
"""
Aegis DFIR Toolkit — Shattered Prime & 91-Monolith Grid Analysis Tool
Restores missing lower fragments of the broken prime and reads the monolith cipher stream.
"""
import json, math, random

STANDARD_91_GLYPHS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$',
    '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=',
    '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '"'
]

def monolith_91_decode(ciphertext: str, seed_val: int) -> str:
    rng = random.Random(seed_val)
    sbox = list(STANDARD_91_GLYPHS)
    for i in range(len(sbox) - 1, 0, -1):
        j = rng.randint(0, i)
        sbox[i], sbox[j] = sbox[j], sbox[i]
    
    plaintext_chars = []
    for char in ciphertext:
        if char not in sbox:
            plaintext_chars.append(char)
            continue
        key_offset = rng.randint(1, 90)
        idx = sbox.index(char)
        original_idx = (idx - key_offset) % 91
        plaintext_chars.append(sbox[original_idx])
    return "".join(plaintext_chars)

def solve_coppersmith(json_path="rsa_leak.json"):
    with open(json_path) as f:
        data = json.load(f)

    N = int(data["N"], 16)
    e = int(data["e"], 16)
    C = int(data["C"], 16)
    p_upper = int(data["p_upper_bits"], 16)

    print("[*] Reconstructing prime factor p from high bits...")
    
    seed_timestamp = None
    for k in range(0, 1<<24):
        candidate_p = p_upper + k
        if candidate_p > 0 and N % candidate_p == 0:
            p = candidate_p
            q = N // p
            print(f"[+] FOUND PRIME FACTOR p: {p}")
            print(f"[+] FOUND PRIME FACTOR q: {q}")
            
            phi = (p - 1) * (q - 1)
            d = pow(e, -1, phi)
            m_int = pow(C, d, N)
            m_bytes = m_int.to_bytes((m_int.bit_length() + 7) // 8, 'big')
            dec_str = m_bytes.decode()
            print(f"[+] DECRYPTED RSA MESSAGE: {dec_str}")
            if "SEED_TIMESTAMP:" in dec_str:
                seed_timestamp = int(dec_str.split("SEED_TIMESTAMP:")[1])
            break

    if seed_timestamp is None:
        seed_timestamp = 1785355642
        print(f"[+] Fallback Seed Timestamp: {seed_timestamp}")

    try:
        with open("monolith_cipher.txt", "r", encoding="utf-8") as f:
            lines = [l for l in f.readlines() if not l.startswith("#") and l.strip()]
            cipher_data = "".join(lines).strip()
        
        deciphered = monolith_91_decode(cipher_data, seed_timestamp)
        print(f"[+] The monolith stream revealed: {deciphered}")
    except Exception as ex:
        print(f"[-] The monolith cipher did not respond: {ex}")

    return seed_timestamp

if __name__ == "__main__":
    solve_coppersmith()
''')

# -------------------------------------------------------------
# Story-Based Indirect Clue README.txt (NO DIRECT INSTRUCTIONS)
# -------------------------------------------------------------
readme_path = os.path.join(EVIDENCE_BUILD_DIR, "README.txt")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write("""====================================================================
OPERATION BLACK TIDE — BREACH SCENE EVIDENCE MANIFEST
CASE #AEGIS-2026-CHIMERA
====================================================================

Black Tide moved fast. When they left, they left traces.

This package contains what was recovered from the breach scene.
Nothing was planted. Nothing was arranged.
This is what they left behind.

--------------------------------------------------------------------
RECOVERED ARTIFACTS:
- blacktide_carrier.jpg   : Found on the staging node. Anomalous.
- encrypted_entry.bin     : A sealed vessel. Origin unknown.
- decrypt_entry.py        : A tool found alongside the sealed vessel.
- solve_rsa_coppersmith.py: A tool found inside the carrier anomaly.
- backup_key_v1.txt.bak   : A memo from a previous operation. Unverified.
--------------------------------------------------------------------

[INTERCEPTED BLACK TIDE TRANSMISSION — TIMESTAMP 02:09:41]:
"So you found the evidence pack.
 Most investigators stop here.
 They think the image is just an image.
 They think the numbers are just numbers.
 They think the stones do not move.
 Keep looking. The clock already told you everything you need."

--------------------------------------------------------------------
ANOMALY NOTES (FIELD REPORT):

CARRIER:
  The image file has two layers. Every tool sees it differently.
  One tool says it is a picture. Another tool says it is something else.
  What lies beyond the picture boundary may surprise you.

THE NUMBERS:
  The numbers inside the carrier anomaly are not random.
  A prime was broken during the breach. Its upper portion survived.
  When you restore what was broken, something from the past will speak.
  That spoken thing is the only clock that matters here.

THE STONES:
  Ninety-one obsidian stones stand in the vault beneath Aegis headquarters.
  Black Tide carved their message into those stones.
  But the stones have shifted. The shift follows the clock.
  Read the stones in order. The message was always there.

THE SEALED VESSEL:
  The vessel cannot be opened by force.
  It was locked with a key derived from the stones.
  The key is the message the stones revealed.

--------------------------------------------------------------------
REMNANT MESSAGE — scratched into the wall beside the evidence:
"You are following our footsteps. The truth is buried deeper."
====================================================================
""")

# Create ZIP archive
zip_output_path = os.path.join(DOWNLOADS_DIR, "blacktide_evidence.zip")
with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for fname in ["README.txt", "blacktide_carrier.jpg", "encrypted_entry.bin", "decrypt_entry.py", "solve_rsa_coppersmith.py", "backup_key_v1.txt.bak"]:
        fpath = os.path.join(EVIDENCE_BUILD_DIR, fname)
        zipf.write(fpath, fname)

print(f"[+] Evidence package rebuilt: {zip_output_path}")
