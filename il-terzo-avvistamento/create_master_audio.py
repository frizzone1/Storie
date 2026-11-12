#!/usr/bin/env python3
"""
Crea la traccia audio MASTER definitiva di 72 secondi per 'Il Terzo Avvistamento'.
VOCE SELEZIONATA: Diego (Profondo & Lento - rate=-10%, pitch=-3Hz)
Zero musica, Zero rumori, Zero distorsione, Zero sovrapposizioni.
"""

import os
import subprocess
import numpy as np
import scipy.io.wavfile as wav

BASE_DIR = "/media/corrado/DATI/REPO_GH/Progetto_pers/Storie/il-terzo-avvistamento"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
VOICE_DIR = os.path.join(ASSETS_DIR, "voice_clips")
MASTER_WAV = os.path.join(ASSETS_DIR, "master_soundtrack_72s.wav")
VOICE_ONLY_WAV = os.path.join(ASSETS_DIR, "voice_only_72s.wav")
MASTER_AUDIO_WAV = os.path.join(ASSETS_DIR, "master_audio_72s.wav")
MASTER_MP3 = os.path.join(ASSETS_DIR, "master_soundtrack_72s.mp3")

SR = 44100
DURATION = 72.0
TOTAL_SAMPLES = int(SR * DURATION)

VOICE_SCHEDULE = [
    # Scena 1: 0.0s - 6.0s
    (1, 1.12, 0.1),
    (2, 1.12, 3.2),
    # Scena 2: 6.0s - 18.5s
    (3, 1.25, 6.1),
    (4, 1.25, 9.8),
    (5, 1.25, 14.9),
    # Scena 3: 18.5s - 34.0s
    (6, 1.28, 18.6),
    (7, 1.28, 22.8),
    (8, 1.28, 26.7),
    (9, 1.28, 31.0),
    # Scena 4: 34.0s - 48.0s
    (10, 1.15, 34.2),
    (11, 1.15, 39.8),
    (12, 1.15, 43.6),
    # Scena 5: 48.0s - 60.0s
    (13, 1.18, 48.2),
    (14, 1.18, 53.1),
    (15, 1.18, 55.8),
    # Scena 6: 60.0s - 72.0s
    (16, 1.00, 60.3),
    (17, 1.00, 63.3),
    (18, 1.00, 67.2),
]

def main():
    print("🎙️ Assemblaggio traccia audio MASTER (Diego: Profondo & Lento)...")
    ffmpeg_bin = "/tmp/ffmpeg" if os.path.exists("/tmp/ffmpeg") else "ffmpeg"
    tmp_dir = "/tmp/diego_master_process"
    os.makedirs(tmp_dir, exist_ok=True)

    voice_track = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

    for num, spd, st in VOICE_SCHEDULE:
        raw_p = os.path.join(VOICE_DIR, f"line_{num:02d}.wav")
        sr, d = wav.read(raw_p)
        thresh = 0.015 * np.max(np.abs(d))
        active = np.where(np.abs(d) > thresh)[0]
        pad = int(0.04 * sr)
        start_idx = max(0, active[0] - pad)
        end_idx = min(len(d), active[-1] + pad)
        trimmed = d[start_idx:end_idx]

        fade_len = int(0.005 * sr)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        trimmed[:fade_len] = (trimmed[:fade_len] * fade_in).astype(np.int16)
        trimmed[-fade_len:] = (trimmed[-fade_len:] * fade_out).astype(np.int16)

        trim_p = os.path.join(tmp_dir, f"trim_{num:02d}.wav")
        proc_p = os.path.join(tmp_dir, f"proc_{num:02d}.wav")
        wav.write(trim_p, sr, trimmed)

        if abs(spd - 1.0) > 0.01:
            cmd = [ffmpeg_bin, "-y", "-i", trim_p, "-filter:a", f"atempo={spd}", proc_p]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            sr_f, final_d = wav.read(proc_p)
        else:
            sr_f, final_d = sr, trimmed

        v_float = final_d.astype(np.float32) / 32767.0
        dur_sec = len(v_float) / sr_f
        s_start = int(st * SR)
        s_end = min(TOTAL_SAMPLES, s_start + len(v_float))
        actual_len = s_end - s_start
        voice_track[s_start:s_end] += v_float[:actual_len]
        print(f"  ✓ Battuta {num:02d}: {st:4.1f}s -> {st + dur_sec:4.1f}s (dur: {dur_sec:4.2f}s)")

    # Normalizzazione sicura con picco a 0.85
    peak = np.max(np.abs(voice_track))
    if peak > 0:
        voice_track = (voice_track / peak) * 0.85

    pcm_mono = (voice_track * 32767).astype(np.int16)
    pcm_stereo = np.column_stack((pcm_mono, pcm_mono))

    wav.write(MASTER_WAV, SR, pcm_stereo)
    wav.write(VOICE_ONLY_WAV, SR, pcm_stereo)
    wav.write(MASTER_AUDIO_WAV, SR, pcm_stereo)
    subprocess.run([ffmpeg_bin, "-y", "-i", MASTER_WAV, "-c:a", "libmp3lame", "-b:a", "192k", MASTER_MP3], check=True)
    print("✅ Master audio completato!")

if __name__ == "__main__":
    main()
