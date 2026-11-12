#!/usr/bin/env python3
"""
Generatore Sound Design Procedurale 72 Secondi per "Il Terzo Avvistamento"
Sintetizza una traccia audio stereo ad alta fedeltà a 44.1 kHz con tutte le sonorità del thriller:
- Drone oscuro e accordi cinematografici
- Onde del mare a Castel dell'Ovo (rumore filtrato e modulazione LFO)
- Taglio improvviso al silenzio assoluto a 43.5s
- Acufene fischio 7.8 kHz a 44s
- Squillo telefonico cupo e battito cardiaco accelerato
- Jumpscare slam finale
"""

import os
import numpy as np
import scipy.io.wavfile as wav

OUTPUT_WAV = "/media/corrado/DATI/REPO_GH/Progetto_pers/Storie/il-terzo-avvistamento/assets/soundtrack_72s.wav"
SR = 44100
DURATION = 72.0
TOTAL_SAMPLES = int(SR * DURATION)

def main():
    print("🔊 Generazione colonna sonora Sound Design 72s...")
    t = np.linspace(0, DURATION, TOTAL_SAMPLES, endpoint=False)
    left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

    def add_tone(start, dur, freq, amp, pan=0.0, fade=0.1):
        s_idx = int(start * SR)
        e_idx = min(TOTAL_SAMPLES, int((start + dur) * SR))
        length = e_idx - s_idx
        if length <= 0: return
        sub_t = np.linspace(0, dur, length, endpoint=False)
        wave = np.sin(2 * np.pi * freq * sub_t)
        # Envelope
        env = np.ones(length, dtype=np.float32)
        fade_samples = int(fade * SR)
        if fade_samples > 0 and fade_samples * 2 < length:
            env[:fade_samples] = np.linspace(0, 1, fade_samples)
            env[-fade_samples:] = np.linspace(1, 0, fade_samples)
        wave = wave * env * amp
        l_gain = np.cos((pan + 1) * np.pi / 4)
        r_gain = np.sin((pan + 1) * np.pi / 4)
        left[s_idx:e_idx] += wave * l_gain
        right[s_idx:e_idx] += wave * r_gain

    def add_drop(start, f_start, f_end, dur, amp):
        s_idx = int(start * SR)
        e_idx = min(TOTAL_SAMPLES, int((start + dur) * SR))
        length = e_idx - s_idx
        if length <= 0: return
        sub_t = np.linspace(0, 1, length)
        freqs = f_start * ((f_end / f_start) ** sub_t)
        phase = 2 * np.pi * np.cumsum(freqs) / SR
        # Include harmonics for audibility on small speakers
        wave = (np.sin(phase) * 0.6 + np.sin(phase * 2) * 0.3 + np.sin(phase * 3) * 0.1)
        env = np.exp(-sub_t * 3.5)
        sound = wave * env * amp
        left[s_idx:e_idx] += sound
        right[s_idx:e_idx] += sound

    # 1. SCENA 1: GANCIO (0:00 - 0:05)
    # Sub drop di apertura
    add_drop(0.0, 160, 45, 2.5, 0.7)
    # Dissonanza metallica
    add_tone(0.1, 4.0, 587.3, 0.08, pan=-0.3, fade=0.5) # D5
    add_tone(0.2, 4.0, 622.2, 0.07, pan=0.3, fade=0.5)  # Eb5 (dissonante)

    # 2. SCENA 2: MILANO STAZIONE (0:05 - 0:18)
    # Drone cupo Re minore (D2, A2, F3)
    milano_t = np.linspace(0, 13.0, int(13.0 * SR))
    drone = (np.sin(2 * np.pi * 73.4 * milano_t) * 0.22 +
             np.sin(2 * np.pi * 110.0 * milano_t) * 0.18 +
             np.sin(2 * np.pi * 174.6 * milano_t) * 0.14 +
             np.sin(2 * np.pi * 146.8 * milano_t) * 0.12)
    # Fade in/out
    env_m = np.ones_like(milano_t)
    env_m[:SR] = np.linspace(0, 1, SR)
    env_m[-SR:] = np.linspace(1, 0, SR)
    s_m = int(5.0 * SR)
    e_m = s_m + len(milano_t)
    left[s_m:e_m] += drone * env_m * 0.8
    right[s_m:e_m] += drone * env_m * 0.8

    # Colpo dell'urto violento a 13.6s
    add_drop(13.6, 220, 40, 1.8, 0.75)
    add_tone(13.6, 1.5, 95.0, 0.35, fade=0.2)

    # 3. SCENA 3: ROMA VICOLO (0:18 - 0:34)
    # Passi ritmici bagnati
    for step_i, step_time in enumerate([18.5, 19.4, 20.3, 21.2, 22.1, 23.0, 23.8, 24.6, 25.4, 26.2]):
        pan_step = -0.4 if step_i % 2 == 0 else 0.4
        add_tone(step_time, 0.12, 180 + (step_i % 3) * 20, 0.25, pan=pan_step, fade=0.02)
        add_tone(step_time + 0.02, 0.08, 90, 0.3, pan=pan_step, fade=0.01)

    # Riser di tensione crescente verso il lampione (26s - 34s)
    riser_len = int(8.0 * SR)
    riser_t = np.linspace(0, 8.0, riser_len)
    riser_freq = np.linspace(180, 520, riser_len)
    riser_phase = 2 * np.pi * np.cumsum(riser_freq) / SR
    riser_wave = np.sin(riser_phase) * np.linspace(0.02, 0.28, riser_len)
    s_r = int(26.0 * SR)
    e_r = s_r + riser_len
    left[s_r:e_r] += riser_wave
    right[s_r:e_r] += riser_wave

    # 4. SCENA 4: NAPOLI CASTEL DELL'OVO - IL MARE (0:34 - 0:48)
    # Onde del mare realistiche generate con rumore filtrato e modulazione LFO
    sea_len = int(9.5 * SR) # da 34.0 a 43.5s esatti
    sea_noise = np.random.normal(0, 1, sea_len).astype(np.float32)
    # Smooth moving average per creare onde scure
    window = 120
    sea_smooth = np.convolve(sea_noise, np.ones(window)/window, mode='same')
    sea_t = np.linspace(0, 9.5, sea_len)
    # Modulazione dell'infrangersi dell'onda
    sea_lfo = (np.sin(2 * np.pi * 0.24 * sea_t) ** 2) * 0.35 + 0.1
    # Dissolvenza in ingresso da 34s
    sea_env = np.ones(sea_len, dtype=np.float32)
    sea_env[:int(1.2 * SR)] = np.linspace(0, 1, int(1.2 * SR))
    # Taglio netto al silenzio esatto a 43.5s!
    sea_env[-int(0.08 * SR):] = np.linspace(1, 0, int(0.08 * SR))
    sea_wave = sea_smooth * sea_lfo * sea_env * 3.5
    s_sea = int(34.0 * SR)
    e_sea = s_sea + sea_len
    left[s_sea:e_sea] += sea_wave
    right[s_sea:e_sea] += sea_wave

    # Vento e maretta armonico
    add_tone(34.2, 9.0, 164.8, 0.08, pan=-0.2, fade=1.0) # E3
    add_tone(34.5, 8.7, 220.0, 0.06, pan=0.2, fade=1.0)  # A3

    # SILENZIO ASSOLUTO: 43.5s -> 44.0s (mezzo secondo di vuoto cosmico)

    # Fischio acuto ACUFENE / TINNITUS a 44.0s (7800 Hz)
    tin_len = int(4.2 * SR)
    tin_t = np.linspace(0, 4.2, tin_len)
    tin_wave = np.sin(2 * np.pi * 7800 * tin_t) * 0.08
    tin_env = np.ones(tin_len, dtype=np.float32)
    tin_env[:int(0.4 * SR)] = np.linspace(0, 1, int(0.4 * SR))
    tin_env[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
    s_tin = int(44.0 * SR)
    e_tin = s_tin + tin_len
    left[s_tin:e_tin] += tin_wave * tin_env
    right[s_tin:e_tin] += tin_wave * tin_env

    # 5. SCENA 5: PANCHINA & TELEFONO (0:48 - 1:00)
    # Squillo telefonico cupo (440Hz + 480Hz)
    def add_ring(ring_start):
        add_tone(ring_start, 0.45, 440, 0.16, fade=0.03)
        add_tone(ring_start, 0.45, 480, 0.16, fade=0.03)
        add_tone(ring_start + 0.65, 0.45, 440, 0.16, fade=0.03)
        add_tone(ring_start + 0.65, 0.45, 480, 0.16, fade=0.03)

    add_ring(48.5)
    add_ring(52.5)
    add_ring(56.5)

    # Battito cardiaco cupo (Thump-thump) in accelerazione
    for hb_time in [50.0, 51.5, 53.0, 54.2, 55.4, 56.5, 57.5, 58.4, 59.2]:
        add_tone(hb_time, 0.14, 60, 0.42, fade=0.02)
        add_tone(hb_time + 0.18, 0.12, 50, 0.32, fade=0.02)

    # 6. SCENA 6: CLIMAX & JUMPSCARE FINALE (1:00 - 1:12)
    # Drone d'attesa teso (Re basso + Si bemolle inquietante)
    add_tone(60.0, 11.2, 73.4, 0.28, fade=1.0)
    add_tone(60.2, 11.0, 116.5, 0.18, fade=1.0)
    add_tone(64.0, 7.2, 233.1, 0.12, fade=1.0)

    # Riser finale verso lo shock (68s -> 71.3s)
    end_len = int(3.3 * SR)
    end_t = np.linspace(0, 3.3, end_len)
    end_f = np.linspace(150, 680, end_len)
    end_phase = 2 * np.pi * np.cumsum(end_f) / SR
    end_wave = np.sin(end_phase) * np.linspace(0.01, 0.32, end_len)
    s_end = int(68.0 * SR)
    e_end = s_end + end_len
    left[s_end:e_end] += end_wave
    right[s_end:e_end] += end_wave

    # JUMPSCARE SLAM FINALE A 71.3s
    add_drop(71.3, 240, 35, 0.7, 0.95)
    add_tone(71.3, 0.65, 120, 0.5, fade=0.05)
    # Stacco netto a nero e silenzio a 72.0s

    # Normalizzazione per evitare clipping e garantire volume ideale (-14 LUFS)
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if max_val > 0:
        left = (left / max_val) * 0.92
        right = (right / max_val) * 0.92

    # Scrittura in formato WAV 16-bit PCM Stereo
    audio_16 = np.column_stack((
        (left * 32767).astype(np.int16),
        (right * 32767).astype(np.int16)
    ))

    os.makedirs(os.path.dirname(OUTPUT_WAV), exist_ok=True)
    wav.write(OUTPUT_WAV, SR, audio_16)
    print(f"✅ Soundtrack generata con successo: {OUTPUT_WAV}")
    print(f"⚖️ Dimensione: {round(os.path.getsize(OUTPUT_WAV) / 1024, 1)} KB")

if __name__ == "__main__":
    main()
