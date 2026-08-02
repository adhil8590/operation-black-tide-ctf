#!/usr/bin/env python3
"""
Operation Black Tide: Project Chimera — Master Walkthrough PDF Generator
Supports multiple professional color themes:
- 'executive_light' (Default: Clean White & Deep Navy, SANS / OffSec print style)
- 'midnight_slate' (Modern Dark Slate, HackTheBox style)
- 'crimson_gold' (Elite Pentest Crimson & Gold style)
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"C:\Users\ADHIL\OneDrive\Desktop\CTF\Operation_Black_Tide_CTF_Master_Walkthrough.pdf"

# -------------------------------------------------------------
# Color Themes Configuration
# -------------------------------------------------------------
THEMES = {
    "executive_light": {
        "bg": colors.HexColor("#FFFFFF"),
        "panel": colors.HexColor("#F8FAFC"),
        "text": colors.HexColor("#0F172A"),
        "muted": colors.HexColor("#64748B"),
        "primary": colors.HexColor("#1E3A8A"),   # Deep Sapphire Navy
        "secondary": colors.HexColor("#059669"), # Emerald Green
        "amber": colors.HexColor("#D97706"),     # Warm Amber
        "danger": colors.HexColor("#DC2626"),    # Crimson Red
        "border": colors.HexColor("#CBD5E1"),    # Slate Border
        "code_bg": colors.HexColor("#0F172A"),  # Dark Code Box for high contrast
        "code_text": colors.HexColor("#38BDF8"),# Cyan Monospace Code Text
        "callout_bg": colors.HexColor("#FEF3C7"),# Warm Callout Box
    },
    "midnight_slate": {
        "bg": colors.HexColor("#0F172A"),
        "panel": colors.HexColor("#1E293B"),
        "text": colors.HexColor("#F1F5F9"),
        "muted": colors.HexColor("#94A3B8"),
        "primary": colors.HexColor("#06B6D4"),   # Electric Cyan
        "secondary": colors.HexColor("#10B981"), # Lime Green
        "amber": colors.HexColor("#F59E0B"),
        "danger": colors.HexColor("#EF4444"),
        "border": colors.HexColor("#334155"),
        "code_bg": colors.HexColor("#020617"),
        "code_text": colors.HexColor("#22D3EE"),
        "callout_bg": colors.HexColor("#1E1B4B"),
    },
    "crimson_gold": {
        "bg": colors.HexColor("#FFFFFF"),
        "panel": colors.HexColor("#FFFBEB"),
        "text": colors.HexColor("#111827"),
        "muted": colors.HexColor("#4B5563"),
        "primary": colors.HexColor("#991B1B"),   # Crimson Red
        "secondary": colors.HexColor("#B45309"), # Royal Gold
        "amber": colors.HexColor("#D97706"),
        "danger": colors.HexColor("#B91C1C"),
        "border": colors.HexColor("#E5E7EB"),
        "code_bg": colors.HexColor("#18181B"),
        "code_text": colors.HexColor("#FDE047"),
        "callout_bg": colors.HexColor("#FEF2F2"),
    }
}

# Selected Theme (Default: executive_light)
ACTIVE_THEME_NAME = "executive_light"
THEME = THEMES[ACTIVE_THEME_NAME]

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(THEME["muted"])

        # Header Bar
        self.drawString(54, 11 * inch - 36, "AEGIS SECURE DFIR // OPERATION BLACK TIDE: PROJECT CHIMERA CTF WALKTHROUGH")
        self.setStrokeColor(THEME["primary"])
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Footer Bar
        self.setStrokeColor(THEME["border"])
        self.line(54, 48, 8.5 * inch - 54, 48)
        self.drawString(54, 34, "CONFIDENTIAL — CYBERSECURITY TRAINING MANUAL")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 34, page_str)

        self.restoreState()

def build_pdf(theme_name="executive_light"):
    global THEME
    THEME = THEMES.get(theme_name, THEMES["executive_light"])

    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=THEME["primary"],
        alignment=1,
        spaceAfter=12
    )

    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=THEME["secondary"],
        alignment=1,
        spaceAfter=25
    )

    style_h1 = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=THEME["primary"],
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=THEME["secondary"],
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=THEME["text"],
        spaceAfter=8
    )

    style_code = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=THEME["code_text"],
        spaceBefore=4,
        spaceAfter=4
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=THEME["text"]
    )

    story = []

    # COVER PAGE
    story.append(Spacer(1, 30))
    story.append(Paragraph("OPERATION BLACK TIDE", style_cover_title))
    story.append(Paragraph("PROJECT CHIMERA — ORGANISER SOLVE REFERENCE MANUAL", style_cover_subtitle))
    story.append(HRFlowable(width="100%", thickness=2, color=THEME["primary"], spaceAfter=25))

    meta_data = [
        [Paragraph("<b>Target Node:</b>", style_body), Paragraph("Aegis Secure DFIR Staging Node-04", style_body)],
        [Paragraph("<b>Difficulty Rating:</b>", style_body), Paragraph(f"<font color='{THEME['danger'].hexval()}'><b>EXPERT</b></font>", style_body)],
        [Paragraph("<b>Categories:</b>", style_body), Paragraph("Polyglot Forensics, Shattered Prime Reconstruction, Monolith Grid Cipher, SUID Escalation, Multi-Stage Hash Synthesis", style_body)],
        [Paragraph("<b>Estimated Solving Time:</b>", style_body), Paragraph("30 – 45 Minutes", style_body)],
        [Paragraph("<b>Author / Creator:</b>", style_body), Paragraph("Aegis Secure Incident Response & DFIR Core Team", style_body)],
        [Paragraph("<b>Document Version:</b>", style_body), Paragraph("v4.0 (Story-Driven Redesign — Organiser Reference)", style_body)],
    ]
    t_meta = Table(meta_data, colWidths=[2.2*inch, 4.8*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), THEME["panel"]),
        ('BOX', (0,0), (-1,-1), 1.5, THEME["primary"]),
        ('INNERGRID', (0,0), (-1,-1), 0.5, THEME["border"]),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 30))

    brief_text = """
    <b>EXECUTIVE MISSION BRIEFING:</b><br/>
    A global cybersecurity company, <i>Aegis Secure</i>, suffered a catastrophic breach by the anonymous threat group <b>Black Tide</b>. The attackers exfiltrated <b>Project Chimera</b> — classified internally as an autonomous zero-day cyber weapon platform capable of overriding national defense networks. Before vanishing, Black Tide left a staged server loaded with polyglot artifacts, a shattered RSA prime, a 91-monolith grid cipher, an AST-Lambda SUID gate, and a multi-stage hash seal. This manual documents the complete investigation path — mapping every lore clue to its exact technical operation.
    """
    t_brief = Table([[Paragraph(brief_text, style_body)]], colWidths=[7.0*inch])
    t_brief.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), THEME["callout_bg"]),
        ('BOX', (0,0), (-1,-1), 1, THEME["amber"]),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_brief)

    story.append(PageBreak())

    # CHAPTER 1: STORY RECAP
    story.append(Paragraph("Chapter 1: Story Recap & Sigil Inventory", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=THEME["primary"], spaceAfter=15))

    story.append(Paragraph("""
    <b>Background Storyline:</b><br/>
    Black Tide breached Aegis Secure's internal network via a zero-day staging vector and extracted Project Chimera. Upon exit, Black Tide transmitted a cryptic taunt:
    """, style_body))

    quote_html = """<i>“You protect the world, yet you couldn't protect yourselves. Project Chimera belongs to us now. If you think you can stop us, follow the trail... if you're skilled enough.”</i>"""
    t_quote = Table([[Paragraph(quote_html, style_callout)]], colWidths=[7.0*inch])
    t_quote.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), THEME["callout_bg"]),
        ('LINELEFT', (0,0), (0,-1), 4, THEME["primary"]),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_quote)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Sigil Inventory (What Players Must Recover):</b>", style_h2))
    flags_table_data = [
        ["Lore Name", "Technical Name", "Exact Flag Value", "Stage & Location"],
        ["First Sigil", "Initial Foothold", "AEGIS{ENTRY-7D9A-88E2}", "Stage 1 (Evidence pack)"],
        ["Second Sigil", "Root Access", "AEGIS{PRIV-C4F8-15B7}", "Stage 2 (Web terminal)"],
        ["Chimera Vessel Sigil", "Project Chimera", "AEGIS{CHMR-E1A6-9D40}", "Stage 3 (/var/backups)"]
    ]
    t_flags = Table(flags_table_data, colWidths=[1.6*inch, 1.6*inch, 2.1*inch, 1.7*inch])
    t_flags.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), THEME["primary"]),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), THEME["panel"]),
        ('GRID', (0,0), (-1,-1), 0.5, THEME["border"]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_flags)

    story.append(Spacer(1, 15))

    # CHAPTER 2: LAB SETUP
    story.append(Paragraph("Chapter 2: Lab Setup & Target Connectivity", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=THEME["primary"], spaceAfter=15))

    story.append(Paragraph("""
    <b>Starting the Target Web Server:</b><br/>
    The Aegis Secure CTF web portal runs as a standalone Python web service. To start the server on your local machine or hosting environment, execute:
    """, style_body))

    code_start = """$ python server.py\n[+] AEGIS SECURE CTF — OPERATION BLACK TIDE SERVER RUNNING\n[+] Hosting Web UI at: http://localhost:3000"""
    story.append(Table([[Paragraph(code_start.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("""
    <b>Network Accessibility:</b><br/>
    The server binds to <code>0.0.0.0:3000</code>. Players can connect locally via <code>http://localhost:3000</code> or remotely across a LAN/Wi-Fi router via <code>http://&lt;HOST_IP&gt;:3000</code>.
    """, style_body))

    story.append(PageBreak())

    # CHAPTER 3: STAGE 1
    story.append(Paragraph("Chapter 3: Stage 1 — Breach Scene Investigation & First Sigil", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=THEME["primary"], spaceAfter=15))

    story.append(Paragraph("""
    <b>Step 1.1: Download & Unpack Evidence Package</b><br/>
    The player clicks <b>DOWNLOAD BREACH SCENE EVIDENCE</b> on the web portal and unpacks the archive on Kali Linux. Reading <code>README.txt</code> first reveals all investigation lore clues: the two-faced carrier, the broken prime, the 91 stones, the sealed vessel.
    """, style_body))

    cmd1 = "$ unzip blacktide_evidence.zip -d evidence && cd evidence\n$ ls -la\nREADME.txt  blacktide_carrier.jpg  encrypted_entry.bin\ndecrypt_entry.py  solve_rsa_coppersmith.py  backup_key_v1.txt.bak\n\n[RED HERRING] backup_key_v1.txt.bak: 'PASSPHRASE: BlackTide_2025_Legacy_Passcode!'\n→ Deprecated label. Does NOT open the sealed vessel."
    story.append(Table([[Paragraph(cmd1.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Step 1.2: Carrier Anomaly — Polyglot Extraction</b>", style_h2))
    story.append(Paragraph("""
    <b>What is happening:</b> <code>blacktide_carrier.jpg</code> is a dual-format polyglot file — simultaneously a valid JPEG image AND a valid ZIP archive. Image viewers stop reading at the JPEG End-Of-Image marker (<code>0xFFD9</code>). Archive tools scan for the ZIP Central Directory header (<code>PK\\x03\\x04</code>) further inside and unpack it.
    """, style_body))

    cmd2 = "$ file blacktide_carrier.jpg\n→ JPEG image data\n$ unzip blacktide_carrier.jpg\nArchive:  blacktide_carrier.jpg\n  extracting: rsa_leak.json\n  extracting: monolith_cipher.txt"
    story.append(Table([[Paragraph(cmd2.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Step 1.3: Shattered Prime Reconstruction (rsa_leak.json)</b>", style_h2))
    story.append(Paragraph("""
    <b>What is happening:</b> The prime <code>p</code> used during the breach was shattered — its upper 302 bits leaked into <code>rsa_leak.json</code>. Because the unknown lower portion is small relative to the modulus, <code>solve_rsa_coppersmith.py</code> brute-forces the missing bits, recovers <code>p</code> and <code>q</code>, computes the private key, and decrypts the RSA ciphertext to extract the ancient clock seed. The solver also automatically decodes the monolith cipher stream in one run.
    """, style_body))

    cmd3 = "$ python3 solve_rsa_coppersmith.py\n[*] Reconstructing prime factor p from high bits...\n[+] FOUND PRIME FACTOR p: 13501726058097950550064560...\n[+] FOUND PRIME FACTOR q: 13426176523961127027581177...\n[+] DECRYPTED RSA MESSAGE: SEED_TIMESTAMP:1785355642\n[+] The monolith stream revealed: PASSPHRASE:BT_COPPERSMITH_AES_2026!\n\nAncient Clock Seed: 1785355642\nVessel Key: BT_COPPERSMITH_AES_2026!"
    story.append(Table([[Paragraph(cmd3.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Step 1.4 & 1.5: 91-Monolith Grid Decode & Open Sealed Vessel</b>", style_h2))
    story.append(Paragraph("""
    <b>What is happening:</b> <code>monolith_cipher.txt</code> is encoded with a custom 91-glyph S-Box cipher, shuffled via Fisher-Yates seeded by <code>1785355642</code>. The solver decodes it automatically — output is the vessel key. That key is passed to <code>decrypt_entry.py</code> to open the sealed vessel (<code>encrypted_entry.bin</code>).
    """, style_body))

    cmd4 = "$ python3 decrypt_entry.py 'BT_COPPERSMITH_AES_2026!'\n\n[+] The sealed entry vessel opened. Contents:\n\n==================================================\nBREACH RECORD — STAGING FOOTHOLD ARTIFACT\n==================================================\nThreat Actor: Black Tide\nCompromised Identity: staging_admin\nFirst Sigil: AEGIS{ENTRY-7D9A-88E2}\n\nThis sigil grants passage to the staging server console.\n=================================================="
    story.append(Table([[Paragraph(cmd4.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    thinking_1 = """
    <b>STAGE 1 — INVESTIGATOR REASONING GUIDE (LORE → TECHNICAL MAPPING)</b><br/>
    • "The image holds two faces" → JPEG polyglot ZIP — run <code>unzip</code> on the JPG<br/>
    • "A prime was broken — upper portion survived" → <code>rsa_leak.json</code> p_upper_bits<br/>
    • "Restore what was broken → something speaks" → Run solver → recovers clock seed 1785355642<br/>
    • "91 obsidian stones shifting with the clock" → 91-Monolith Grid cipher, seeded PRNG<br/>
    • "The sealed vessel" → <code>encrypted_entry.bin</code> opened with <code>BT_COPPERSMITH_AES_2026!</code>
    """
    t_think1 = Table([[Paragraph(thinking_1, style_body)]], colWidths=[7.0*inch])
    t_think1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), THEME["panel"]),
        ('BOX', (0,0), (-1,-1), 1, THEME["secondary"]),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_think1)

    story.append(PageBreak())

    # CHAPTER 4: STAGE 2
    story.append(Paragraph("Chapter 4: Stage 2 — Staging Server & Second Sigil", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=THEME["primary"], spaceAfter=15))

    story.append(Paragraph("""
    <b>Step 2.1: Establish Access</b><br/>
    The player enters <code>AEGIS{ENTRY-7D9A-88E2}</code> in the web portal and clicks <b>ESTABLISH ACCESS</b>. The interactive terminal opens as <code>analyst@aegis-staging-node-04</code>.
    """, style_body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Steps 2.2–2.4: Enumeration, Bash History & Audit Log</b>", style_h2))
    cmd5 = "$ ls -la && cat .bash_history\n...\nexport TEMP_KEY=test      ← RED HERRING\nexport AEGIS_AUTH=123     ← RED HERRING\nexport VAULT_KEY=???      ← attacker's failed attempt\n\n$ sudo -l\n    (root) NOPASSWD: /opt/aegis/bin/vault_check\n\n$ cat /var/log/blacktide_audit.log\n[02:15:01] INTERCEPTED MEMORY TRACE: \"The AST gate measures 24 glyphs in length.\nOperative Echo inscribed the key by reflecting the cipher 'BlackTide_Root_Override'\nthrough the 13th mirror of Caesar...\""
    story.append(Table([[Paragraph(cmd5.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Step 2.5: Binary String Analysis & Caesar Mirror Derivation</b>", style_h2))
    story.append(Paragraph("""
    Running <code>strings /opt/aegis/bin/vault_check</code> reveals: <i>"The name they used to break in — seen backwards through Caesar's thirteenth mirror — is the only key this gate will accept."</i><br/>
    Combining both clues: <b>BlackTide_Root_Override</b> shifted 13 positions (Caesar mirror / ROT13) yields: <code>OynpxGvqr_Ebbg_Bireevqr</code>
    """, style_body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Step 2.6: Root Privilege Escalation</b>", style_h2))
    cmd6 = "$ export VAULT_KEY=OynpxGvqr_Ebbg_Bireevqr\n$ /opt/aegis/bin/vault_check\n\n[+] The AST-Lambda gate accepted the aura.\n[+] Root spirit awakened within the Aegis Security Core.\n[+] The crown of the system now rests on your head.\n\n[SECOND SIGIL RECOVERED]: AEGIS{PRIV-C4F8-15B7}\n\n[BLACK TIDE WHISPER]: \"Everything you have recovered must be bound together\nbefore the final chest opens.\""
    story.append(Table([[Paragraph(cmd6.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    thinking_2 = """
    <b>STAGE 2 — INVESTIGATOR REASONING GUIDE (LORE → TECHNICAL MAPPING)</b><br/>
    • "Audit footprints in /var/log" → <code>cat /var/log/blacktide_audit.log</code><br/>
    • "AST-Lambda entity in /opt/aegis/bin" → <code>vault_check</code> SUID binary<br/>
    • "The 13th mirror of Caesar" → ROT13 — shift each letter by 13 positions<br/>
    • "The name they used to break in" → <code>BlackTide_Root_Override</code><br/>
    • Applying mirror → <code>OynpxGvqr_Ebbg_Bireevqr</code> → export as VAULT_KEY<br/>
    • After escalation: <code>whoami</code> returns <code>root</code>, prompt becomes <code>#</code>
    """
    t_think2 = Table([[Paragraph(thinking_2, style_body)]], colWidths=[7.0*inch])
    t_think2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), THEME["panel"]),
        ('BOX', (0,0), (-1,-1), 1, THEME["secondary"]),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_think2)

    story.append(PageBreak())

    # CHAPTER 5: STAGE 3
    story.append(Paragraph("Chapter 5: Stage 3 — Project Chimera Recovery & Chimera Vessel Sigil", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=THEME["primary"], spaceAfter=15))

    story.append(Paragraph("""
    <b>Step 3.1 & 3.2: Vault Exploration & Chimera Manifest</b><br/>
    As <code>root</code>, navigate to <code>/var/backups</code>. Filter the red herrings (<code>chimera_v3_old.bak</code> = corrupted; <code>unused_env.conf</code> = unused DB password). Read <code>chimera_clue_manifest.txt</code>:
    """, style_body))

    cmd7 = "$ cd /var/backups && ls -la\nproject_chimera_v4.enc  chimera_clue_manifest.txt\nchimera_v3_old.bak      unused_env.conf\n\n$ cat chimera_clue_manifest.txt\n\n==================================================\nPROJECT CHIMERA — THE SEAL OF DUAL TRUTHS\n==================================================\nThe First Sigil (FLAG 1) and Second Sigil (FLAG 2) were never meant to stand alone.\nThe forgotten clock time from the first trial remembers their meeting.\n1. Combine First Sigil, Second Sigil, and Ancient Clock Seed from Stage 1.\n2. Join with twin-dot monolith separators (:): \"FLAG1:FLAG2:CLOCK_SEED\"\n3. Pass through the 256-bit Iron Forge → 64-character hex key.\n4. python3 /opt/aegis/tools/decrypt_chimera.py --key <SIXTY_FOUR_MARK_IRON_SEAL>"
    story.append(Table([[Paragraph(cmd7.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Step 3.3: Multi-Stage Hash Synthesis (The Iron Forge)</b>", style_h2))
    story.append(Paragraph("""
    <b>Input assembly:</b> Combine all three investigation pieces in order, separated by colons (<code>:</code>):<br/>
    <code>AEGIS{ENTRY-7D9A-88E2}:AEGIS{PRIV-C4F8-15B7}:1785355642</code><br/>
    Pass through SHA256 — the 256-bit Iron Forge — to produce the 64-mark seal.
    """, style_body))
    cmd8 = "$ echo -n 'AEGIS{ENTRY-7D9A-88E2}:AEGIS{PRIV-C4F8-15B7}:1785355642' | sha256sum\nb3a7f29f35ef4e9c706c7e044aa835c973ca8d6b9cbe5632366c091c3434cb0a\n\n$ python3 /opt/aegis/tools/decrypt_chimera.py --key b3a7f29f35ef4e9c706c7e044aa835c973ca8d6b9cbe5632366c091c3434cb0a\n\n[+] AEGIS PROJECT CHIMERA ARCHIVE DECRYPTION SUCCESSFUL!\nCLASSIFICATION: TOP SECRET // AUTONOMOUS ZERO-DAY WEAPON PLATFORM\n\n\"Project Chimera was never a shield. It is an autonomous zero-day cyber weapon\ncapable of overriding national defense networks and taking down power grids.\"\n\n[RECOVERED CHIMERA VESSEL SIGIL]: AEGIS{CHMR-E1A6-9D40}"
    story.append(Table([[Paragraph(cmd8.replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 10))
    thinking_3 = """
    <b>STAGE 3 — INVESTIGATOR REASONING GUIDE (LORE → TECHNICAL MAPPING)</b><br/>
    • "First and Second Sigil were never meant to stand alone" → Combine both flags<br/>
    • "The forgotten clock from the first trial" → Seed <code>1785355642</code> from Stage 1<br/>
    • "Twin-dot monolith separator" → Colon <code>:</code> between each value<br/>
    • "256-bit Iron Forge — 64-mark seal" → SHA256 hash (64 hex characters)<br/>
    • The three-piece input string: <code>FLAG1:FLAG2:1785355642</code><br/>
    • Correct hash: <code>b3a7f29f35ef4e9c706c7e044aa835c973ca8d6b9cbe5632366c091c3434cb0a</code>
    """
    t_think3 = Table([[Paragraph(thinking_3, style_body)]], colWidths=[7.0*inch])
    t_think3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), THEME["panel"]),
        ('BOX', (0,0), (-1,-1), 1, THEME["secondary"]),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_think3)

    story.append(Spacer(1, 15))

    # CHAPTER 6: INVESTIGATION CHAIN DIAGRAM
    story.append(Paragraph("Chapter 6: Investigation Chain & Visual Summary", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=THEME["primary"], spaceAfter=15))

    attack_path_diagram = """
    +-----------------------------------------------------------------------------------+
    |              OPERATION BLACK TIDE — FULL INVESTIGATION CHAIN                      |
    +-----------------------------------------------------------------------------------+
    |  [1.  Breach Scene]   --> Download blacktide_evidence.zip + Read README.txt      |
    |  [2.  Carrier Anomaly]--> unzip blacktide_carrier.jpg (Two faces — one hidden)   |
    |  [3.  Broken Prime]   --> solve_rsa_coppersmith.py → Clock seed: 1785355642      |
    |  [4.  Stone Shifting] --> 91-Monolith Grid decode → Vessel key recovered         |
    |  [5.  First Sigil]    --> decrypt_entry.py → AEGIS{ENTRY-7D9A-88E2}             |
    |  [6.  Web Terminal]   --> Login → Enumerate → .bash_history → audit.log          |
    |  [7.  Caesar Mirror]  --> BlackTide_Root_Override → OynpxGvqr_Ebbg_Bireevqr     |
    |  [8.  Second Sigil]   --> vault_check SUID → AEGIS{PRIV-C4F8-15B7}              |
    |  [9.  Iron Forge]     --> SHA256(Sigil1:Sigil2:1785355642) → 64-char seal        |
    |  [10. Chimera Vessel] --> decrypt_chimera.py → AEGIS{CHMR-E1A6-9D40} → Victory |
    +-----------------------------------------------------------------------------------+
    """
    story.append(Table([[Paragraph(attack_path_diagram.replace(' ', '&nbsp;').replace('\n', '<br/>'), style_code)]], colWidths=[7.0*inch], style=[('BACKGROUND', (0,0), (-1,-1), THEME["code_bg"]), ('BOX', (0,0), (-1,-1), 1, THEME["primary"]), ('PADDING', (0,0), (-1,-1), 8)]))

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Post-Mortem & Professional Takeaways:</b>", style_h2))
    story.append(Paragraph("""
    1. <b>Polyglot File Integrity:</b> File formats parse headers differently. Always scan media with multi-format engines (<code>binwalk</code>, <code>yara</code>, <code>file</code>).<br/>
    2. <b>Partial RSA Prime Leaks:</b> Even upper bits of prime <code>p</code> completely break RSA hardness. Internal key structures must never appear in logs or memory dumps.<br/>
    3. <b>Predictable PRNG Seeds:</b> Never seed RNGs with Unix timestamps. An attacker recovering the seed can reconstruct all RNG output.<br/>
    4. <b>SUID Environment Sanitization:</b> SUID binaries must enforce <code>env_reset</code> and <code>clearenv()</code>. User-controlled env vars are a direct escalation vector.<br/>
    5. <b>Multi-Stage Hash Binding:</b> Requiring synthesized proof from all stages (both sigils + ancient clock seed) prevents milestone-bypassing and forces the full investigation chain.
    """, style_body))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] PDF with theme '{theme_name}' generated at:\n    {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    theme_arg = sys.argv[1] if len(sys.argv) > 1 else "executive_light"
    build_pdf(theme_arg)
