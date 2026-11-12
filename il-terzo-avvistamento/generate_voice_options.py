#!/usr/bin/env python3
"""
Generatore di provini vocali per "Il Terzo Avvistamento".
Genera 5 campioni con impostazioni:
- Più profonda (pitch ribassato, EQ caldo sui bassi)
- Più adulta (timbro maturo)
- Riflessiva (ritmo controllato, pause naturali)
- Più lenta (rate rallentato -12% / -18%)
"""

import os
import asyncio
import subprocess
import edge_tts

BASE_DIR = "/media/corrado/DATI/REPO_GH/Progetto_pers/Storie/il-terzo-avvistamento"
SAMPLES_DIR = os.path.join(BASE_DIR, "assets", "voice_samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)

FFMPEG_BIN = "/tmp/ffmpeg" if os.path.exists("/tmp/ffmpeg") else "ffmpeg"

TEST_TEXT = "Le probabilità di incontrare lo stesso sconosciuto in tre città diverse... sono zero. Sotto un lampione: era lui. Non era invecchiato di un giorno."

OPTIONS = [
    {
        "id": "giuseppe_riflessivo_caldo",
        "title": "Giuseppe - Adulto, Riflessivo & Caldo",
        "voice": "it-IT-GiuseppeMultilingualNeural",
        "rate": "-12%",
        "pitch": "-4Hz",
        "eq": "equalizer=f=130:t=q:w=1.2:g=3.5,equalizer=f=3200:t=q:w=1.0:g=1.5,acompressor=threshold=-18dB:ratio=2.5:attack=25:release=200",
    },
    {
        "id": "giuseppe_cupo_profondo_lento",
        "title": "Giuseppe - Cupo Thriller, Molto Profondo & Lento",
        "voice": "it-IT-GiuseppeMultilingualNeural",
        "rate": "-18%",
        "pitch": "-8Hz",
        "eq": "equalizer=f=110:t=q:w=1.0:g=4.5,equalizer=f=3000:t=q:w=1.0:g=1.0,acompressor=threshold=-16dB:ratio=3:attack=20:release=200",
    },
    {
        "id": "giuseppe_baritono_equilibrato",
        "title": "Giuseppe - Baritono Equilibrato & Cadenzato",
        "voice": "it-IT-GiuseppeMultilingualNeural",
        "rate": "-15%",
        "pitch": "-6Hz",
        "eq": "equalizer=f=120:t=q:w=1.1:g=3.8,equalizer=f=3200:t=q:w=1.0:g=1.2,acompressor=threshold=-17dB:ratio=2.8:attack=20:release=200",
    },
    {
        "id": "brian_calmo_cinema",
        "title": "Brian Multilingual - Voce Cinema Cupa & Solenne",
        "voice": "en-US-BrianMultilingualNeural",
        "rate": "-14%",
        "pitch": "-5Hz",
        "eq": "equalizer=f=115:t=q:w=1.1:g=3.5,equalizer=f=3300:t=q:w=1.0:g=1.2,acompressor=threshold=-18dB:ratio=2.5:attack=20:release=180",
    },
    {
        "id": "diego_profondo_rallentato",
        "title": "Diego - Profondo & Rallentato (Senza accelerazioni)",
        "voice": "it-IT-DiegoNeural",
        "rate": "-15%",
        "pitch": "-7Hz",
        "eq": "equalizer=f=125:t=q:w=1.2:g=4.0,equalizer=f=3000:t=q:w=1.0:g=1.0,acompressor=threshold=-18dB:ratio=2.8:attack=20:release=180",
    }
]

async def generate_option(opt):
    raw_mp3 = f"/tmp/{opt['id']}_raw.mp3"
    final_mp3 = os.path.join(SAMPLES_DIR, f"{opt['id']}.mp3")
    final_wav = os.path.join(SAMPLES_DIR, f"{opt['id']}.wav")

    print(f"🎙️ Generazione: {opt['title']}...")
    communicate = edge_tts.Communicate(TEST_TEXT, opt["voice"], rate=opt["rate"], pitch=opt["pitch"])
    await communicate.save(raw_mp3)

    # Processamento audio professionale: EQ calore, compressione per dinamica controllata e mastering
    cmd_mp3 = [
        FFMPEG_BIN, "-y", "-i", raw_mp3,
        "-af", opt["eq"],
        "-c:a", "libmp3lame", "-b:a", "192k",
        final_mp3
    ]
    subprocess.run(cmd_mp3, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cmd_wav = [
        FFMPEG_BIN, "-y", "-i", raw_mp3,
        "-af", opt["eq"],
        final_wav
    ]
    subprocess.run(cmd_wav, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✓ Salvato in {final_mp3}")

async def main():
    for opt in OPTIONS:
        await generate_option(opt)
    print("\n✅ Tutti i provini vocali sono stati generati con successo!")

if __name__ == "__main__":
    asyncio.run(main())
