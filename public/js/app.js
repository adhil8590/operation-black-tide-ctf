/* ==========================================================================
   AEGIS SECURE DFIR TERMINAL ENGINE & ANTI-INSPECT GUARD
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const authForm = document.getElementById('authForm');
  const flag1Input = document.getElementById('flag1Input');
  const authErrorMessage = document.getElementById('authErrorMessage');
  
  const authGateSection = document.getElementById('authGateSection');
  const terminalSection = document.getElementById('terminalSection');
  
  const termInput = document.getElementById('termInput');
  const terminalOutput = document.getElementById('terminalOutput');
  const terminalBody = document.getElementById('terminalBody');
  const promptUser = document.getElementById('promptUser');
  const promptCwd = document.getElementById('promptCwd');
  const promptChar = document.getElementById('promptChar');

  // Flag Tracker DOM
  const flag2Val = document.getElementById('flag2Val');
  const badgeFlag2 = document.getElementById('badgeFlag2');
  const stepFlag2 = document.getElementById('stepFlag2');
  const flag3Val = document.getElementById('flag3Val');
  const badgeFlag3 = document.getElementById('badgeFlag3');
  const stepFlag3 = document.getElementById('stepFlag3');
  
  const victoryModal = document.getElementById('victoryModal');
  const modalClose = document.getElementById('modalClose');

  // Security Toast Element
  const securityToast = document.getElementById('securityToast');

  // State Management
  let sessionToken = null;
  let historyList = [];
  let historyIndex = -1;

  // -------------------------------------------------------------
  // 1. STRICT ANTI-INSPECT & TAMPER GUARD
  // -------------------------------------------------------------
  function showSecurityToast() {
    if (securityToast) {
      securityToast.classList.remove('hidden');
      setTimeout(() => {
        securityToast.classList.add('hidden');
      }, 3000);
    }
  }

  // Disable Right-Click Context Menu
  document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    showSecurityToast();
  });

  // Disable Developer Shortcut Keys
  document.addEventListener('keydown', (e) => {
    // F12
    if (e.key === 'F12' || e.keyCode === 123) {
      e.preventDefault();
      showSecurityToast();
      return false;
    }
    // Ctrl+Shift+I / Cmd+Option+I (Inspect element)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.keyCode === 73)) {
      e.preventDefault();
      showSecurityToast();
      return false;
    }
    // Ctrl+Shift+J / Cmd+Option+J (Console)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'J' || e.key === 'j' || e.keyCode === 74)) {
      e.preventDefault();
      showSecurityToast();
      return false;
    }
    // Ctrl+Shift+C / Cmd+Option+C (Inspect node)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'C' || e.key === 'c' || e.keyCode === 67)) {
      e.preventDefault();
      showSecurityToast();
      return false;
    }
    // Ctrl+U / Cmd+Option+U (View Source)
    if ((e.ctrlKey || e.metaKey) && (e.key === 'U' || e.key === 'u' || e.keyCode === 85)) {
      e.preventDefault();
      showSecurityToast();
      return false;
    }
    // Ctrl+S / Cmd+S (Save Page)
    if ((e.ctrlKey || e.metaKey) && (e.key === 'S' || e.key === 's' || e.keyCode === 83)) {
      e.preventDefault();
      showSecurityToast();
      return false;
    }
  });

  // -------------------------------------------------------------
  // 2. FOOTHOLD AUTHENTICATION (FLAG 1 LOGIN)
  // -------------------------------------------------------------
  if (authForm) {
    authForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const flag1Val = flag1Input.value.trim();

      if (!flag1Val) return;

      try {
        const res = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ flag1: flag1Val })
        });
        const data = await res.json();

        if (data.success) {
          sessionToken = data.session_token;
          authGateSection.classList.add('hidden');
          terminalSection.classList.remove('hidden');
          termInput.focus();
        } else {
          authErrorMessage.textContent = data.message || "The gate did not recognize that sigil.";
          authErrorMessage.classList.remove('hidden');
        }
      } catch (err) {
        authErrorMessage.textContent = "Connection to the Aegis node was lost. Try again.";
        authErrorMessage.classList.remove('hidden');
      }
    });
  }

  // -------------------------------------------------------------
  // 3. INTERACTIVE TERMINAL EXECUTION ENGINE
  // -------------------------------------------------------------
  if (termInput) {
    // Keep focus inside terminal
    terminalBody.addEventListener('click', () => termInput.focus());

    termInput.addEventListener('keydown', async (e) => {
      // Command History Navigation (Up/Down Arrow)
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (historyList.length > 0 && historyIndex < historyList.length - 1) {
          historyIndex++;
          termInput.value = historyList[historyList.length - 1 - historyIndex];
        }
        return;
      }
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (historyIndex > 0) {
          historyIndex--;
          termInput.value = historyList[historyList.length - 1 - historyIndex];
        } else if (historyIndex === 0) {
          historyIndex = -1;
          termInput.value = '';
        }
        return;
      }

      // Execute Command on Enter
      if (e.key === 'Enter') {
        const cmd = termInput.value.trim();
        termInput.value = '';
        if (!cmd) return;

        // Save command in history
        historyList.push(cmd);
        historyIndex = -1;

        // Display user input line in output
        const userPromptStr = `${promptUser.textContent}:${promptCwd.textContent}${promptChar.textContent} ${cmd}`;
        appendTerminalLine(userPromptStr, 'user-cmd-line');

        // Send to server API
        try {
          const res = await fetch('/api/terminal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              session_token: sessionToken,
              command: cmd
            })
          });

          const data = await res.json();
          if (data.success) {
            if (data.output === '__CLEAR__') {
              terminalOutput.innerHTML = '';
            } else if (data.output) {
              appendTerminalLine(data.output, 'cmd-response');
            }

            // Update User & CWD
            promptUser.textContent = `${data.user}@aegis-staging`;
            promptCwd.textContent = data.cwd;
            promptChar.textContent = data.is_root ? '#' : '$';

            // Check if Flags Solved
            if (data.solved_flags) {
              updateFlagTracker(data.solved_flags);
            }
          } else {
            appendTerminalLine(data.output || "Execution failed.", 'error-msg');
          }
        } catch (err) {
          appendTerminalLine("[Network error — staging node connection dropped.]", 'error-msg');
        }

        // Scroll terminal to bottom
        terminalBody.scrollTop = terminalBody.scrollHeight;
      }
    });
  }

  function appendTerminalLine(text, cssClass = '') {
    const div = document.createElement('div');
    div.className = `terminal-line ${cssClass}`;
    div.textContent = text;
    terminalOutput.appendChild(div);
  }

  // -------------------------------------------------------------
  // 4. FLAG PROGRESS TRACKER & VICTORY MODAL TRIGGER
  // -------------------------------------------------------------
  function updateFlagTracker(solvedFlags) {
    // Second sigil check
    if (solvedFlags.includes('AEGIS{PRIV-C4F8-15B7}')) {
      flag2Val.textContent = 'AEGIS{PRIV-C4F8-15B7}';
      badgeFlag2.textContent = 'RECOVERED';
      stepFlag2.classList.remove('locked');
      stepFlag2.classList.add('completed');
    }

    // Chimera vessel sigil check
    if (solvedFlags.includes('AEGIS{CHMR-E1A6-9D40}')) {
      flag3Val.textContent = 'AEGIS{CHMR-E1A6-9D40}';
      badgeFlag3.textContent = 'RECOVERED';
      stepFlag3.classList.remove('locked');
      stepFlag3.classList.add('completed');

      // Trigger Victory Modal
      setTimeout(() => {
        if (victoryModal) victoryModal.classList.remove('hidden');
      }, 1200);
    }
  }

  if (modalClose) {
    modalClose.addEventListener('click', () => {
      victoryModal.classList.add('hidden');
    });
  }
});
