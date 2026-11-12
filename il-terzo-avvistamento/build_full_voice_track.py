#!/usr/bin/env python3
"""
Generazione completa delle 18 battute e montaggio Master Audio 72s
con voce adulta, profonda, riflessiva e lenta.
"""

import os
import asyncio
import subprocess
import numpy as np
import scipy.io.wavfile as wav
import edge_tts

BASE_DIR = "/media/corrado/DATI/REPO_GH/Progetto_pers/Storie/il-terzo-avvistamento"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
VOICE_DIR = os.path.join(ASSETS_DIR, "voice_clips")
MASTER_WAV = os.path.join(ASSETS_DIR, "master_soundtrack_72s.wav")
VOICE_ONLY_WAV = os.path.join(ASSETS_DIR, "voice_only_72s.wav")
MASTER_AUDIO_WAV = os.path.join(ASSETS_DIR, "master_audio_72s.wav")
MASTER_MP3 = os.path.join(ASSETS_DIR, "master_soundtrack_72s.mp3")

FFMPEG_BIN = "/tmp/ffmpeg" if os.path.exists("/tmp/ffmpeg") else "ffmpeg"
SR = 44100
DURATION = 72.0
TOTAL_SAMPLES = int(SR * DURATION)

LINES = [
    (1, 0.2, "Le probabilità di incontrare lo stesso sconosciuto..."),
    (2, 3.2, "in tre città diverse... sono zero."),
    (3, 6.2, "La prima volta: Milano. Nebbia fitta."),
    (4, 9.8, "Nella calca, un ragazzo mi urta. Occhi vitrei, cappotto nero."),
    (5, 14.8, "Non chiede scusa. Scompare nel nulla tra la folla."),
    (6, 18.7, "Due anni dopo. Roma, vicoli deserti alle tre di notte."),
    (7, 23.0, "Sento dei passi. Accelero... l'ombra accelera."),
    (8, 27.0, "Sotto un lampione: era lui. Non era invecchiato di un giorno."),
    (9, 31.0, "Ha sorriso e mi ha sussurrato: la data di oggi."),
    (10, 34.3, "Oggi. Napoli, Castel dell'Ovo. Davanti al mare."),
    (11, 39.0, "Pensavo di essere al sicuro... poi, quel gelo sulla nuca."),
    (12, 43.2, "E un silenzio anomalo: il mare si spegne di colpo."),
    (13, 48.2, "Sulla panchina c'è un telefono. Accanto, quel cappotto."),
    (14, 52.5, "Chiamata in arrivo da: mio stesso numero."),
    (15, 56.4, "Una mano gelida sulla spalla. Ho trattenuto il respiro."),
    (16, 60.3, "Te l'avevo detto che era oggi."),
    (17, 63.6, "Nel riflesso nero ho visto la mia faccia..."),
    (18, 67.4, "Ma i miei occhi... erano diventati i suoi.")
]

async def generate_line(num, text, voice, rate, pitch, eq, tmp_dir):
    raw_mp3 = os.path.join(tmp_dir, f"raw_{num:02d}.mp3")
    proc_wav = os.path.join(tmp_dir, f"line_{num:02d}.wav")

    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(raw_mp3)

    # Conversione con EQ caldo e compressione
    cmd = [
        FFMPEG_BIN, "-y", "-i", raw_mp3,
        "-af", eq,
        "-ar", str(SR), "-ac", "1",
        proc_wav
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Trim solo a inizio e fine, preservando le pause riflessive interne
    sr, d = wav.read(proc_wav)
    peak = np.max(np.abs(d))
    if peak > 0:
        thresh = 0.012 * peak
        active = np.where(np.abs(d) > thresh)[0]
        if len(active) > 0:
            pad = int(0.05 * sr)
            start_idx = max(0, active[0] - pad)
            end_idx = min(len(d), active[-1] + pad)
            d = d[start_idx:end_idx]
            # Soft micro fade-in/out
            fade_len = int(0.005 * sr)
            if len(d) > fade_len * 2:
                fade_in = np.linspace(0, 1, fade_len)
                fade_out = np.linspace(1, 0, fade_len)
                d[:fade_len] = (d[:fade_len] * fade_in).astype(np.int16)
                d[-fade_len:] = (d[-fade_len:] * fade_out).astype(np.int16)
            wav.write(proc_wav, sr, d)

    return proc_wav

async def build_voice_master(
    voice="it-IT-GiuseppeMultilingualNeural",
    rate="-10%",
    pitch="-8Hz",
    eq="equalizer=f=110:t=q:w=1.0:g=4.5,equalizer=f=3000:t=q:w=1.0:g=1.0,acompressor=threshold=-16dB:ratio=3:attack=20:release=200"
):
    tmp_dir = "/tmp/giuseppe_cupo_master"
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(VOICE_DIR, exist_ok=True)

    print(f"🎙️ Generazione traccia MASTER CUPO THRILLER DEFINITIVA: {voice} (rate={rate}, pitch={pitch})...")
    voice_track = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    final_schedule = []

    prev_end = 0.0
    for num, preferred_start, text in LINES:
        wav_path = await generate_line(num, text, voice, rate, pitch, eq, tmp_dir)
        sr, data = wav.read(wav_path)
        dur = len(data) / sr

        # Assicura zero overlap preservando le pause riflessive
        st = max(preferred_start, prev_end + 0.10)
        end_t = min(DURATION, st + dur)
        prev_end = end_t
        final_schedule.append((num, st, end_t, text))

        # Copia in assets/voice_clips
        dest_wav = os.path.join(VOICE_DIR, f"line_{num:02d}.wav")
        wav.write(dest_wav, sr, data)

        # Mix nel master 72s
        s_start = int(st * SR)
        v_float = data.astype(np.float32) / 32767.0
        s_end = min(TOTAL_SAMPLES, s_start + len(v_float))
        actual_len = s_end - s_start
        voice_track[s_start:s_end] += v_float[:actual_len]
        print(f"  ✓ Battuta {num:02d}: {st:4.1f}s -> {end_t:4.1f}s (dur: {dur:4.2f}s) | \"{text[:35]}...\"")

    # Normalizzazione con picco a 0.88 (-1.1 dBFS)
    peak = np.max(np.abs(voice_track))
    if peak > 0:
        voice_track = (voice_track / peak) * 0.88

    pcm_mono = (voice_track * 32767).astype(np.int16)
    pcm_stereo = np.column_stack((pcm_mono, pcm_mono))

    wav.write(MASTER_WAV, SR, pcm_stereo)
    wav.write(VOICE_ONLY_WAV, SR, pcm_stereo)
    wav.write(MASTER_AUDIO_WAV, SR, pcm_stereo)

    subprocess.run([
        FFMPEG_BIN, "-y", "-i", MASTER_WAV,
        "-c:a", "libmp3lame", "-b:a", "192k",
        MASTER_MP3
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n✅ Master cupo thriller definitivo esportato in {MASTER_MP3} e {MASTER_WAV}")
    print("\n--- TIMINGS DEFINITIVI PER CAPTIONS ---")
    for num, st, end_t, text in final_schedule:
        print(f"    ({num:2d}, {st:4.1f}, {end_t:4.1f}), # {text[:25]}")

if __name__ == "__main__":
    asyncio.run(build_voice_master())

