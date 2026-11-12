// Player Video 9:16 per "Il Terzo Avvistamento"
// Rendering grafico su Canvas 1080x1920 con animazioni Ken Burns, kinetic captions,
// movimenti organici delle scene (onde del mare, nebbia alla stazione, lampione sfarfallante)
// e Web Audio Sound Design con voce maschile thriller sincronizzata ai cambi scena.

const TOTAL_DURATION = 72; // secondi

// Definizione delle 6 scene sincronizzate (con nuova scena Napoli Mare a Castel dell'Ovo)
const SCENES = [
  {
    id: 1,
    name: "Il Gancio",
    start: 0,
    end: 6.5,
    src: "assets/01_gancio_occhio.jpg",
    zoomStart: 1.35,
    zoomEnd: 1.06,
    panX: 0,
    panY: 0,
    ambientColor: "rgba(0, 180, 255, 0.18)",
    effect: "eye"
  },
  {
    id: 2,
    name: "Milano - Stazione Centrale",
    start: 6.5,
    end: 19.8,
    src: "assets/02_milano_stazione.jpg",
    zoomStart: 1.0,
    zoomEnd: 1.25,
    panX: 0,
    panY: -0.05,
    ambientColor: "rgba(100, 140, 160, 0.15)",
    effect: "station"
  },
  {
    id: 3,
    name: "Roma - Vicolo Notturno",
    start: 19.8,
    end: 37.4,
    src: "assets/03_roma_vicolo.jpg",
    zoomStart: 1.04,
    zoomEnd: 1.28,
    panX: 0,
    panY: -0.07,
    ambientColor: "rgba(255, 170, 0, 0.16)",
    effect: "rome"
  },
  {
    id: 4,
    name: "Napoli - Castel dell'Ovo (Il Mare)",
    start: 37.4,
    end: 50.7,
    src: "assets/04_napoli_mare_castel.jpg",
    zoomStart: 1.03,
    zoomEnd: 1.22,
    panX: 0,
    panY: 0.04,
    ambientColor: "rgba(0, 160, 220, 0.16)",
    effect: "sea"
  },
  {
    id: 5,
    name: "Napoli - La Panchina & Il Telefono",
    start: 50.7,
    end: 62.8,
    src: "assets/05_napoli_panchina_telefono.jpg",
    zoomStart: 1.0,
    zoomEnd: 1.20,
    panX: 0,
    panY: 0.08,
    desaturate: true,
    ambientColor: "rgba(0, 150, 200, 0.12)",
    effect: "bench"
  },
  {
    id: 6,
    name: "Il Climax - Il Riflesso",
    start: 62.8,
    end: 72.0,
    src: "assets/06_climax_riflesso.jpg",
    zoomStart: 1.05,
    zoomEnd: 1.35,
    panX: -0.05,
    panY: 0.05,
    ambientColor: "rgba(255, 30, 80, 0.22)",
    effect: "climax"
  }
];

// Sottotitoli sincronizzati con la voce Giuseppe Cupo Thriller & Lento
const CAPTIONS = [
  // SCENA 1: L'Occhio (0.0s - 6.5s)
  {
    start: 0.2,
    end: 3.5,
    text: "Le probabilità di incontrare\nlo stesso sconosciuto...",
    highlight: "stesso sconosciuto",
    color: "#ffffff"
  },
  {
    start: 3.6,
    end: 6.4,
    text: "in tre città diverse...\nsono zero.",
    highlight: "sono zero",
    color: "#ffe600"
  },

  // SCENA 2: Milano - Stazione Centrale (6.5s - 19.8s)
  {
    start: 6.5,
    end: 10.2,
    text: "La prima volta: Milano.\nNebbia fitta.",
    highlight: "Milano 📍",
    color: "#00e5ff"
  },
  {
    start: 10.3,
    end: 15.7,
    text: "Nella calca, un ragazzo mi urta.\nOcchi vitrei, cappotto nero.",
    highlight: "cappotto nero",
    color: "#ffe600"
  },
  {
    start: 15.8,
    end: 19.8,
    text: "Non chiede scusa.\nScompare nel nulla tra la folla.",
    highlight: "Scompare nel nulla",
    color: "#ffffff"
  },

  // SCENA 3: Roma - Vicolo Notturno (19.8s - 37.4s)
  {
    start: 19.9,
    end: 24.7,
    text: "Due anni dopo. Roma,\nvicoli deserti alle tre di notte.",
    highlight: "Roma 📍",
    color: "#00e5ff"
  },
  {
    start: 24.8,
    end: 29.0,
    text: "Sento dei passi.\nAccelero... l'ombra accelera.",
    highlight: "l'ombra accelera",
    color: "#ffe600"
  },
  {
    start: 29.1,
    end: 33.9,
    text: "Sotto un lampione: era lui.\nNon era invecchiato di un giorno.",
    highlight: "era lui",
    color: "#ffe600"
  },
  {
    start: 34.0,
    end: 37.3,
    text: "Ha sorriso e mi ha sussurrato:\nla data di oggi.",
    highlight: "la data di oggi",
    color: "#ff3366"
  },

  // SCENA 4: Napoli - Castel dell'Ovo & Il Mare (37.4s - 50.7s)
  {
    start: 37.4,
    end: 42.6,
    text: "Oggi. Napoli, Castel dell'Ovo.\nDavanti al mare.",
    highlight: "Napoli 📍",
    color: "#00e5ff"
  },
  {
    start: 42.7,
    end: 46.9,
    text: "Pensavo di essere al sicuro...\npoi, quel gelo sulla nuca.",
    highlight: "quel gelo",
    color: "#ffe600"
  },
  {
    start: 47.0,
    end: 50.6,
    text: "E un silenzio anomalo:\nil mare si spegne di colpo.",
    highlight: "si spegne di colpo",
    color: "#00e5ff"
  },

  // SCENA 5: La Panchina & Il Telefono (50.7s - 62.8s)
  {
    start: 50.7,
    end: 55.3,
    text: "Sulla panchina c'è un telefono.\nAccanto, quel cappotto.",
    highlight: "telefono",
    color: "#ffe600"
  },
  {
    start: 55.4,
    end: 58.3,
    text: "Chiamata in arrivo da:\nMIO STESSO NUMERO.",
    highlight: "MIO STESSO NUMERO",
    color: "#ff3366"
  },
  {
    start: 58.4,
    end: 62.7,
    text: "Una mano gelida sulla spalla.\nHo trattenuto il respiro.",
    highlight: "mano gelida",
    color: "#ff3366"
  },

  // SCENA 6: Il Climax & Riflesso (62.8s - 72.0s)
  {
    start: 62.8,
    end: 64.6,
    text: "'Te l'avevo detto che era oggi.'",
    highlight: "era oggi",
    color: "#ffe600"
  },
  {
    start: 64.7,
    end: 67.4,
    text: "Nel riflesso nero ho visto la mia faccia...",
    highlight: "la mia faccia",
    color: "#ffffff"
  },
  {
    start: 67.5,
    end: 70.5,
    text: "Ma i miei occhi...\nerano diventati i suoi.",
    highlight: "diventati i suoi",
    color: "#ff3366"
  }
];

// Inizializzazione elementi DOM
const canvas = document.getElementById("videoCanvas");
const ctx = canvas.getContext("2d");
const playBtn = document.getElementById("playBtn");
const bigPlayBtn = document.getElementById("bigPlayBtn");
const playOverlay = document.getElementById("playOverlay");
const restartBtn = document.getElementById("restartBtn");
const progressBar = document.getElementById("progressBar");
const progressBarContainer = document.getElementById("progressBarContainer");
const timeDisplay = document.getElementById("timeDisplay");
const ambientGlow = document.getElementById("ambientGlow");
const playIcon = document.getElementById("playIcon");
const pauseIcon = document.getElementById("pauseIcon");
const voiceToggle = document.getElementById("voiceToggle");
const sfxToggle = document.getElementById("sfxToggle");
const captionsToggle = document.getElementById("captionsToggle");
const fullscreenBtn = document.getElementById("fullscreenBtn");
const exportBtn = document.getElementById("exportBtn");
const recordingBadge = document.getElementById("recordingBadge");
const recProgress = document.getElementById("recProgress");
const voiceSelect = document.getElementById("voiceSelect");
const testVoiceBtn = document.getElementById("testVoiceBtn");
const motionFxToggle = document.getElementById("motionFxToggle");
const soundtrackAudio = document.getElementById("soundtrackAudio");

let isPlaying = false;
let currentTime = 0;
let lastTimestamp = 0;
let animationFrameId = null;
let voiceEnabled = true;
let sfxEnabled = false; // Disabilitata musica e SFX: Solo Voce del Protagonista
let captionsEnabled = true;
let motionFxEnabled = true;

// Precaricamento delle immagini
const loadedImages = {};
let imagesLoadedCount = 0;

SCENES.forEach(scene => {
  const img = new Image();
  img.src = scene.src;
  img.onload = () => {
    imagesLoadedCount++;
    if (scene.id === 1 || imagesLoadedCount === SCENES.length) {
      renderFrame(currentTime);
    }
  };
  loadedImages[scene.id] = img;
});

// Particelle procedurali persistenti (nebbia stazione, spruzzi mare, pioggia Roma)
const fogParticles = Array.from({ length: 28 }, () => ({
  x: Math.random() * 1080,
  y: 600 + Math.random() * 1100,
  speed: 0.8 + Math.random() * 1.5,
  size: 140 + Math.random() * 220,
  alpha: 0.04 + Math.random() * 0.06
}));

const seaMistParticles = Array.from({ length: 35 }, () => ({
  x: 200 + Math.random() * 800,
  y: 900 + Math.random() * 950,
  speedY: -1.2 - Math.random() * 2.0,
  speedX: (Math.random() - 0.5) * 1.0,
  size: 30 + Math.random() * 80,
  alpha: 0.05 + Math.random() * 0.12
}));

const rainParticles = Array.from({ length: 60 }, () => ({
  x: Math.random() * 1080,
  y: Math.random() * 1920,
  speedY: 18 + Math.random() * 14,
  speedX: -2 - Math.random() * 2,
  len: 15 + Math.random() * 25,
  alpha: 0.15 + Math.random() * 0.25
}));

// ==========================================
// Web Audio API Sound Design Engine
// ==========================================
let audioCtx = null;
let audioDest = null; // Per registrazione MediaRecorder con audio

function initAudioContext() {
  if (!audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();
    audioDest = audioCtx.createMediaStreamDestination();
  }
  if (audioCtx.state === "suspended") {
    audioCtx.resume();
  }
}

function connectNode(node) {
  return;
}

// Generatori SFX Disabilitati: modalità Solo Voce Narrante
function playSubBassBoom() {}
function playTinnitusEffect(duration = 6) {}
function playStationAtmosphere() {}
function playFootstepsWhoosh() {}
function playTenseRiser() {}
function startSeaWaves() {}
function stopSeaWavesAbrupt() {}
function playPhoneRing() {}
function playHeartbeat() {}
function playClimaxHit() {}

const SFX_TRIGGERS = [];

function resetSfxTriggers() {}

function checkSfxTriggers(t) {}

// ==========================================
// ==========================================
// Gestione Voce Narrante (Traccia Master Audio HD)
// ==========================================
let currentCaptionIndex = -1;

function populateVoiceSelect() {
  voiceSelect.innerHTML = `
    <option value="giuseppe_cupo_profondo_lento" selected>🌑 Giuseppe - Cupo Thriller, Molto Profondo & Lento (⭐ Master Attivo)</option>
    <option value="giuseppe_riflessivo_caldo">🧔 Giuseppe - Adulto, Riflessivo & Caldo</option>
    <option value="giuseppe_baritono_equilibrato">🎙️ Giuseppe - Baritono Equilibrato & Cadenzato</option>
    <option value="brian_calmo_cinema">🎬 Brian Multilingual - Cinema Cupo & Solenne</option>
    <option value="diego_profondo_rallentato">📻 Diego - Profondo & Rallentato (Senza accelerazioni)</option>
    <option value="current_master">✨ Master Audio (Traccia Video Completa)</option>
  `;
}
populateVoiceSelect();

function speakCurrentCaption(index) {
  return;
}

// Player dedicato per il test istantaneo delle voci
let previewAudio = new Audio();

testVoiceBtn.addEventListener("click", () => {
  const selected = voiceSelect.value;
  if (isPlaying) pauseVideo();

  previewAudio.pause();
  if (selected === "current_master") {
    previewAudio.src = "assets/master_soundtrack_72s.mp3?v=" + Date.now();
  } else {
    previewAudio.src = `assets/voice_samples/${selected}.mp3?v=` + Date.now();
  }
  
  testVoiceBtn.textContent = "🔊 In ascolto...";
  testVoiceBtn.disabled = true;

  previewAudio.currentTime = 0;
  previewAudio.play()
    .then(() => {
      previewAudio.onended = () => {
        testVoiceBtn.textContent = "▶️ Prova Voce";
        testVoiceBtn.disabled = false;
      };
    })
    .catch(e => {
      console.log("Preview error:", e);
      testVoiceBtn.textContent = "▶️ Prova Voce";
      testVoiceBtn.disabled = false;
    });
});

// ==========================================
// Rendering del Canvas con Movimenti Dinamici
// ==========================================
function renderFrame(time) {
  let activeScene = SCENES.find(s => time >= s.start && time < s.end);
  if (!activeScene) activeScene = SCENES[SCENES.length - 1];

  const img = loadedImages[activeScene.id];
  if (!img || !img.complete) return;

  const progress = (time - activeScene.start) / (activeScene.end - activeScene.start);

  // 1. Ken Burns Zoom & Pan di base
  let currentScale = activeScene.zoomStart + (activeScene.zoomEnd - activeScene.zoomStart) * progress;
  let currentPanX = (activeScene.panX || 0) * progress * canvas.width;
  let currentPanY = (activeScene.panY || 0) * progress * canvas.height;

  // 2. Movimenti organici cinematici specifici per ogni scena
  if (motionFxEnabled) {
    // Respiro organico continuo della camera
    currentPanX += Math.sin(time * 0.9) * 6;
    currentPanY += Math.cos(time * 0.7) * 5;

    if (activeScene.effect === "eye") {
      // Micro-tremolio oculare (involontario jitter di terrore)
      currentPanX += (Math.sin(time * 35) * 2.5);
      // Leggera dilatazione pulsante
      currentScale += Math.sin(time * 3.0) * 0.02;
    } else if (activeScene.effect === "station") {
      // Oscillazione della camminata POV in prima persona
      currentPanX += Math.sin(time * 5.0) * 5;
      currentPanY += Math.abs(Math.sin(time * 5.0)) * 7;
      // Scossa dell'urto violento a ~13.6s
      if (time >= 13.2 && time <= 14.2) {
        const bumpIntensity = (1 - Math.abs(time - 13.6) / 0.6) * 18;
        currentPanX += Math.sin(time * 45) * bumpIntensity;
        currentPanY += Math.cos(time * 50) * bumpIntensity;
      }
    } else if (activeScene.effect === "rome") {
      // Pedinamento: camminata furtiva lenta
      currentPanX += Math.sin(time * 2.8) * 4;
      currentPanY += Math.cos(time * 2.5) * 4;
    } else if (activeScene.effect === "sea") {
      // Moto ondoso del mare: dondolio verticale armonico
      currentPanY += Math.sin(time * 1.5) * 10;
      currentScale += Math.sin(time * 1.2) * 0.015;
    } else if (activeScene.effect === "bench") {
      // Vibrazione dello smartphone sulla pietra
      if (Math.sin(time * 8) > 0.3) {
        currentPanX += (Math.random() - 0.5) * 3;
        currentPanY += (Math.random() - 0.5) * 3;
      }
    } else if (activeScene.effect === "climax") {
      // Tensione finale con scatti e micro-zoom
      if (time > 70) {
        currentPanX += (Math.random() - 0.5) * 6;
      }
    }
  }

  ctx.save();
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Disegno immagine con Ken Burns & Cam Motion
  ctx.translate(canvas.width / 2 + currentPanX, canvas.height / 2 + currentPanY);
  ctx.scale(currentScale, currentScale);

  // Desaturazione progressiva per la scena della panchina / gelo
  if (activeScene.desaturate) {
    const desatVal = Math.min(100, Math.floor(progress * 85));
    ctx.filter = `saturate(${100 - desatVal}%) brightness(${100 - progress * 15}%)`;
  } else {
    ctx.filter = "none";
  }

  ctx.drawImage(img, -canvas.width / 2, -canvas.height / 2, canvas.width, canvas.height);
  ctx.restore();

  // 3. Sovrapposizione effetti particellari e atmosferici
  if (motionFxEnabled) {
    drawSceneAtmosphere(activeScene.effect, time, progress);
  }

  // 4. Vignettatura cinematografica 35mm
  const grad = ctx.createRadialGradient(
    canvas.width / 2, canvas.height / 2, canvas.width * 0.35,
    canvas.width / 2, canvas.height / 2, canvas.width * 0.78
  );
  grad.addColorStop(0, "rgba(0,0,0,0)");
  grad.addColorStop(1, "rgba(0,0,0,0.68)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 5. Sottotitoli cinetici (Kinetic Captions)
  if (captionsEnabled) {
    renderCaptions(time);
  }

  // 6. Aggiorna bagliore ambientale dello schermo
  if (ambientGlow) {
    ambientGlow.style.background = `radial-gradient(circle, ${activeScene.ambientColor} 0%, rgba(0,0,0,0) 75%)`;
  }
}

// Disegna elementi visivi atmosferici (nebbia, onde mare, lampione, display)
function drawSceneAtmosphere(effect, time, progress) {
  if (effect === "station") {
    // Nebbia volumetrica in movimento nella Stazione di Milano
    fogParticles.forEach(p => {
      p.x -= p.speed;
      if (p.x < -p.size) p.x = 1080 + p.size;
      const g = ctx.createRadialGradient(p.x, p.y, 10, p.x, p.y, p.size);
      g.addColorStop(0, `rgba(200, 225, 240, ${p.alpha * 1.5})`);
      g.addColorStop(1, "rgba(200, 225, 240, 0)");
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    });
  } else if (effect === "rome") {
    // Lampione sfarfallante a Roma
    const flicker = 0.85 + Math.sin(time * 18) * 0.08 + (Math.sin(time * 42) > 0.8 ? -0.22 : 0.04);
    const lampX = 540;
    const lampY = 420;
    const lampGlow = ctx.createRadialGradient(lampX, lampY, 30, lampX, lampY, 550);
    lampGlow.addColorStop(0, `rgba(255, 210, 80, ${0.35 * flicker})`);
    lampGlow.addColorStop(0.5, `rgba(255, 170, 40, ${0.12 * flicker})`);
    lampGlow.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = lampGlow;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Gocce di pioggia notturna umida
    ctx.strokeStyle = "rgba(220, 240, 255, 0.22)";
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    rainParticles.forEach(rp => {
      rp.y += rp.speedY;
      rp.x += rp.speedX;
      if (rp.y > 1920) rp.y = -30;
      if (rp.x < 0) rp.x = 1080;
      ctx.moveTo(rp.x, rp.y);
      ctx.lineTo(rp.x + rp.speedX * 2, rp.y + rp.len);
    });
    ctx.stroke();
  } else if (effect === "sea") {
    // Onde del mare vive a Castel dell'Ovo
    // Shimmer ondoso sulle acque del mare (zona compresa tra y=950 e y=1600)
    ctx.save();
    for (let row = 0; row < 5; row++) {
      const baseY = 1050 + row * 110;
      const waveAlpha = 0.08 + Math.sin(time * 2.0 + row) * 0.04;
      ctx.fillStyle = `rgba(180, 220, 245, ${waveAlpha})`;
      ctx.beginPath();
      ctx.moveTo(0, baseY);
      for (let x = 0; x <= 1080; x += 40) {
        const waveY = baseY + Math.sin(x * 0.015 + time * 2.8 + row) * 8 + Math.cos(x * 0.008 - time) * 4;
        ctx.lineTo(x, waveY);
      }
      ctx.lineTo(1080, baseY + 60);
      ctx.lineTo(0, baseY + 60);
      ctx.closePath();
      ctx.fill();
    }

    // Spruzzi e vapore marino che si alzano dai flutti
    seaMistParticles.forEach(mp => {
      mp.y += mp.speedY;
      mp.x += mp.speedX;
      if (mp.y < 850) {
        mp.y = 1700 + Math.random() * 200;
        mp.x = 150 + Math.random() * 800;
      }
      const mg = ctx.createRadialGradient(mp.x, mp.y, 4, mp.x, mp.y, mp.size);
      mg.addColorStop(0, `rgba(230, 245, 255, ${mp.alpha})`);
      mg.addColorStop(1, "rgba(230, 245, 255, 0)");
      ctx.fillStyle = mg;
      ctx.beginPath();
      ctx.arc(mp.x, mp.y, mp.size, 0, Math.PI * 2);
      ctx.fill();
    });

    // Vento gelido desaturante verso la fine della scena (44s-48s)
    if (progress > 0.65) {
      const coldFactor = (progress - 0.65) / 0.35;
      ctx.fillStyle = `rgba(0, 190, 255, ${coldFactor * 0.16})`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    ctx.restore();
  } else if (effect === "bench") {
    // Bagliore intermittente del display telefonico che illumina la panchina
    const phonePulse = Math.max(0, Math.sin(time * 7));
    const phoneGlow = ctx.createRadialGradient(540, 1150, 10, 540, 1150, 380);
    phoneGlow.addColorStop(0, `rgba(0, 229, 255, ${0.45 * phonePulse})`);
    phoneGlow.addColorStop(0.5, `rgba(0, 150, 255, ${0.15 * phonePulse})`);
    phoneGlow.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = phoneGlow;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  } else if (effect === "climax") {
    // Glitch e aberrazione cromatica sul riflesso finale (secondi 70-72)
    if (time >= 69.8) {
      const glitchStrength = (time - 69.8) * 12;
      ctx.fillStyle = `rgba(255, 0, 60, 0.12)`;
      ctx.fillRect(Math.sin(time * 60) * glitchStrength, 0, canvas.width, canvas.height);
      ctx.fillStyle = `rgba(0, 229, 255, 0.12)`;
      ctx.fillRect(-Math.sin(time * 60) * glitchStrength, 0, canvas.width, canvas.height);
    }
  }
}

// Rendering dei sottotitoli cinetici (Kinetic Captions)
function renderCaptions(time) {
  const captionIndex = CAPTIONS.findIndex(c => time >= c.start && time < c.end);
  if (captionIndex === -1) return;

  const caption = CAPTIONS[captionIndex];

  ctx.save();
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  const boxY = canvas.height * 0.78;
  const fontSize = 52;
  ctx.font = `900 ${fontSize}px 'Montserrat', sans-serif`;

  const words = caption.text.split(" ");
  let lines = [];
  let currentLine = "";

  words.forEach(w => {
    const testLine = currentLine ? `${currentLine} ${w}` : w;
    const testWidth = ctx.measureText(testLine).width;
    if (testWidth > canvas.width * 0.85) {
      lines.push(currentLine);
      currentLine = w;
    } else {
      currentLine = testLine;
    }
  });
  if (currentLine) lines.push(currentLine);

  const lineHeight = fontSize * 1.35;
  const startY = boxY - ((lines.length - 1) * lineHeight) / 2;

  lines.forEach((lineText, lIdx) => {
    const lineY = startY + lIdx * lineHeight;

    // Ombra profonda per massima leggibilità
    ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
    ctx.shadowBlur = 18;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 4;

    // Background pill per ogni riga
    const lineWidth = ctx.measureText(lineText).width;
    ctx.fillStyle = "rgba(8, 11, 18, 0.82)";
    ctx.beginPath();
    ctx.roundRect(
      canvas.width / 2 - lineWidth / 2 - 24,
      lineY - fontSize / 2 - 10,
      lineWidth + 48,
      fontSize + 20,
      14
    );
    ctx.fill();

    // Contorno nero sul testo
    ctx.lineWidth = 6;
    ctx.strokeStyle = "#000000";
    ctx.strokeText(lineText, canvas.width / 2, lineY);

    // Testo evidenziato o bianco
    if (caption.highlight && lineText.includes(caption.highlight)) {
      ctx.fillStyle = caption.color || "#ffe600";
    } else {
      ctx.fillStyle = "#ffffff";
    }
    ctx.fillText(lineText, canvas.width / 2, lineY);
  });

  ctx.restore();
}

// ==========================================
// Loop di Riproduzione & Aggiornamento UI
// ==========================================
function updateUI() {
  const pct = (currentTime / TOTAL_DURATION) * 100;
  progressBar.style.width = `${Math.min(100, pct)}%`;

  const curM = Math.floor(currentTime / 60);
  const curS = Math.floor(currentTime % 60).toString().padStart(2, "0");
  const totM = Math.floor(TOTAL_DURATION / 60);
  const totS = Math.floor(TOTAL_DURATION % 60).toString().padStart(2, "0");
  timeDisplay.textContent = `${curM}:${curS} / ${totM}:${totS}`;
}

function playVideo() {
  initAudioContext();
  isPlaying = true;
  lastTimestamp = performance.now();
  playIcon.style.display = "none";
  pauseIcon.style.display = "block";
  playOverlay.style.display = "none";

  if (soundtrackAudio) {
    soundtrackAudio.currentTime = currentTime;
    soundtrackAudio.muted = !voiceEnabled;
    soundtrackAudio.play().catch(e => console.log("Soundtrack play prevented:", e));
  }

  requestAnimationFrame(step);
}

function pauseVideo() {
  isPlaying = false;
  playIcon.style.display = "block";
  pauseIcon.style.display = "none";
  playOverlay.style.display = "flex";

  if (soundtrackAudio) {
    soundtrackAudio.pause();
  }

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  stopSeaWavesAbrupt();
}

function step(timestamp) {
  if (!isPlaying) return;

  const dt = (timestamp - lastTimestamp) / 1000;
  lastTimestamp = timestamp;

  // Usa l'audio hardware come clock di riferimento master per evitare micro-scatti e distorsioni da seek
  if (soundtrackAudio && !soundtrackAudio.paused) {
    currentTime = soundtrackAudio.currentTime;
  } else {
    currentTime += dt;
  }

  if (currentTime >= TOTAL_DURATION) {
    currentTime = 0;
    if (soundtrackAudio) {
      soundtrackAudio.currentTime = 0;
      soundtrackAudio.pause();
    }
    pauseVideo();
    resetSfxTriggers();
    currentCaptionIndex = -1;
    renderFrame(0);
    updateUI();
    return;
  }

  checkSfxTriggers(currentTime);
  renderFrame(currentTime);
  updateUI();

  requestAnimationFrame(step);
}

// ==========================================
// Event Listeners
// ==========================================
playBtn.addEventListener("click", () => {
  if (isPlaying) pauseVideo();
  else playVideo();
});

bigPlayBtn.addEventListener("click", () => {
  playVideo();
});

playOverlay.addEventListener("click", (e) => {
  if (e.target !== bigPlayBtn && !bigPlayBtn.contains(e.target)) {
    playVideo();
  }
});

restartBtn.addEventListener("click", () => {
  currentTime = 0;
  if (soundtrackAudio) {
    soundtrackAudio.currentTime = 0;
  }
  resetSfxTriggers();
  currentCaptionIndex = -1;
  renderFrame(0);
  updateUI();
});

progressBarContainer.addEventListener("click", (e) => {
  const rect = progressBarContainer.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const pct = clickX / rect.width;
  currentTime = pct * TOTAL_DURATION;
  if (soundtrackAudio) {
    soundtrackAudio.currentTime = currentTime;
  }
  currentCaptionIndex = -1;
  resetSfxTriggers();
  renderFrame(currentTime);
  updateUI();
});

voiceToggle.addEventListener("click", () => {
  voiceEnabled = !voiceEnabled;
  voiceToggle.classList.toggle("active", voiceEnabled);
  if (soundtrackAudio) {
    soundtrackAudio.muted = !voiceEnabled;
  }
});

sfxToggle.addEventListener("click", () => {
  sfxEnabled = !sfxEnabled;
  sfxToggle.classList.toggle("active", sfxEnabled);
  if (soundtrackAudio) {
    soundtrackAudio.muted = !sfxEnabled;
  }
  if (!sfxEnabled) {
    stopSeaWavesAbrupt();
  }
});

captionsToggle.addEventListener("click", () => {
  captionsEnabled = !captionsEnabled;
  captionsToggle.classList.toggle("active", captionsEnabled);
  renderFrame(currentTime);
});

motionFxToggle.addEventListener("change", (e) => {
  motionFxEnabled = e.target.checked;
  renderFrame(currentTime);
});

fullscreenBtn.addEventListener("click", () => {
  const elem = document.getElementById("screenContainer");
  if (!document.fullscreenElement) {
    elem.requestFullscreen().catch(err => alert(err.message));
  } else {
    document.exitFullscreen();
  }
});

// Esportatore Video MP4 / WebM con Audio Integrato
exportBtn.addEventListener("click", async () => {
  initAudioContext();
  if (exportBtn.disabled) return;

  exportBtn.disabled = true;
  exportBtn.innerHTML = "<span>Rendering in corso...</span>";
  recordingBadge.style.display = "flex";

  isPlaying = false;
  currentTime = 0;
  resetSfxTriggers();
  currentCaptionIndex = -1;

  // Cattura stream da canvas + traccia audio sintetizzata
  const canvasStream = canvas.captureStream(30); // 30 FPS
  const combinedStream = new MediaStream();

  canvasStream.getVideoTracks().forEach(t => combinedStream.addTrack(t));
  if (audioDest && audioDest.stream.getAudioTracks().length > 0) {
    audioDest.stream.getAudioTracks().forEach(t => combinedStream.addTrack(t));
  }

  let recorder;
  try {
    recorder = new MediaRecorder(combinedStream, { mimeType: "video/webm;codecs=vp9,opus" });
  } catch (e) {
    try {
      recorder = new MediaRecorder(combinedStream, { mimeType: "video/webm" });
    } catch (e2) {
      recorder = new MediaRecorder(combinedStream);
    }
  }

  const chunks = [];
  recorder.ondataavailable = (e) => {
    if (e.data.size > 0) chunks.push(e.data);
  };

  recorder.onstop = () => {
    const blob = new Blob(chunks, { type: "video/webm" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "il_terzo_avvistamento_9x16.webm";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    recordingBadge.style.display = "none";
    exportBtn.disabled = false;
    exportBtn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      <span>Esporta Video</span>
    `;
    alert("Video esportato con successo con audio & effetti! Pronto per TikTok e Reels.");
  };

  recorder.start();

  const renderInterval = setInterval(() => {
    currentTime += 0.1;
    recProgress.textContent = `${Math.min(100, Math.floor((currentTime / TOTAL_DURATION) * 100))}%`;
    checkSfxTriggers(currentTime);
    renderFrame(currentTime);
    updateUI();

    if (currentTime >= TOTAL_DURATION) {
      clearInterval(renderInterval);
      recorder.stop();
      currentTime = 0;
      resetSfxTriggers();
      renderFrame(0);
      updateUI();
    }
  }, 33);
});

// Render iniziale del primo fotogramma
renderFrame(0);
