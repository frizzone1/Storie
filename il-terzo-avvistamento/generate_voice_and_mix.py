#!/usr/bin/env python3
"""
Generazione Voce Narrante del Protagonista (AI Neural Voice Maschile)
e Mixaggio con la Colonna Sonora Sound Design per 'Il Terzo Avvistamento'.
Crea il master audio completo a 44.1 kHz: assets/master_soundtrack_72s.wav
"""

import os
import asyncio
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal
import edge_tts
import openshot
import ctypes

BASE_DIR = "/media/corrado/DATI/REPO_GH/Progetto_pers/Storie/il-terzo-avvistamento"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
VOICE_DIR = os.path.join(ASSETS_DIR, "voice_clips")
SOUNDTRACK_FILE = os.path.join(ASSETS_DIR, "soundtrack_72s.wav")
MASTER_OUTPUT = os.path.join(ASSETS_DIR, "master_soundtrack_72s.wav")

SR = 44100
DURATION = 72.0
TOTAL_SAMPLES = int(SR * DURATION)

CAPTIONS_VOICE = [
    ("01", 0.1, "Le probabilità di incontrare lo stesso sconosciuto..."),
    ("02", 3.2, "in tre città diverse... sono zero."),
    ("03", 6.1, "La prima volta: Milano. Nebbia fitta."),
    ("04", 9.8, "Nella calca, un ragazzo mi urta. Occhi vitrei, cappotto nero."),
    ("05", 14.8, "Non chiede scusa. Scompare nel nulla tra la folla."),
    ("06", 18.6, "Due anni dopo. Roma, vicoli deserti alle tre di notte."),
    ("07", 23.0, "Sento dei passi. Accelero... l'ombra accelera."),
    ("08", 27.0, "Sotto un lampione: era lui. Non era invecchiato di un giorno."),
    ("09", 31.0, "Ha sorriso e mi ha sussurrato: la data di oggi."),
    ("10", 34.2, "Oggi. Napoli, Castel dell'Ovo. Davanti al mare."),
    ("11", 39.0, "Pensavo di essere al sicuro... poi, quel gelo sulla nuca."),
    ("12", 43.2, "E un silenzio anomalo: il mare si spegne di colpo."),
    ("13", 48.2, "Sulla panchina c'è un telefono. Accanto, quel cappotto."),
    ("14", 52.5, "Chiamata in arrivo da: mio stesso numero."),
    ("15", 56.5, "Una mano gelida sulla spalla. Ho trattenuto il respiro."),
    ("16", 60.2, "Te l'avevo detto che era oggi."),
    ("17", 63.8, "Nel riflesso nero ho visto la mia faccia..."),
    ("18", 67.8, "Ma i miei occhi... erano diventati i suoi.")
]

def mix_master():
    from create_master_audio import main as run_mix
    run_mix()

if __name__ == "__main__":
    mix_master()
