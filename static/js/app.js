  // ── Pre-defined Branch Subjects Configurations ──
  const BRANCH_SUBJECTS = {
    "1": {
        "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
        "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
        "3": ["CD301", "CD302", "CD303", "CD304", "CD305", "CD303[P]", "CD304[P]", "CD305[P]", "CD306[P]", "BT107[P]"],
        "4": ["CD401[T]", "CD402[T]", "CD403[T]", "CD404[T]", "CD405[T]", "CD402[P]", "CD403[P]", "CD404[P]", "CD405[P]", "CD406[P]"],
        "5": ["CD501", "CD502", "CD503", "CD504", "BT407[P]", "CD501[P]", "CD502[P]", "CD505[P]", "CD506[P]", "CD508[P]"],
        "6": ["CD601[T]", "CD602[T]", "CD603[T]", "CD604[T]", "CD601[P]", "CD602[P]", "CD605[P]", "CD606[P]", "CD608"],
        "7": ["CD701", "CD702", "CD703", "CD704", "CD705"],
        "8": ["CD801", "CD802", "CD803", "CD804", "CD805"]
    },
    "2": { 
        "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
        "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
        "3": ["AL301", "AL302", "AL303", "AL304", "AL305", "AL303[P]", "AL304[P]", "AL305[P]", "AL306[P]", "BT107[P]"],
        "4": ["AL401[T]", "AL402[T]", "AL403[T]", "AL404[T]", "AL405[T]", "AL402[P]", "AL403[P]", "AL404[P]", "AL405[P]", "AL406[P]"],
        "5": ["AL501", "AL502", "AL503", "AL504", "BT407[P]", "AL501[P]", "AL502[P]", "AL505[P]", "AL506[P]", "AL508[P]"],
        "6": ["AL601[T]", "AL602[T]", "AL603[T]", "AL604[T]", "AL601[P]", "AL602[P]", "AL605[P]", "AL606[P]", "AL608"],
        "7": ["AL701", "AL702", "AL703", "AL704", "AL705"],
        "8": ["AL801", "AL802", "AL803", "AL804", "AL805"] 
    },
    "3": { 
        "1": ["BT101[T]", "BT102[T]", "BT103[T]", "BT104[T]", "BT105[T]", "BT101[P]", "BT103[P]", "BT104[P]", "BT105[P]", "BT106[P]", "BT108[P]"],
        "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
        "3": ["ES301", "CS302", "CS303", "CS304", "CS305", "CS303[P]", "CS304[P]", "CS305[P]", "CS306[P]", "BT107[P]"],
        "4": ["CS401[T]", "CS402[T]", "CS403[T]", "CS404[T]", "CS405[T]", "CS402[P]", "CS403[P]", "CS404[P]", "CS405[P]", "CS406[P]"],
        "5": ["CS501", "CS502", "CS503", "CS504", "BT407[P]", "CS501[P]", "CS502[P]", "CS505[P]", "CS506[P]", "CS508[P]"],
        "6": ["CS601[T]", "CS602[T]", "CS603[T]", "CS604[T]", "CS601[P]", "CS602[P]", "CS605[P]", "CS606[P]", "CS608"],
        "7": ["CS701", "CS702", "CS703", "CS704", "CS705"],
        "8": ["CS801", "CS802", "CS803", "CS804", "CS805"] 
    },
    "4": { 
        "1": ["BT101[T]", "BT102[T]", "BT103[T]", "BT104[T]", "BT105[T]", "BT101[P]", "BT103[P]", "BT104[P]", "BT105[P]", "BT106[P]", "BT108[P]"],
        "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
        "3": ["ES301", "IT302", "IT303", "IT304", "IT305", "IT303[P]", "IT304[P]", "IT305[P]", "IT306[P]", "BT107[P]"],
        "4": ["IT401[T]", "IT402[T]", "IT403[T]", "IT404[T]", "IT405[T]", "IT402[P]", "IT403[P]", "IT404[P]", "IT405[P]", "IT406[P]"],
        "5": ["IT501", "IT502", "IT503", "IT504", "BT408[P]", "IT501[P]", "IT502[P]", "IT505[P]", "IT506[P]", "IT508[P]"],
        "6": ["IT601[T]", "IT602[T]", "IT603[T]", "IT604[T]", "IT601[P]", "IT602[P]", "IT605[P]", "IT606[P]", "IT608"],
        "7": ["IT701", "IT702", "IT703", "IT704", "IT705"],
        "8": ["IT801", "IT802", "IT803", "IT804", "IT805"] 
    },
    "5": { 
        "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
        "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
        "3": ["CY301", "CY302", "CY303", "CY304", "CY305", "CY303[P]", "CY304[P]", "CY305[P]", "CY306[P]", "BT107[P]"],
        "4": ["CY401[T]", "CY402[T]", "CY403[T]", "CY404[T]", "CY405[T]", "CY402[P]", "CY403[P]", "CY404[P]", "CY405[P]", "CY406[P]"],
        "5": ["CY501", "CY502", "CY503", "CY504", "BT407[P]", "CY501[P]", "CY502[P]", "CY505[P]", "CY506[P]", "CY508[P]"],
        "6": ["CY601[T]", "CY602[T]", "CY603[T]", "CY604[T]", "CY601[P]", "CY602[P]", "CY605[P]", "CY606[P]", "CY608"],
        "7": ["CY701", "CY702", "CY703", "CY704", "CY705"],
        "8": ["CY801", "CY802", "CY803", "CY804", "CY805"] 
    },
    "6": { 
        "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
        "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
        "3": ["IO301", "IO302", "IO303", "IO304", "IO305", "IO303[P]", "IO304[P]", "IO305[P]", "IO306[P]", "BT107[P]"],
        "4": ["IO401[T]", "IO402[T]", "IO403[T]", "IO404[T]", "IO405[T]", "IO402[P]", "IO403[P]", "IO404[P]", "IO405[P]", "IO406[P]"],
        "5": ["IO501", "IO502", "IO503", "IO504", "BT407[P]", "IO501[P]", "IO502[P]", "IO505[P]", "IO506[P]", "IO508[P]"],
        "6": ["IO601[T]", "IO602[T]", "IO603[T]", "IO604[T]", "IO601[P]", "IO602[P]", "IO605[P]", "IO606[P]", "IO608"],
        "7": ["IO701", "IO702", "IO703", "IO704", "IO705"],
        "8": ["IO801", "IO802", "IO803", "IO804", "IO805"] 
    },
    "mca": {
        "1": ["MCA101", "MCA102", "MCA103", "MCA104", "MCA105", "MCA101[P]", "MCA102[P]", "MCA103[P]", "MCA105[P]"],
        "2": ["MCA201", "MCA202", "MCA203", "MCA204", "MCA205", "MCA201[P]", "MCA202[P]", "MCA203[P]", "MCA205[P]"],
        "3": ["MCA301", "MCA302", "MCA303", "MCA304", "MCA305", "MCA301[P]", "MCA302[P]", "MCA303[P]", "MCA305[P]"],
        "4": ["MCA401", "MCA402", "MCA403", "MCA404", "MCA405", "MCA401[P]", "MCA402[P]", "MCA403[P]", "MCA405[P]"]
    }
  };

  // ── Manual Batch / Prefix Configuration ──────────
  const BRANCH_PREFIXES = {
    "1": "0905CD",
    "2": "0905AL",
    "3": "0905CS",
    "4": "0905IT",
    "5": "0905CY",
    "6": "0905IO",
    "mca": "0905CA"
  };

  function toggleManualBatch() {
    const chk = document.getElementById('manual-batch-chk');
    const standardSelect = document.getElementById('batch-year-select');
    const manualContainer = document.getElementById('manual-batch-container');
    
    if (chk.checked) {
      standardSelect.style.display = 'none';
      manualContainer.style.display = 'block';
    } else {
      standardSelect.style.display = 'block';
      manualContainer.style.display = 'none';
    }
    updateManualPrefixPreview();
  }

  function toggleAdvancedSettings() {
    const content = document.getElementById('advanced-settings-content');
    const arrow = document.getElementById('adv-arrow');
    if (content.style.display === 'none') {
      content.style.display = 'block';
      arrow.textContent = '▼';
    } else {
      content.style.display = 'none';
      arrow.textContent = '▶';
    }
  }

  function toggleEngineSettings() {
    const content = document.getElementById('engine-settings-content');
    const arrow = document.getElementById('engine-arrow');
    if (content.style.display === 'none') {
      content.style.display = 'block';
      arrow.style.transform = 'rotate(90deg)';
    } else {
      content.style.display = 'none';
      arrow.style.transform = 'rotate(0deg)';
    }
  }

  function toggleWaitMode() {
    const mode = document.getElementById('wait-mode').value;
    const label = document.getElementById('wait-value-label');
    const input = document.getElementById('wait-value');
    const slider = document.getElementById('wait-value-slider');
    const badge = document.getElementById('range-val-badge');
    const desc = document.getElementById('wait-mode-desc');
    
    if (mode === 'dynamic') {
      label.textContent = 'Max Timeout Limit';
      slider.min = '5';
      slider.max = '45';
      slider.step = '1';
      slider.value = '25';
      input.value = '25';
      badge.textContent = '25s';
      desc.textContent = 'Waits up to 25s for portal response, continues instantly when ready.';
    } else {
      label.textContent = 'Fixed Sleep Duration';
      slider.min = '1';
      slider.max = '10';
      slider.step = '0.5';
      slider.value = '3.5';
      input.value = '3.5';
      badge.textContent = '3.5s';
      desc.textContent = 'Waits for exactly 3.5s regardless of portal load speed.';
    }
    updateStepsProgress();
  }

  function onSliderChange() {
    const slider = document.getElementById('wait-value-slider');
    const input = document.getElementById('wait-value');
    const badge = document.getElementById('range-val-badge');
    
    input.value = slider.value;
    badge.textContent = slider.value + 's';
    
    badge.classList.add('scale');
    setTimeout(() => {
      badge.classList.remove('scale');
    }, 200);
  }

  function onSubmitDelaySliderChange() {
    const slider = document.getElementById('submit-delay-slider');
    const input = document.getElementById('submit-delay');
    const badge = document.getElementById('submit-delay-badge');
    
    input.value = slider.value;
    badge.textContent = slider.value + 's';
    
    badge.classList.add('scale');
    setTimeout(() => {
      badge.classList.remove('scale');
    }, 200);

    // Dynamic sync if running
    syncSubmitDelayToBackend(parseFloat(slider.value));
  }

  async function syncSubmitDelayToBackend(val) {
    if (state.running) {
      try {
        await fetch('/api/update_wait', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ submit_delay: val })
        });
      } catch (e) {
        console.error('Failed to sync submit delay to backend:', e);
      }
    }
  }

  function onResetDelaySliderChange() {
    const slider = document.getElementById('reset-delay-slider');
    const input = document.getElementById('reset-delay');
    const badge = document.getElementById('reset-delay-badge');
    
    input.value = slider.value;
    badge.textContent = slider.value + 's';
    
    badge.classList.add('scale');
    setTimeout(() => {
      badge.classList.remove('scale');
    }, 200);

    // Dynamic sync if running
    syncResetDelayToBackend(parseFloat(slider.value));
  }

  async function syncResetDelayToBackend(val) {
    if (state.running) {
      try {
        await fetch('/api/update_wait', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ reset_delay: val })
        });
      } catch (e) {
        console.error('Failed to sync reset delay to backend:', e);
      }
    }
  }

  async function onSpeedModeChange() {
    const val = document.getElementById('speed-mode').value;
    state.speedMode = val;
    log(`Speed mode adjusted to: ${val}`, 'info');

    // Auto-update submit delay based on speed mode preset
    const speedSubmitDelays = {
      slow: 2.0,
      normal: 1.5,
      fast: 0.8,
      turbo: 0.2
    };
    const targetDelay = speedSubmitDelays[val] || 1.5;
    const slider = document.getElementById('submit-delay-slider');
    const input = document.getElementById('submit-delay');
    const badge = document.getElementById('submit-delay-badge');
    if (slider && input && badge) {
      slider.value = targetDelay;
      input.value = targetDelay;
      badge.textContent = targetDelay + 's';
    }

    // Auto-update reset delay based on speed mode preset
    const speedResetDelays = {
      slow: 1.5,
      normal: 0.5,
      fast: 0.2,
      turbo: 0.0
    };
    const targetResetDelay = speedResetDelays[val] !== undefined ? speedResetDelays[val] : 0.5;
    const rSlider = document.getElementById('reset-delay-slider');
    const rInput = document.getElementById('reset-delay');
    const rBadge = document.getElementById('reset-delay-badge');
    if (rSlider && rInput && rBadge) {
      rSlider.value = targetResetDelay;
      rInput.value = targetResetDelay;
      rBadge.textContent = targetResetDelay + 's';
    }

    // If a session is active, update the backend too
    if (state.running) {
      try {
        await fetch('/api/update_wait', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            speed_mode: val,
            submit_delay: targetDelay,
            reset_delay: targetResetDelay
          })
        });
      } catch (e) {
        console.error('Failed to sync speed/delays to backend:', e);
      }
    }
  }

  function toggleTheme() {
    const isLight = document.documentElement.classList.toggle('light-theme');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    updateThemeToggleIcon(isLight);
  }

  function updateThemeToggleIcon(isLight) {
    const btn = document.getElementById('theme-toggle-btn');
    if (btn) {
      btn.textContent = isLight ? '🌙' : '☀️';
    }
  }

  function updateStepsProgress() {
    const step1 = document.getElementById('step-node-1');
    const step2 = document.getElementById('step-node-2');
    const step3 = document.getElementById('step-node-3');
    const step4 = document.getElementById('step-node-4');
    const progressFill = document.getElementById('steps-progress-fill');
    
    if (!step1 || !step2 || !step3 || !step4 || !progressFill) return;
    
    const nodes = [step1, step2, step3, step4];
    nodes.forEach(n => {
      n.classList.remove('active', 'completed');
    });
    
    step1.classList.add('completed');
    
    let activeStep = 2;
    
    const isUploaded = isUploadMode() ? (state.rollList && state.rollList.length > 0) : true;
    if (isUploaded) {
      step2.classList.add('completed');
      activeStep = 3;
    } else {
      step2.classList.add('active');
    }
    
    if (activeStep >= 3) {
      step3.classList.add('completed');
      activeStep = 4;
    }
    
    if (state.running) {
      step4.classList.add('active');
      activeStep = 4;
    } else if (isUploaded) {
      step4.classList.add('active');
    }
    
    const completedCount = nodes.filter(n => n.classList.contains('completed')).length;
    const percent = Math.min(100, Math.round(((completedCount - 1) / 3) * 100));
    progressFill.style.width = percent + '%';
  }

  function toggleRowDetails(roll, d) {
    const existingDetails = document.getElementById(`details-${roll}`);
    if (existingDetails) {
      existingDetails.remove();
      return;
    }
    
    document.querySelectorAll('.details-row').forEach(row => row.remove());
    
    const studentRow = document.getElementById(`row-${roll}`);
    if (!studentRow) return;
    
    const colCount = 6 + state.activeSubjects.length;
    const detailsRow = document.createElement('tr');
    detailsRow.id = `details-${roll}`;
    detailsRow.className = 'details-row';
    
    let subjectHtml = '';
    for (let subKey in d.subjects) {
      const grade = d.subjects[subKey];
      let gradeColor = "var(--text)";
      const gUpper = grade.trim().toUpperCase();
      if (["F", "ABS", "ABSENT", "W"].some(g => gUpper.includes(g))) {
        gradeColor = "var(--fail)";
      } else if (["O", "A+", "A", "B+", "B", "C+", "C", "D", "P"].some(g => gUpper.startsWith(g))) {
        gradeColor = "var(--pass)";
      }
      
      subjectHtml += `
        <div class="subject-mini-card">
          <span class="sub-mini-code">${subKey}</span>
          <span class="sub-mini-grade" style="color: ${gradeColor};">${grade}</span>
        </div>
      `;
    }
    
    detailsRow.innerHTML = `
      <td colspan="${colCount}" style="padding: 0 18px 14px 18px;">
        <div class="expanded-card">
          <div class="expanded-card-header">
            <span class="expanded-card-title">📖 Marks breakdown for ${d.name} (${roll})</span>
            <span style="font-size: 0.72rem; color: var(--muted); font-family: var(--mono);">SGPA: <strong style="color: var(--accent2); font-size: 0.82rem;">${d.sgpa}</strong>  |  CGPA: <strong style="color: var(--accent2); font-size: 0.82rem;">${d.cgpa}</strong></span>
          </div>
          <div class="subject-grid">
            ${subjectHtml || '<div style="color:var(--muted); font-size:0.7rem;">No subject-wise grade details available</div>'}
          </div>
        </div>
      </td>
    `;
    
    studentRow.after(detailsRow);
  }


  function toggleProgramMode() {
    const program = document.getElementById('program').value;
    const branchContainer = document.getElementById('branch-select-container');
    const semSelect = document.getElementById('sem');
    
    if (program === 'MCA') {
      branchContainer.style.display = 'none';
      
      let semHtml = `
        <option value="1" selected>Semester 1</option>
        <option value="2">Semester 2</option>
        <option value="3">Semester 3</option>
        <option value="4">Semester 4</option>
      `;
      semSelect.innerHTML = semHtml;
    } else {
      branchContainer.style.display = 'block';
      
      let semHtml = `
        <option value="1">Semester 1</option>
        <option value="2" selected>Semester 2</option>
        <option value="3">Semester 3</option>
        <option value="4">Semester 4</option>
        <option value="5">Semester 5</option>
        <option value="6">Semester 6</option>
        <option value="7">Semester 7</option>
        <option value="8">Semester 8</option>
      `;
      semSelect.innerHTML = semHtml;
    }
    updateManualPrefixPreview();
  }

  function updateManualPrefixPreview() {
    const program = document.getElementById('program').value;
    let basePrefix = "0905CS";
    if (program === 'MCA') {
      basePrefix = BRANCH_PREFIXES["mca"] || "0905CA";
    } else {
      const branch = document.getElementById('branch').value;
      basePrefix = BRANCH_PREFIXES[branch] || "0905CS";
    }
    const manualBatchVal = document.getElementById('manual-batch-val').value.trim();
    const manualPrefixVal = document.getElementById('manual-prefix-val').value.trim().toUpperCase();
    
    let preview = "";
    if (manualPrefixVal) {
      preview = manualPrefixVal;
    } else if (manualBatchVal) {
      preview = basePrefix + manualBatchVal;
    } else {
      const sem = document.getElementById('sem').value;
      try {
        const sem_num = parseInt(sem);
        const guessed_year = 26 - Math.floor((sem_num + 1) / 2);
        preview = basePrefix + String(guessed_year).padStart(2, '0');
      } catch (e) {
        preview = basePrefix + "24";
      }
    }
    
    const previewEl = document.getElementById('prefix-preview');
    if (previewEl) {
      previewEl.textContent = preview;
    }
    return preview;
  }

  // ── State ─────────────────────────────────────
  let state = {
    running: false,
    currentRoll: 0,
    startRoll: 0,
    endRoll: 0,
    totalFetched: 0,
    passCount: 0,
    failCount: 0,
    skipCount: 0,
    rowCount: 0,
    emptyCleared: false,
    activeSubjects: [],
    captchaRetries: 0,
    sessionPrefix: "",
    sessionMode: "range",   // "range" or "list"
    speedMode: "normal",    // "slow", "normal", "fast", "turbo"
    submitDelay: 1.5,
    // ── Roll List (Upload) Mode ─────────────────────────────
    rollList: [],           // Full roll numbers from uploaded Excel
    rollListIdx: 0,         // Current position in rollList
    fetchedStudentsData: [] // Successfully fetched students in the current session
  };

  // ── Upload Mode Helper (DOM-based, never gets out of sync) ────────
  function isUploadMode() {
    if (state.running) {
      return state.sessionMode === 'list';
    }
    const el = document.getElementById('upload-roll-section');
    return el && el.style.display !== 'none';
  }

  // ── Log ───────────────────────────────────────
  function log(msg, type='info') {
    console.log(`[${type.toUpperCase()}] ${msg}`);
    const box  = document.getElementById('log-box');
    if (!box) return;
    const time = new Date().toLocaleTimeString('en',{hour12:false,hour:'2-digit',minute:'2-digit',second:'2-digit'});
    const el   = document.createElement('div');
    el.className = 'log-entry';
    el.innerHTML = `<span class="log-time">${time}</span><span class="log-${type}">${msg}</span>`;
    box.appendChild(el);
    box.scrollTop = box.scrollHeight;
  }

  // ── Status bar ────────────────────────────────
  function setStatus(msg, type='idle') {
    const bar = document.getElementById('status-bar');
    bar.className = 'status-bar status-' + type;
    document.getElementById('status-msg').textContent = msg;
    document.getElementById('header-status').textContent =
      type === 'running' ? '● RUNNING' :
      type === 'done'    ? '● DONE'    :
      type === 'error'   ? '● ERROR'   : '● IDLE';
  }

  // ── Input Mode Toggle ─────────────────────────
  function setInputMode(mode) {
    const rangeSection = document.getElementById('manual-range-section');
    const uploadSection = document.getElementById('upload-roll-section');
    const btnRange = document.getElementById('mode-btn-range');
    const btnUpload = document.getElementById('mode-btn-upload');

    if (mode === 'upload') {
      rangeSection.style.display = 'none';
      uploadSection.style.display = 'block';
      btnUpload.style.background = 'linear-gradient(135deg, var(--accent2), #0284c7)';
      btnUpload.style.color = '#fff';
      btnUpload.style.boxShadow = '0 2px 8px rgba(14,165,233,0.25)';
      btnRange.style.background = 'transparent';
      btnRange.style.color = 'var(--muted)';
      btnRange.style.boxShadow = 'none';
    } else {
      rangeSection.style.display = 'block';
      uploadSection.style.display = 'none';
      btnRange.style.background = 'linear-gradient(135deg, var(--accent), #059669)';
      btnRange.style.color = '#fff';
      btnRange.style.boxShadow = '0 2px 8px rgba(16,185,129,0.25)';
      btnUpload.style.background = 'transparent';
      btnUpload.style.color = 'var(--muted)';
      btnUpload.style.boxShadow = 'none';
    }
    updateStepsProgress();
  }

  // ── Upload Roll Sheet: File Handlers ──────────
  function handleFileDrop(event) {
    event.preventDefault();
    document.getElementById('upload-dropzone').classList.remove('drop-active');
    const file = event.dataTransfer.files[0];
    if (file) processUploadedFile(file);
  }

  function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) processUploadedFile(file);
  }

  async function processUploadedFile(file) {
    const errorEl = document.getElementById('upload-error');
    const statusEl = document.getElementById('upload-status');
    const countLbl = document.getElementById('upload-count-lbl');
    const detectLbl = document.getElementById('upload-detect-lbl');
    const previewEl = document.getElementById('upload-roll-preview');
    const overrideEl = document.getElementById('upload-branch-override');
    const badgeEl = document.getElementById('upload-branch-badge');
    const branchSel = document.getElementById('upload-branch-select');
    const dropzone = document.getElementById('upload-dropzone');

    // Reset state
    errorEl.style.display = 'none';
    statusEl.style.display = 'none';
    state.rollList = [];
    state.rollListIdx = 0;

    // Show loading indicator
    dropzone.innerHTML = `
      <div style="font-size:1.5rem;margin-bottom:8px;opacity:0.6">⏳</div>
      <div style="font-family:var(--mono);font-size:0.78rem;color:var(--text);font-weight:700">Parsing file...</div>
      <input type="file" id="roll-file-input" accept=".xlsx,.xls,.csv" style="display:none" onchange="handleFileSelect(event)"/>
    `;

    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch('/api/parse_rollsheet', { method: 'POST', body: formData });

      // Read raw text first — if server returned HTML (error page), res.json() would crash
      const rawText = await res.text();
      let data;
      try {
        data = JSON.parse(rawText);
      } catch (jsonErr) {
        // Server returned non-JSON (HTML error page) — show the HTTP status
        const preview = rawText.substring(0, 200).replace(/</g, '&lt;');
        throw new Error(
          `Server returned HTTP ${res.status} (non-JSON).\n` +
          `This usually means the server crashed. Check the server console.\n` +
          `Response preview: ${rawText.substring(0, 100)}`
        );
      }

      // Restore dropzone
      dropzone.innerHTML = `
        <div style="font-size:2rem;margin-bottom:8px;opacity:0.6">📂</div>
        <div style="font-family:var(--mono);font-size:0.78rem;color:var(--text);font-weight:700;margin-bottom:4px">
          ${file.name} — click to change
        </div>
        <div style="font-family:var(--mono);font-size:0.65rem;color:var(--muted)">Supports .xlsx and .csv files</div>
        <input type="file" id="roll-file-input" accept=".xlsx,.xls,.csv" style="display:none" onchange="handleFileSelect(event)"/>
      `;

      if (!data.ok) {
        errorEl.textContent = '⚠️ ' + data.error;
        errorEl.style.display = 'block';
        return;
      }

      // Store roll list
      state.rollList = data.rolls;
      state.rollListIdx = 0;

      // Update preview
      countLbl.textContent = `${data.count} roll numbers loaded from "${file.name}"`;
      
      const chipsWrap = document.getElementById('upload-chips-container');
      if (chipsWrap) {
        chipsWrap.innerHTML = '';
        if (data.detected_branch_name) {
          const bChip = document.createElement('span');
          bChip.className = 'chip-glowing';
          bChip.innerHTML = `🏫 Branch: ${data.detected_branch_name}`;
          chipsWrap.appendChild(bChip);
          
          if (data.detected_year) {
            const yChip = document.createElement('span');
            yChip.className = 'chip-glowing blue';
            yChip.innerHTML = `📅 Batch: 20${data.detected_year}`;
            chipsWrap.appendChild(yChip);
          }
        } else {
          chipsWrap.innerHTML = `<span class="chip-glowing" style="color:var(--fail); border-color:rgba(239,68,68,0.25); background:rgba(239,68,68,0.06)">ℹ️ Auto-detection failed</span>`;
        }
      }

      previewEl.textContent = data.rolls.slice(0, 40).join('  ') + (data.count > 40 ? `  ...+${data.count - 40} more` : '');
      statusEl.style.display = 'block';
      updateStepsProgress();

      // Show branch override section
      overrideEl.style.display = 'block';
      if (data.detected_branch_id) {
        branchSel.value = data.detected_branch_id;
        badgeEl.textContent = data.detected_branch_name;
      } else {
        badgeEl.textContent = 'Unknown';
      }

    } catch (e) {
      // Restore dropzone on error
      dropzone.innerHTML = `
        <div style="font-size:2rem;margin-bottom:8px;opacity:0.6">📂</div>
        <div style="font-family:var(--mono);font-size:0.78rem;color:var(--text);font-weight:700;margin-bottom:4px">Click or drag & drop your file here</div>
        <div style="font-family:var(--mono);font-size:0.65rem;color:var(--muted)">Supports .xlsx and .csv files</div>
        <input type="file" id="roll-file-input" accept=".xlsx,.xls,.csv" style="display:none" onchange="handleFileSelect(event)"/>
      `;
      errorEl.textContent = '⚠️ Network error: ' + e.message;
      errorEl.style.display = 'block';
    }
  }

  function onUploadBranchChange() {
    // When user manually changes branch in upload mode, we need to re-read subjects
    // This will be picked up by startSession when it reads upload-branch-select
  }

  // ── Progress ──────────────────────────────────
  function updateProgress() {
    if (isUploadMode()) {
      const total = state.rollList.length;
      const done  = state.rollListIdx;
      const pct   = total > 0 ? Math.round((done / total) * 100) : 0;
      document.getElementById('progress-bar').style.width  = pct + '%';
      document.getElementById('progress-label').textContent = `${done} / ${total}`;
    } else {
      const total = state.endRoll - state.startRoll + 1;
      const done  = state.currentRoll - state.startRoll;
      const pct   = total > 0 ? Math.round((done / total) * 100) : 0;
      document.getElementById('progress-bar').style.width  = pct + '%';
      document.getElementById('progress-label').textContent = `${done} / ${total}`;
    }
  }


  // ── Stats ─────────────────────────────────────
  function updateStats() {
    document.getElementById('stat-total').textContent = state.totalFetched;
    document.getElementById('stat-pass').textContent  = state.passCount;
    document.getElementById('stat-fail').textContent  = state.failCount;
    document.getElementById('stat-skip').textContent  = state.skipCount;
  }

  // ── Toggle Diploma Mode ────────────────────────
  function toggleDiplomaMode() {
    const isDiploma = document.getElementById('diploma-chk').checked;
    const startInput = document.getElementById('start-roll');
    const endInput = document.getElementById('end-roll');
    
    if (isDiploma) {
      if (startInput.value === '1001') startInput.value = '1';
      if (endInput.value === '1010') endInput.value = '20';
      startInput.min = '1';
    } else {
      if (startInput.value === '1') startInput.value = '1001';
      if (endInput.value === '20') endInput.value = '1010';
      startInput.min = '1000';
    }
  }

  // ── Rebuild Table Header Columns Dynamically ──
  function rebuildTableHeader(preserveActiveSubjects = false) {
    if (!preserveActiveSubjects) {
      const branch = document.getElementById('branch').value;
      const sem = document.getElementById('sem').value;
      let rawSubjects = (BRANCH_SUBJECTS[branch] && BRANCH_SUBJECTS[branch][sem]) ? BRANCH_SUBJECTS[branch][sem] : [];
      state.activeSubjects = rawSubjects.map(s => {
        let sUpper = s.toUpperCase();
        let isPractical = sUpper.includes("[P]") || sUpper.includes("(P)") || sUpper.endsWith("P");
        let isTheory = sUpper.includes("[T]") || sUpper.includes("(T)") || sUpper.endsWith("T");
        let base = s.replace(/[\(\[\{][PT][\)\]\}]/g, "").trim();
        if (isPractical) {
          return base + "[P]";
        } else if (isTheory) {
          return base + "[T]";
        } else {
          return base + "[T]";
        }
      });
    }

    
    let html = `
      <th>#</th>
      <th>Roll Number</th>
      <th>Name</th>
    `;

    state.activeSubjects.forEach(sub => {
      html += `<th style="color:var(--accent2); font-weight: 800; text-align: center; background: rgba(0,119,230,0.03);">${sub}</th>`;
    });

    html += `
      <th>SGPA</th>
      <th>CGPA</th>
      <th>Result</th>
    `;

    document.getElementById('table-header-row').innerHTML = html;
  }

  // ── Add row to table ──────────────────────────
  function addRow(d) {
    if (!state.fetchedStudentsData) {
      state.fetchedStudentsData = [];
    }
    const idx = state.fetchedStudentsData.findIndex(item => item.roll.trim().toUpperCase() === d.roll.trim().toUpperCase());
    if (idx !== -1) {
      state.fetchedStudentsData[idx] = d;
    } else {
      state.fetchedStudentsData.push(d);
    }
    drawRowUI(d);
  }

  // ── Draw single row in table UI ────────────────
  function drawRowUI(d) {
    const tbody = document.getElementById('result-tbody');
    
    // Remove existing duplicate roll row if any
    const existingRows = Array.from(tbody.querySelectorAll('tr'));
    for (let r of existingRows) {
      const rollCell = r.querySelector('td.roll');
      if (rollCell && rollCell.textContent.trim().toUpperCase() === d.roll.trim().toUpperCase()) {
        r.remove();
      }
    }

    if (!state.emptyCleared) {
      tbody.innerHTML = '';
      state.emptyCleared = true;
    }
    
    const isPass = d.result.trim().toUpperCase() === 'PASS';
    const row = document.createElement('tr');
    row.className = 'student-row';
    row.id = `row-${d.roll}`;
    row.onclick = () => toggleRowDetails(d.roll, d);
    
    let baseHtml = `
      <td class="muted" style="color:var(--muted)">-</td>
      <td class="roll" style="font-weight:700;">${d.roll}</td>
      <td class="name">${d.name}</td>
    `;

    state.activeSubjects.forEach(sub => {
      let subjectGrade = "-";
      let subClean = sub.replace(/[- ]/g, "").toUpperCase();
      let subIsPractical = subClean.includes("[P]") || subClean.endsWith("P");
      
      let bestKey = null;

      for (let key in d.subjects) {
        let keyClean = key.replace(/[- ]/g, "").toUpperCase();
        let keyIsPractical = keyClean.includes("[P]") || keyClean.includes("(P)") || keyClean.endsWith("P");
        
        if (subIsPractical === keyIsPractical) {
          let subBase = subClean.replace(/[\(\[\{][PT][\)\]\}]/g, "");
          let keyBase = keyClean.replace(/[\(\[\{][PT][\)\]\}]/g, "");
          
          if (keyBase.includes(subBase) || subBase.includes(keyBase)) {
            bestKey = key;
            break;
          }
        }
      }

      if (bestKey) {
        subjectGrade = d.subjects[bestKey];
      }
      
      let gradeStyle = "";
      let upperGrade = subjectGrade.trim().toUpperCase();
      if (["F", "ABS", "ABSENT", "W"].some(g => upperGrade.includes(g))) {
         gradeStyle = "color: var(--fail); font-weight: 700;";
      } else if (["O", "A+", "A", "B+", "B", "C+", "C", "D", "P"].some(g => upperGrade.startsWith(g))) {
         gradeStyle = "color: var(--pass); font-weight: 700;";
      }
      
      baseHtml += `<td class="grade-td" style="${gradeStyle}">${subjectGrade}</td>`;
    });

    baseHtml += `
      <td class="sgpa">${d.sgpa}</td>
      <td class="cgpa">${d.cgpa}</td>
      <td><span class="badge ${isPass ? 'badge-pass':'badge-fail'}">${d.result}</span></td>
    `;

    row.innerHTML = baseHtml;
    tbody.prepend(row);   
    reindexTable();
  }

  // ── Re-index Table Rows Sequentially ───────────
  function reindexTable() {
    const tbody = document.getElementById('result-tbody');
    const rowsList = Array.from(tbody.querySelectorAll('tr'));
    state.rowCount = 0;
    rowsList.forEach((tr) => {
      const indexCell = tr.querySelector('td.muted');
      if (indexCell) {
        state.rowCount++;
        indexCell.textContent = state.rowCount;
      }
    });
  }

  // ── Add Skip/Not Found Row to Table ───────────
  function addNotFoundRow(suffix) {
    const tbody = document.getElementById('result-tbody');
    const suffixUpper = suffix.trim().toUpperCase();
    const fullRoll = (isUploadMode() || (state.sessionPrefix && suffixUpper.startsWith && suffixUpper.startsWith(state.sessionPrefix.toUpperCase())) || /^[0-9]{4}[A-Z]{2,4}[0-9]{2}(?:[0-9]{3,4}|3D[0-9]{2})$/.test(suffixUpper))
      ? suffix
      : (state.sessionPrefix ? (state.sessionPrefix + suffix) : suffix);

    // Remove existing duplicate roll row if any
    const existingRows = Array.from(tbody.querySelectorAll('tr'));
    for (let r of existingRows) {
      const rollCell = r.querySelector('td.roll');
      if (rollCell && rollCell.textContent.trim().toUpperCase() === fullRoll.trim().toUpperCase()) {
        r.remove();
      }
    }

    if (!state.emptyCleared) {
      tbody.innerHTML = '';
      state.emptyCleared = true;
    }
    const row = document.createElement('tr');
    row.style.background = "rgba(224, 48, 80, 0.02)";
    row.style.fontStyle = "italic";
    
    const colsCount = 6 + state.activeSubjects.length;
    row.innerHTML = `
      <td class="muted" style="color:var(--muted)">-</td>
      <td class="roll" style="color:var(--warn)">${fullRoll}</td>
      <td colspan="${colsCount - 2}" style="color:var(--muted); font-size: 0.75rem;">Roll number not active or matching on portal</td>
    `;
    tbody.prepend(row);
    reindexTable();
  }

  // ── START SESSION ─────────────────────────────
  async function startSession() {
    let program, branch, sem, year = "", customPrefix = "";

    if (isUploadMode()) {
      // ── Upload Mode: get values from upload section ──
      if (!state.rollList || state.rollList.length === 0) {
        alert('Please upload an Excel or CSV file with roll numbers first!');
        return;
      }
      branch = document.getElementById('upload-branch-select').value;
      sem    = document.getElementById('sem-upload').value;
      program = (branch === 'mca') ? 'MCA' : 'BTech';

      state.rollListIdx = 0;
      state.startRoll = 0;
      state.endRoll   = state.rollList.length - 1;
      state.currentRoll = 0;
    } else {
      // ── Manual Range Mode: existing logic ──
      program = document.getElementById('program').value;
      branch  = program === 'MCA' ? 'mca' : document.getElementById('branch').value;
      sem    = document.getElementById('sem').value;
      
      const manualBatchActive = document.getElementById('manual-batch-chk').checked;
      if (manualBatchActive) {
        const manualBatchVal = document.getElementById('manual-batch-val').value.trim();
        const manualPrefixVal = document.getElementById('manual-prefix-val').value.trim().toUpperCase();
        if (manualPrefixVal) {
          customPrefix = manualPrefixVal;
        } else if (manualBatchVal) {
          year = manualBatchVal;
        } else {
          customPrefix = updateManualPrefixPreview();
        }
      } else {
        year = document.getElementById('batch-year-select').value;
      }

      state.startRoll   = parseInt(document.getElementById('start-roll').value);
      state.endRoll     = parseInt(document.getElementById('end-roll').value);
      state.currentRoll = state.startRoll;

      if (state.startRoll > state.endRoll) {
        alert('Starting roll must be ≤ ending roll!'); return;
      }
    }

    // Rebuild table header — pick branch from upload or manual mode
    const effectiveBranch = isUploadMode()
      ? document.getElementById('upload-branch-select').value
      : (document.getElementById('program').value === 'MCA' ? 'mca' : document.getElementById('branch').value);
    const effectiveSem = isUploadMode()
      ? document.getElementById('sem-upload').value
      : document.getElementById('sem').value;

    // Manually set branch/sem for rebuildTableHeader (it reads from #branch/#sem)
    const branchEl = document.getElementById('branch');
    const semEl    = document.getElementById('sem');
    // Temporarily override for rebuild
    const prevBranch = branchEl ? branchEl.value : '';
    const prevSem    = semEl    ? semEl.value    : '';
    if (branchEl) branchEl.value = effectiveBranch;
    if (semEl)    semEl.value    = effectiveSem;
    rebuildTableHeader();
    // Restore (so manual mode is unaffected)
    if (branchEl) branchEl.value = prevBranch;
    if (semEl)    semEl.value    = prevSem;

    document.getElementById('result-tbody').innerHTML = `
      <tr id="empty-row">
        <td colspan="${6 + state.activeSubjects.length}">
          <div class="empty-state">
            <div class="icon">📋</div>
            Waiting for captchas to load and process results...
          </div>
        </td>
      </tr>
    `;
    state.emptyCleared = false;
    state.rowCount = 0;
    state.fetchedStudentsData = [];

    setBtnLoading('btn-start', 'start-spinner', 'btn-start-txt', true, 'Starting...');
    setStatus('Opening browser...', 'running');

    try {
      const waitMode = document.getElementById('wait-mode').value;
      const waitValue = parseFloat(document.getElementById('wait-value').value) || 12;
      const speedMode = document.getElementById('speed-mode').value;
      const submitDelay = parseFloat(document.getElementById('submit-delay').value) || 1.5;
      const resetDelay = parseFloat(document.getElementById('reset-delay').value) || 0.5;
      const payload = {
        program,
        branch,
        sem,
        year,
        custom_prefix: customPrefix,
        wait_mode: waitMode,
        wait_value: waitValue,
        speed_mode: speedMode,
        submit_delay: submitDelay,
        reset_delay: resetDelay
      };
      if (isUploadMode()) {
        payload.roll_list = state.rollList;
      }


      const res  = await fetch('/api/start', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text.substring(0, 100)}`);
      }
      const data = await res.json();

      if (data.ok) {
        state.sessionMode = isUploadMode() ? 'list' : 'range';
        state.running = true;
        state.sessionPrefix = data.prefix || "";
        updateStepsProgress();
        const modeLabel = isUploadMode()
          ? `${state.rollList.length} rolls from file`
          : `Range ${state.startRoll}–${state.endRoll}`;
        log(`Session started — Branch ${branch}, Sem ${sem} [${modeLabel}]`, 'ok');
        loadPreviousSheets();
        const firstDisplay = isUploadMode() ? state.rollList[0] : state.currentRoll;
        setStatus(`Browser open · Roll ${firstDisplay} loading...`, 'running');
        enableCaptchaSection(true);
        updateProgress();
        loadCaptcha();
      } else {
        log('Start failed: ' + data.error, 'err');
        setStatus('Error: ' + data.error, 'error');
      }
    } catch(e) {
      log('Connection error: ' + e.message, 'err');
      setStatus('Server error', 'error');
    }

    setBtnLoading('btn-start', 'start-spinner', 'btn-start-txt', false, '⚡ Restart Browser');

  }

  // ── LOAD CAPTCHA ──────────────────────────────
  async function loadCaptcha() {
    let roll, captchaUrl;

    if (isUploadMode()) {
      // List mode: use full roll number from uploaded sheet
      if (state.rollListIdx >= state.rollList.length) return; // Safety guard
      roll = state.rollList[state.rollListIdx];
      captchaUrl = `/api/captcha?roll=${encodeURIComponent(roll)}&full=1`;
    } else {
      // Manual range mode: existing logic
      const isDiploma = document.getElementById('diploma-chk').checked;
      roll = state.currentRoll.toString();
      if (isDiploma) {
        roll = "3D" + state.currentRoll.toString().padStart(2, '0');
      }
      captchaUrl = '/api/captcha?roll=' + roll;
    }

    document.getElementById('current-roll-lbl').textContent = roll;
    document.getElementById('captcha-input').value = '';

    const wrap = document.getElementById('captcha-wrap');
    wrap.innerHTML = `
      <div class="captcha-scanner-overlay active" id="captcha-scanner">
        <div class="scan-line"></div>
      </div>
      <div class="captcha-placeholder">Loading captcha...</div>
    `;

    const aiStatus = document.getElementById('ai-solver-status');
    if (aiStatus) {
      aiStatus.style.display = 'block';
      aiStatus.innerHTML = '🤖 Loading...';
    }

    try {
      const res  = await fetch(captchaUrl);
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text.substring(0, 100)}`);
      }
      const data = await res.json();

      if (data.ok) {
        wrap.innerHTML = `
          <div class="captcha-scanner-overlay" id="captcha-scanner">
            <div class="scan-line"></div>
          </div>
          <img src="${data.image}" alt="captcha"/>
        `;
        log(`Captcha loaded for roll ${roll}`, 'info');

        const errorBanner = document.getElementById('ocr-error-banner');
        if (data.ocr_error) {
          errorBanner.style.display = 'block';
          errorBanner.innerHTML = `
            <strong style="display:block;margin-bottom:4px;text-transform:uppercase;">⚠️ OCR Solver Disabled</strong>
            ${data.ocr_error_msg.replace(/\n/g, '<br>')}
          `;
          log(`OCR Solver deactivated: ${data.ocr_error_msg.split('\n')[0]}`, 'err');
          if (aiStatus) aiStatus.style.display = 'none';
        } else {
          errorBanner.style.display = 'none';
        }

        if (data.captcha_text) {
          document.getElementById('captcha-input').value = data.captcha_text;
          if (aiStatus) {
            aiStatus.innerHTML = `🤖 Auto-Solved: <span style="color:var(--accent); font-weight:800;">${data.captcha_text}</span>`;
          }
          if (data.solver_used === "deep_learning") {
            log(`🤖 AI Deep Learning predicted captcha: "${data.captcha_text}"`, 'ok');
          } else {
            log(`OCR predicted captcha: "${data.captcha_text}"`, 'info');
          }

          const autoSolve = document.getElementById('auto-solve-chk').checked;
          if (autoSolve) {
            // Small visual delay to let user see predicted captcha
            setTimeout(() => {
              submitCaptcha();
            }, 600);
            return;
          }
        } else {
          if (!data.ocr_error) {
            log(`OCR could not solve captcha. Please type manually or check server console logs.`, 'warn');
            if (aiStatus) aiStatus.innerHTML = '⌨️ Type Manually';
          }
        }

        document.getElementById('captcha-input').focus();
      } else {
        wrap.innerHTML = `
          <div class="captcha-scanner-overlay" id="captcha-scanner">
            <div class="scan-line"></div>
          </div>
          <div class="captcha-placeholder" style="color:#ff6b35">Failed — click ↺ to retry</div>
        `;
        log('Captcha load failed: ' + data.error, 'warn');
        if (aiStatus) aiStatus.style.display = 'none';
      }
    } catch(e) {
      wrap.innerHTML = `
        <div class="captcha-scanner-overlay" id="captcha-scanner">
          <div class="scan-line"></div>
        </div>
        <div class="captcha-placeholder" style="color:#ff6b35">Error — retry</div>
      `;
      log('Network error: ' + e.message, 'err');
      if (aiStatus) aiStatus.style.display = 'none';
    }
  }

  // ── Sleep Helper ──────────────────────────────
  function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

  // ── SUBMIT CAPTCHA ────────────────────────────
  async function submitCaptcha() {
    const captcha = document.getElementById('captcha-input').value.trim();
    if (!captcha) { document.getElementById('captcha-input').focus(); return; }

    setBtnLoading('btn-submit','submit-spinner','btn-submit-txt', true, 'Checking...');

    // Determine roll identifier based on mode
    let rollSuffix, isFullRoll = false;
    if (isUploadMode()) {
      rollSuffix = state.rollList[state.rollListIdx]; // Full roll number
      isFullRoll = true;
    } else {
      const isDiploma = document.getElementById('diploma-chk').checked;
      rollSuffix = state.currentRoll.toString();
      if (isDiploma) {
        rollSuffix = "3D" + state.currentRoll.toString().padStart(2, '0');
      }
    }

    try {
      const res  = await fetch('/api/submit', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ roll: rollSuffix, captcha, full_roll: isFullRoll })
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text.substring(0, 100)}`);
      }
      const data = await res.json();

      if (!data.ok) {
        log('Submit error: ' + data.error, 'err');
        setBtnLoading('btn-submit','submit-spinner','btn-submit-txt', false, 'Submit →');
        return;
      }

      if (data.status === 'success') {
        const d = data.data;
        const isPass = d.result.trim().toUpperCase() === 'PASS';
        
        // --- DYNAMIC FRONTEND COLUMN EXPANSION ---
        let newSubjectsDetected = [];
        for (let portalKey in d.subjects) {
          let portalClean = portalKey.replace(/[- ]/g, "").toUpperCase();
          let portalIsPractical = portalClean.includes("[P]") || portalClean.includes("(P)") || portalClean.endsWith("P");
          let pSubBase = portalClean.replace(/[\(\[\{][PT][\)\]\}]/g, "");
          
          let matched = false;
          state.activeSubjects.forEach(sub => {
            let subClean = sub.replace(/[- ]/g, "").toUpperCase();
            let subIsPractical = subClean.includes("[P]") || subClean.endsWith("P");
            let subBase = subClean.replace(/[\(\[\{][PT][\)\]\}]/g, "");
            
            if (portalIsPractical === subIsPractical) {
              if (pSubBase === subBase || subBase.includes(pSubBase) || pSubBase.includes(subBase)) {
                matched = true;
              }
            }
          });
          
          if (!matched && pSubBase && !["PASS", "FAIL", "TOTAL", "SGPA", "CGPA"].some(g => pSubBase.includes(g))) {
            let cleanNewSub = portalIsPractical ? pSubBase + "[P]" : pSubBase + "[T]";
            if (!newSubjectsDetected.includes(cleanNewSub) && !state.activeSubjects.includes(cleanNewSub)) {
              newSubjectsDetected.push(cleanNewSub);
            }
          }

        }
        
        if (newSubjectsDetected.length > 0) {
          const combined = state.activeSubjects.concat(newSubjectsDetected);
          const isPract = s => s.includes("[P]") || s.includes("(P)") || s.toUpperCase().endsWith("P");
          const theory = combined.filter(s => !isPract(s));
          const practical = combined.filter(isPract);
          state.activeSubjects = theory.concat(practical);
          rebuildTableHeader(true);
          
          // Clear and redraw all rows in history to align with new headers
          const tbody = document.getElementById('result-tbody');
          tbody.innerHTML = '';
          state.emptyCleared = true;
          
          // Add current student to history list before redrawing
          if (!state.fetchedStudentsData) {
            state.fetchedStudentsData = [];
          }
          const exists = state.fetchedStudentsData.some(item => item.roll.trim().toUpperCase() === d.roll.trim().toUpperCase());
          if (!exists) {
            state.fetchedStudentsData.push(d);
          }
          
          state.fetchedStudentsData.forEach(student => {
             drawRowUI(student);
          });
        } else {
          addRow(d);
        }

        state.totalFetched++;
        if (isPass) state.passCount++; else state.failCount++;
        updateStats();
        log(`✓ ${d.roll} · ${d.name} · SGPA ${d.sgpa} · ${d.result}`, 'ok');
        if (isUploadMode()) { state.rollListIdx++; } else { state.currentRoll++; }
        state.captchaRetries = 0; // RESET RETRY COUNT ON SUCCESS

      } else if (data.status === 'not_found') {
        if (isUploadMode()) {
          addNotFoundRow(rollSuffix);  // rollSuffix is already full roll in list mode
        } else {
          addNotFoundRow(rollSuffix);
        }
        state.skipCount++;
        state.totalFetched++;
        updateStats();
        log(`⚠ Roll ${rollSuffix} not found — skipped`, 'warn');
        if (isUploadMode()) { state.rollListIdx++; } else { state.currentRoll++; }
        state.captchaRetries = 0; // RESET RETRY COUNT ON NOT FOUND

      } else if (data.status === 'browser_recovered') {
        log(`🛡️ Browser session recovered automatically — retrying captcha...`, 'info');
        setBtnLoading('btn-submit','submit-spinner','btn-submit-txt', false, 'Submit →');
        await loadCaptcha();
        return; // Terminates safely to prevent stream collisions
      } else if (data.status === 'wrong_captcha') {
        state.captchaRetries++;
        if (state.captchaRetries >= 10) {
          log(`✗ Too many captcha retries (${state.captchaRetries}) for roll ${rollSuffix}. Disabling Auto-Solve.`, 'err');
          document.getElementById('auto-solve-chk').checked = false;
          state.captchaRetries = 0;
        }
        log(`✗ Verification notice: ${data.message || 'Wrong captcha'} — retry (Attempt ${state.captchaRetries}/10)`, 'err');
        setBtnLoading('btn-submit','submit-spinner','btn-submit-txt', false, 'Submit →');
        await loadCaptcha();
        return; // Terminates safely to prevent stream collisions
      }

      // Check if done
      const isDone = isUploadMode()
        ? state.rollListIdx >= state.rollList.length
        : state.currentRoll > state.endRoll;

      if (isDone) {
        setStatus('All done! ✓', 'done');
        log('🎉 All roll numbers processed!', 'ok');
        enableCaptchaSection(false);
        state.running = false;
        updateStepsProgress();
        document.getElementById('btn-dl').style.opacity = '1';
        document.getElementById('btn-dl').style.pointerEvents = 'auto';
        document.getElementById('btn-pdf').style.opacity = '1';
        document.getElementById('btn-pdf').style.pointerEvents = 'auto';
        loadPreviousSheets();
      } else {
        updateProgress();
        const nextRoll = isUploadMode()
          ? (state.rollList[state.rollListIdx] || '')
          : state.currentRoll;
        const totalCount = isUploadMode() ? state.rollList.length : state.endRoll;
        const speedInterRollDelays = {
          slow: 2000,
          normal: 1000,
          fast: 500,
          turbo: 100
        };
        const currentInterRollDelay = speedInterRollDelays[state.speedMode || 'normal'] || 1000;
        const delayInSec = (currentInterRollDelay / 1000).toFixed(1);
        setStatus(`Running · Roll ${nextRoll} of ${totalCount} · Waiting ${delayInSec}s...`, 'running');
        await sleep(currentInterRollDelay);
        setStatus(`Running · Roll ${nextRoll} of ${totalCount}`, 'running');
        await loadCaptcha();
      }

    } catch(e) {
      log('Error parsing response stream: ' + e.message, 'err');
    }

    setBtnLoading('btn-submit','submit-spinner','btn-submit-txt', false, 'Submit →');
  }

  // ── DOWNLOAD CSV ──────────────────────────────
  function downloadCSV() {
    window.location.href = '/api/download';
    log('CSV downloaded', 'ok');
  }

  // ── Helpers ───────────────────────────────────
  function setBtnLoading(btnId, spinnerId, txtId, loading, txt) {
    document.getElementById(btnId).disabled = loading;
    document.getElementById(spinnerId).style.display = loading ? 'block' : 'none';
    document.getElementById(txtId).textContent = txt;
    document.getElementById(btnId).classList.toggle('loading', loading);
  }

  function enableCaptchaSection(on) {
    const s = document.getElementById('captcha-section');
    s.style.opacity       = on ? '1'    : '.4';
    s.style.pointerEvents = on ? 'auto' : 'none';
    if (on) {
      document.getElementById('btn-dl').style.opacity = '1';
      document.getElementById('btn-dl').style.pointerEvents = 'auto';
      document.getElementById('btn-pdf').style.opacity = '1';
      document.getElementById('btn-pdf').style.pointerEvents = 'auto';
    }
  }

  // ── Load Previous Sheets ──────────────────────
  async function loadPreviousSheets() {
    const listContainer = document.getElementById('previous-sheets-list');
    try {
      const res = await fetch('/api/previous_files');
      if (!res.ok) throw new Error("Failed to fetch previous files list");
      const data = await res.json();
      
      if (data.ok) {
        if (!data.files || data.files.length === 0) {
          listContainer.innerHTML = '<div style="color: var(--muted); text-align: center; padding: 10px 0;">No previous sheets found.</div>';
          return;
        }
        
        let html = '';
        data.files.forEach(file => {
          let folderBadgeColor = "var(--muted)";
          if (file.folder === "CS_Core") folderBadgeColor = "var(--accent2)";
          else if (file.folder === "IT") folderBadgeColor = "var(--accent)";
          else if (file.folder === "CS_Emerging") folderBadgeColor = "var(--warn)";

          html += `
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: rgba(15, 23, 42, 0.02); border: 1px solid var(--border); border-radius: 8px; transition: background 0.2s;">
              <div style="display: flex; flex-direction: column; gap: 2px; max-width: 65%;">
                <span style="font-weight: 700; color: var(--text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.7rem;" title="${file.name}">${file.name}</span>
                <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                  <span style="font-size: 0.62rem; color: var(--muted);">${file.size} · ${file.mtime}</span>
                  <span style="font-size: 0.58rem; padding: 1px 6px; border-radius: 4px; color: #fff; background: ${folderBadgeColor}; font-weight: 700; font-family: var(--mono);">${file.folder}</span>
                </div>
              </div>
              <div style="display: flex; gap: 6px;">
                <button onclick="window.location.href='/api/download_file/${file.name}?folder=${file.folder}'" 
                        style="background: transparent; border: 1px solid var(--border); border-radius: 6px; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; color: var(--accent); cursor: pointer; transition: all 0.2s; font-size: 0.8rem;" 
                        title="Download CSV"
                        onmouseover="this.style.background='rgba(16, 185, 129, 0.08)'; this.style.borderColor='var(--accent)'"
                        onmouseout="this.style.background='transparent'; this.style.borderColor='var(--border)'">
                  ↓
                </button>
                <button onclick="convertCSVToPDF('${file.name}', '${file.folder}')" 
                        style="background: transparent; border: 1px solid var(--border); border-radius: 6px; width: 36px; height: 26px; display: flex; align-items: center; justify-content: center; color: var(--accent2); cursor: pointer; transition: all 0.2s; font-size: 0.6rem; font-weight: 700; font-family: var(--mono);" 
                        title="Convert to PDF"
                        onmouseover="this.style.background='rgba(14, 165, 233, 0.08)'; this.style.borderColor='var(--accent2)'"
                        onmouseout="this.style.background='transparent'; this.style.borderColor='var(--border)'">
                  PDF
                </button>
              </div>
            </div>
          `;
        });
        listContainer.innerHTML = html;
      } else {
        listContainer.innerHTML = `<div style="color: var(--fail); text-align: center; padding: 10px 0;">Error: ${data.error}</div>`;
      }
    } catch (err) {
      listContainer.innerHTML = `<div style="color: var(--fail); text-align: center; padding: 10px 0;">Connection failed</div>`;
    }
  }

  // ── GENERATE AND DOWNLOAD PDF REPORT ──────────
  async function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4'); // Landscape A4 is mathematically necessary for 10+ columns
    
    // Header Style
    doc.setFont("Helvetica", "bold");
    doc.setFontSize(16);
    doc.setTextColor(15, 23, 42); // Deep Slate Charcoal
    doc.text("RGPV Result Scraper - Session Report", 10, 12);
    
    // Metadata block
    doc.setFont("Helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(100, 116, 139); // Tech Cool Gray
    
    const isUpload = isUploadMode();
    const branchSelect = isUpload ? document.getElementById("upload-branch-select") : document.getElementById("branch");
    const branchText = branchSelect ? branchSelect.options[branchSelect.selectedIndex].text : "Custom Branch";
    const semSelect = isUpload ? document.getElementById("sem-upload") : document.getElementById("sem");
    const semText = semSelect ? semSelect.options[semSelect.selectedIndex].text : "Custom Sem";
    const dateText = new Date().toLocaleString('en-US', { hour12: true });

    
    doc.text(`Branch: ${branchText}  |  Semester: ${semText}  |  Generated on: ${dateText}`, 10, 17);
    
    // Extract dynamic headers from DOM
    const headerCells = Array.from(document.querySelectorAll("#table-header-row th")).map(th => th.textContent.trim());
    
    // Extract dynamic rows from DOM
    const rowElements = Array.from(document.querySelectorAll("#result-tbody tr"));
    const bodyRows = [];
    const seenRolls = new Set();
    
    rowElements.forEach(tr => {
      if (tr.querySelector("td.roll")) {
        // Active student data row
        const rowCells = Array.from(tr.querySelectorAll("td")).map(td => {
           const badge = td.querySelector(".badge");
           return badge ? badge.textContent.trim() : td.textContent.trim();
        });
        
        if (rowCells.length > 1) {
          const roll = rowCells[1].trim().toUpperCase();
          if (!seenRolls.has(roll)) {
            seenRolls.add(roll);
            bodyRows.push(rowCells);
          }
        }
      } else {
        // Skipped / Not found row
        const rollElement = tr.querySelector("td.roll");
        const roll = rollElement ? rollElement.textContent.trim() : "";
        if (roll) {
          const rollUpper = roll.toUpperCase();
          if (!seenRolls.has(rollUpper)) {
            seenRolls.add(rollUpper);
            const descCell = tr.cells[2];
            const desc = descCell ? descCell.textContent.trim() : "Roll number not active on portal";
            
            const emptyRow = [bodyRows.length + 1, roll, desc];
            while (emptyRow.length < headerCells.length) {
              emptyRow.push("-");
            }
            bodyRows.push(emptyRow);
          }
        }
      }
    });

    // Re-index row numbering sequentially from 1 to N
    bodyRows.forEach((row, idx) => {
      row[0] = idx + 1;
    });

    // Auto-scale fonts and paddings based on total columns
    const totalCols = headerCells.length;
    let fontSize = 7.0;
    let headFontSize = 7.4;
    let cellPadding = 1.2;
    let subWidth = 12;
    let sgpaWidth = 13;
    let resultWidth = 16;
    
    if (totalCols > 12) {
      fontSize = 6.0;
      headFontSize = 6.5;
      cellPadding = 0.8;
      subWidth = 9.5;
      sgpaWidth = 11;
      resultWidth = 13;
    } else if (totalCols > 8) {
      fontSize = 6.6;
      headFontSize = 7.0;
      cellPadding = 1.0;
      subWidth = 11;
      sgpaWidth = 12;
      resultWidth = 15;
    }

    const columnStyles = {
      0: { cellWidth: 7 }, // Compact Index
      1: { cellWidth: 22, fontStyle: 'bold' }, // Compact Roll Number
      2: { halign: 'left' } // Student Name (let it auto-fit the remaining space)
    };
    
    if (totalCols > 3) {
      columnStyles[totalCols - 3] = { cellWidth: sgpaWidth }; // SGPA
      columnStyles[totalCols - 2] = { cellWidth: sgpaWidth }; // CGPA
      columnStyles[totalCols - 1] = { cellWidth: resultWidth }; // Result
      
      for (let i = 3; i < totalCols - 3; i++) {
        columnStyles[i] = { cellWidth: subWidth }; // Subjects
      }
    }
    
    // Draw professional AutoTable
    doc.autoTable({
      head: [headerCells],
      body: bodyRows,
      startY: 21,
      theme: 'grid',
      styles: {
        font: 'helvetica',
        fontSize: fontSize,
        cellPadding: cellPadding,
        halign: 'center',
        valign: 'middle',
        overflow: 'linebreak'
      },
      headStyles: {
        fillColor: [15, 23, 42], // obsidian deep slate
        textColor: [255, 255, 255],
        fontStyle: 'bold',
        fontSize: headFontSize
      },
      bodyStyles: {
        textColor: [51, 65, 85]
      },
      columnStyles: columnStyles,
      margin: { top: 21, left: 10, right: 10, bottom: 15 },
      didParseCell: function (cellData) {
        // 1. Color code Result column (last column)
        if (cellData.column.index === totalCols - 1) {
          const val = String(cellData.cell.raw).trim().toUpperCase();
          if (val === 'PASS') {
            cellData.cell.styles.textColor = [16, 185, 129]; // Emerald Green
            cellData.cell.styles.fontStyle = 'bold';
          } else if (val.includes('FAIL') || val.includes('BACKLOG')) {
            cellData.cell.styles.textColor = [239, 68, 68]; // Vibrant Red
            cellData.cell.styles.fontStyle = 'bold';
          }
        }
        
        // 2. Highlight skipped / inactive student rows
        const isSkippedRow = cellData.row.raw[2] && String(cellData.row.raw[2]).includes("active or matching");
        if (isSkippedRow) {
          cellData.cell.styles.fillColor = [254, 243, 243]; // Light pastel red background
          cellData.cell.styles.textColor = [100, 116, 139]; // Muted gray text
          if (cellData.column.index === 1) {
            cellData.cell.styles.textColor = [245, 158, 11]; // Keep roll number warning color
            cellData.cell.styles.fontStyle = 'bold';
          }
        }
      },
      didDrawPage: function (data) {

        // Footer (Page numbers only, no brand signatures)
        const str = "Page " + doc.internal.getNumberOfPages();
        doc.setFontSize(8);
        doc.setTextColor(148, 163, 184);
        doc.text(str, doc.internal.pageSize.width - data.settings.margin.right, doc.internal.pageSize.height - 10, { align: 'right' });
      }
    });
    
    // Format filename matching CSV naming conventions
    let cleanBranch = "Report";
    if (branchText.includes("·")) {
      cleanBranch = branchText.split("·")[1].trim().replace(/\s+/g, "_");
    } else {
      cleanBranch = branchText.trim().replace(/\s+/g, "_");
    }
    const semValue = isUpload ? document.getElementById("sem-upload").value : document.getElementById("sem").value;
    const filename = `${cleanBranch}_sem${semValue}_report.pdf`;
    
    doc.save(filename);
    log(`PDF downloaded successfully: ${filename}`, 'ok');
  }

  // ── CONVERT PREVIOUS CSV TO PDF REPORT ──────────
  async function convertCSVToPDF(filename, folder='') {
    log(`Converting ${filename} to professional PDF...`, 'info');
    try {
      const res = await fetch(`/api/get_csv_data/${filename}?folder=${folder}`);
      if (!res.ok) throw new Error("Failed to parse CSV file");
      const data = await res.json();
      
      if (data.ok) {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF('l', 'mm', 'a4'); // Landscape A4 is mathematically necessary for 10+ columns
        
        // Header Style
        doc.setFont("Helvetica", "bold");
        doc.setFontSize(16);
        doc.setTextColor(15, 23, 42); // Deep Slate Charcoal
        doc.text("RGPV Result Scraper - Saved Report", 10, 12);
        
        // Metadata block
        doc.setFont("Helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(100, 116, 139); // Slate Gray
        
        // Parse metadata (Branch/Semester) from filename if possible
        let parsedMeta = "";
        try {
          const parts = filename.replace("_results.csv", "").split("_sem");
          if (parts.length === 2) {
             const cleanBranchName = parts[0].replace("_", " ");
             parsedMeta = `  |  Branch: ${cleanBranchName}  |  Semester: ${parts[1]}`;
          }
        } catch (e) {}
        
        const dateText = new Date().toLocaleString('en-US', { hour12: true });
        doc.text(`Source File: ${filename}${parsedMeta}  |  Converted on: ${dateText}`, 10, 17);
        
        const headerCells = data.headers;
        const rawRows = data.rows;
        
        // Deduplicate rows by Roll Number (index 0 in CSV row)
        const bodyRows = [];
        const seenRolls = new Set();
        
        // Determine Roll Number column index (usually 0 in generated CSV files)
        let csvRollIdx = 0;
        if (headerCells && headerCells.length > 1) {
          const idx = headerCells.findIndex(h => h.trim().toUpperCase() === "ROLL NUMBER");
          if (idx !== -1) csvRollIdx = idx;
        }
        
        rawRows.forEach(row => {
          if (row && row.length > csvRollIdx) {
            const roll = row[csvRollIdx].trim().toUpperCase();
            if (!seenRolls.has(roll)) {
              seenRolls.add(roll);
              // Insert dynamic sequential index placeholder at the beginning
              bodyRows.push(["-", ...row]);
            }
          }
        });
        
        // Insert a new sequential '#' header cell if not present
        let finalHeaders = [...headerCells];
        if (finalHeaders[0].trim() !== "#") {
          finalHeaders = ["#", ...finalHeaders];
        } else {
          // If first column in CSV is already # index, we don't prepend extra column
          // We just use raw data but re-index it
          bodyRows.length = 0; // reset
          seenRolls.clear();
          rawRows.forEach(row => {
            if (row && row.length > 1) {
              const roll = row[1].trim().toUpperCase();
              if (!seenRolls.has(roll)) {
                seenRolls.add(roll);
                bodyRows.push([...row]);
              }
            }
          });
        }
        
        // Re-index sequential numbering from 1 to N
        bodyRows.forEach((row, idx) => {
          row[0] = idx + 1;
        });
        
        // Auto-scale fonts and paddings based on total columns
        const totalCols = finalHeaders.length;
        let fontSize = 7.0;
        let headFontSize = 7.4;
        let cellPadding = 1.2;
        let subWidth = 12;
        let sgpaWidth = 13;
        let resultWidth = 16;
        
        if (totalCols > 12) {
          fontSize = 6.0;
          headFontSize = 6.5;
          cellPadding = 0.8;
          subWidth = 9.5;
          sgpaWidth = 11;
          resultWidth = 13;
        } else if (totalCols > 8) {
          fontSize = 6.6;
          headFontSize = 7.0;
          cellPadding = 1.0;
          subWidth = 11;
          sgpaWidth = 12;
          resultWidth = 15;
        }

        const columnStyles = {
          0: { cellWidth: 7 }, // Compact Index
          1: { cellWidth: 22, fontStyle: 'bold' }, // Compact Roll Number
          2: { halign: 'left' } // Student Name (let it auto-fit the remaining space)
        };
        
        if (totalCols > 3) {
          columnStyles[totalCols - 3] = { cellWidth: sgpaWidth }; // SGPA
          columnStyles[totalCols - 2] = { cellWidth: sgpaWidth }; // CGPA
          columnStyles[totalCols - 1] = { cellWidth: resultWidth }; // Result
          
          for (let i = 3; i < totalCols - 3; i++) {
            columnStyles[i] = { cellWidth: subWidth }; // Subjects
          }
        }
        
        // Draw professional AutoTable
        doc.autoTable({
          head: [finalHeaders],
          body: bodyRows,
          startY: 21,
          theme: 'grid',
          styles: {
            font: 'helvetica',
            fontSize: fontSize,
            cellPadding: cellPadding,
            halign: 'center',
            valign: 'middle',
            overflow: 'linebreak'
          },
          headStyles: {
            fillColor: [15, 23, 42], // obsidian deep slate
            textColor: [255, 255, 255],
            fontStyle: 'bold',
            fontSize: headFontSize
          },
          bodyStyles: {
            textColor: [51, 65, 85]
          },
          columnStyles: columnStyles,
          margin: { top: 21, left: 10, right: 10, bottom: 15 },
          didParseCell: function (cellData) {
            // 1. Color code Result column (last column)
            if (cellData.column.index === totalCols - 1) {
              const val = String(cellData.cell.raw).trim().toUpperCase();
              if (val === 'PASS') {
                cellData.cell.styles.textColor = [16, 185, 129]; // Emerald Green
                cellData.cell.styles.fontStyle = 'bold';
              } else if (val.includes('FAIL') || val.includes('BACKLOG')) {
                cellData.cell.styles.textColor = [239, 68, 68]; // Vibrant Red
                cellData.cell.styles.fontStyle = 'bold';
              }
            }
            
            // 2. Highlight skipped / inactive student rows
            const isSkippedRow = cellData.row.raw[2] && String(cellData.row.raw[2]).includes("active or matching");
            if (isSkippedRow) {
              cellData.cell.styles.fillColor = [254, 243, 243]; // Light pastel red background
              cellData.cell.styles.textColor = [100, 116, 139]; // Muted gray text
              if (cellData.column.index === 1) {
                cellData.cell.styles.textColor = [245, 158, 11]; // Keep roll number warning color
                cellData.cell.styles.fontStyle = 'bold';
              }
            }
          },
          didDrawPage: function (data) {
            // Footer (Page numbers only, no brand signatures)
            const str = "Page " + doc.internal.getNumberOfPages();
            doc.setFontSize(8);
            doc.setTextColor(148, 163, 184);
            doc.text(str, doc.internal.pageSize.width - data.settings.margin.right, doc.internal.pageSize.height - 10, { align: 'right' });
          }
        });
        
        // Save PDF with _converted suffix
        const pdfFilename = filename.replace(".csv", "_converted.pdf");
        doc.save(pdfFilename);
        log(`PDF successfully generated: ${pdfFilename}`, 'ok');
      } else {
        log(`Conversion failed: ${data.error}`, 'err');
      }
    } catch (err) {
      log(`Conversion connection failed: ${err.message}`, 'err');
    }
  }

  // ── LIVE TABLE FILTERING & SEARCH ──────────
  let currentResultFilter = 'all';

  function filterTable() {
    const query = document.getElementById('table-search').value.toLowerCase().trim();
    const tbody = document.getElementById('result-tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.forEach(tr => {
      // Skip empty row or log box nested items
      if (tr.id === 'empty-row') return;

      const rollCell = tr.querySelector('td.roll');
      const nameCell = tr.querySelector('td.name');
      const badgeCell = tr.querySelector('.badge');

      if (!rollCell || !nameCell) return;

      const roll = rollCell.textContent.toLowerCase();
      const name = nameCell.textContent.toLowerCase();
      const result = badgeCell ? badgeCell.textContent.toLowerCase() : '';

      const matchesSearch = roll.includes(query) || name.includes(query);
      
      let matchesFilter = true;
      if (currentResultFilter === 'pass') {
        matchesFilter = result === 'pass';
      } else if (currentResultFilter === 'fail') {
        matchesFilter = result.includes('fail') || result.includes('backlog');
      }

      if (matchesSearch && matchesFilter) {
        tr.style.display = '';
      } else {
        tr.style.display = 'none';
      }
    });
  }

  function setResultFilter(type, btn) {
    currentResultFilter = type;
    
    // Update active pill button state
    const pills = document.querySelectorAll('.filter-pill');
    pills.forEach(p => p.classList.remove('active'));
    btn.classList.add('active');

    filterTable();
  }

  // Load previous sheets automatically on page start
  document.addEventListener('DOMContentLoaded', () => {
    loadPreviousSheets();
    
    // Initialize Theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const isLight = savedTheme === 'light';
    if (isLight) {
      document.documentElement.classList.add('light-theme');
    } else {
      document.documentElement.classList.remove('light-theme');
    }
    updateThemeToggleIcon(isLight);

    // Initial wizard setup
    updateStepsProgress();

    // Add real-time updates for prefix preview
    document.getElementById('program').addEventListener('change', updateManualPrefixPreview);
    document.getElementById('branch').addEventListener('change', updateManualPrefixPreview);
    document.getElementById('sem').addEventListener('change', updateManualPrefixPreview);
    
    // Initial preview setup
    updateManualPrefixPreview();
  });
