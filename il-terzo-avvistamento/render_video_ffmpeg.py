#!/usr/bin/env python3
"""
Render definitivo Full HD 1080x1920 (9:16) per 'Il Terzo Avvistamento'
Genera il video MP4 tramite FFmpeg statico e Pillow:
- 1080x1920 a 30 FPS (72.0s = 2160 fotogrammi esatti)
- Animazioni Ken Burns e movimenti di camera dedicati per ogni scena
- Sottotitoli cinetici impressi (burned-in) con pill scura ad alta leggibilità
- Audio master HD: SOLO VOCE NARRANTE (Zero musica, Zero rumori, Zero sovrapposizioni)
- Muxing H.264 High Profile + AAC 192kbps con flag faststart per riproduzione immediata
"""

import os
import sys
import subprocess
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/media/corrado/DATI/REPO_GH/Progetto_pers/Storie/il-terzo-avvistamento"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_FILE = os.path.join(ASSETS_DIR, "master_soundtrack_72s.wav")
OUTPUT_FILE = os.path.join(BASE_DIR, "il_terzo_avvistamento_9x16.mp4")
FFMPEG_BIN = "/tmp/ffmpeg" if os.path.exists("/tmp/ffmpeg") else "ffmpeg"

WIDTH = 1080
HEIGHT = 1920
FPS = 30
TOTAL_DURATION = 72.0
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

SCENES = [
    {
        "id": 1,
        "name": "Il Gancio",
        "start": 0.0,
        "end": 6.5,
        "file": "01_gancio_occhio.jpg",
        "scale_start": 1.15,
        "scale_end": 1.04,
        "pan_y": 0.0,
        "type": "eye"
    },
    {
        "id": 2,
        "name": "Milano",
        "start": 6.5,
        "end": 19.8,
        "file": "02_milano_stazione.jpg",
        "scale_start": 1.02,
        "scale_end": 1.16,
        "pan_y": -0.04,
        "type": "walk"
    },
    {
        "id": 3,
        "name": "Roma",
        "start": 19.8,
        "end": 37.4,
        "file": "03_roma_vicolo.jpg",
        "scale_start": 1.03,
        "scale_end": 1.18,
        "pan_y": -0.06,
        "type": "dark"
    },
    {
        "id": 4,
        "name": "Napoli - Il Mare",
        "start": 37.4,
        "end": 50.7,
        "file": "04_napoli_mare_castel.jpg",
        "scale_start": 1.03,
        "scale_end": 1.15,
        "pan_y": 0.03,
        "type": "sea"
    },
    {
        "id": 5,
        "name": "La Panchina",
        "start": 50.7,
        "end": 62.8,
        "file": "05_napoli_panchina_telefono.jpg",
        "scale_start": 1.02,
        "scale_end": 1.18,
        "pan_y": 0.05,
        "type": "bench"
    },
    {
        "id": 6,
        "name": "Il Climax",
        "start": 62.8,
        "end": 72.0,
        "file": "06_climax_riflesso.jpg",
        "scale_start": 1.04,
        "scale_end": 1.25,
        "pan_y": 0.03,
        "type": "climax"
    }
]

CAPTIONS = [
    {"start": 0.2, "end": 3.5, "text": "Le probabilità di incontrare\nlo stesso sconosciuto...", "color": "#FFFFFF"},
    {"start": 3.6, "end": 6.4, "text": "in tre città diverse...\nsono zero.", "color": "#FFE600"},
    {"start": 6.5, "end": 10.2, "text": "La prima volta: Milano.\nNebbia fitta.", "color": "#00E5FF"},
    {"start": 10.3, "end": 15.7, "text": "Nella calca, un ragazzo mi urta.\nOcchi vitrei, cappotto nero.", "color": "#FFE600"},
    {"start": 15.8, "end": 19.8, "text": "Non chiede scusa.\nScompare nel nulla tra la folla.", "color": "#FFFFFF"},
    {"start": 19.9, "end": 24.7, "text": "Due anni dopo. Roma,\nvicoli deserti alle tre di notte.", "color": "#00E5FF"},
    {"start": 24.8, "end": 29.0, "text": "Sento dei passi.\nAccelero... l'ombra accelera.", "color": "#FFE600"},
    {"start": 29.1, "end": 33.9, "text": "Sotto un lampione: era lui.\nNon era invecchiato di un giorno.", "color": "#FFE600"},
    {"start": 34.0, "end": 37.3, "text": "Ha sorriso e mi ha sussurrato:\nla data di oggi.", "color": "#FF3366"},
    {"start": 37.4, "end": 42.6, "text": "Oggi. Napoli, Castel dell'Ovo.\nDavanti al mare.", "color": "#00E5FF"},
    {"start": 42.7, "end": 46.9, "text": "Pensavo di essere al sicuro...\npoi, quel gelo sulla nuca.", "color": "#FFE600"},
    {"start": 47.0, "end": 50.6, "text": "E un silenzio anomalo:\nil mare si spegne di colpo.", "color": "#00E5FF"},
    {"start": 50.7, "end": 55.3, "text": "Sulla panchina c'è un telefono.\nAccanto, quel cappotto.", "color": "#FFE600"},
    {"start": 55.4, "end": 58.3, "text": "Chiamata in arrivo da:\nMIO STESSO NUMERO.", "color": "#FF3366"},
    {"start": 58.4, "end": 62.7, "text": "Una mano gelida sulla spalla.\nHo trattenuto il respiro.", "color": "#FF3366"},
    {"start": 62.8, "end": 64.6, "text": "'Te l'avevo detto che era oggi.'", "color": "#FFE600"},
    {"start": 64.7, "end": 67.4, "text": "Nel riflesso nero ho visto la mia faccia...", "color": "#FFFFFF"},
    {"start": 67.5, "end": 70.5, "text": "Ma i miei occhi...\nerano diventati i suoi.", "color": "#FF3366"},
]

def create_caption_overlay(caption, font):
    """Crea un overlay RGBA 1080x1920 con il sottotitolo impresso su pill scura"""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    if not caption:
        return overlay

    draw = ImageDraw.Draw(overlay)
    lines = caption["text"].split("\n")
    line_h = 72
    box_y = int(HEIGHT * 0.76)
    start_y = box_y - ((len(lines) - 1) * line_h) // 2

    for i, line in enumerate(lines):
        y_pos = start_y + i * line_h
        bbox = font.getbbox(line)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x_pos = (WIDTH - tw) // 2

        pad_x, pad_y = 32, 12
        rect = [x_pos - pad_x, y_pos - pad_y, x_pos + tw + pad_x, y_pos + th + pad_y + 8]
        draw.rounded_rectangle(rect, radius=18, fill=(10, 12, 18, 225))
        draw.text((x_pos, y_pos), line, font=font, fill=caption.get("color", "#FFFFFF"))

    return overlay

def create_vignette():
    """Crea una vignettatura cinematografica radiale 35mm"""
    vignette = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vignette)
    cx, cy = WIDTH // 2, HEIGHT // 2
    r_max = int(np.sqrt(cx**2 + cy**2))
    for r in range(int(WIDTH * 0.35), r_max, 16):
        alpha = int(min(175, 175 * ((r - WIDTH * 0.35) / (r_max - WIDTH * 0.35)) ** 1.6))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 0, 0, alpha), width=18)
    return vignette

def main():
    print("🎬 AVVIO RENDERING PROFESSIONALE 1080x1920 'IL TERZO AVVISTAMENTO'")
    print(f"📐 Risoluzione: {WIDTH}x{HEIGHT} (Full HD Verticale 9:16) | FPS: {FPS}")
    print(f"🎙️ Audio Master: {AUDIO_FILE} (SOLO VOCE, Zero Overlap, Zero Distorsione)")
    print(f"📁 Output Video: {OUTPUT_FILE}")

    # 1. Carica le 6 immagini di base
    base_images = {}
    for s in SCENES:
        img_p = os.path.join(ASSETS_DIR, s["file"])
        img = Image.open(img_p).convert("RGB")
        base_images[s["id"]] = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
    print("  ✓ Tutte le 6 scene caricate e scalate a 1080x1920")

    # 2. Prepara font e overlay
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 52)

    caption_overlays = [create_caption_overlay(c, font) for c in CAPTIONS]
    vignette_overlay = create_vignette()
    print("  ✓ Overlay sottotitoli cinetici e vignettatura generati")

    # 3. Avvia processo FFmpeg con pipe stdin
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_FILE,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        OUTPUT_FILE
    ]

    print(f"\n🚀 Avvio codifica FFmpeg H.264 / AAC...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    t0 = time.time()
    for frame_idx in range(TOTAL_FRAMES):
        t_sec = frame_idx / float(FPS)

        # Trova scena attiva
        scene = next((s for s in SCENES if t_sec >= s["start"] and t_sec < s["end"]), SCENES[-1])
        base_img = base_images[scene["id"]]
        progress = (t_sec - scene["start"]) / (scene["end"] - scene["start"])

        # Ken Burns zoom & camera motion
        scale = scene["scale_start"] + (scene["scale_end"] - scene["scale_start"]) * progress
        # Micro respiro organico della camera
        pan_x = np.sin(t_sec * 0.8) * 8.0
        pan_y = (scene["pan_y"] * HEIGHT * progress) + np.cos(t_sec * 0.6) * 6.0

        if scene["type"] == "eye":
            pan_x += np.sin(t_sec * 32.0) * 3.0
            scale += np.sin(t_sec * 2.8) * 0.015
        elif scene["type"] == "walk":
            pan_x += np.sin(t_sec * 4.5) * 6.0
            pan_y += abs(np.sin(t_sec * 4.5)) * 8.0
        elif scene["type"] == "sea":
            pan_y += np.sin(t_sec * 1.6) * 12.0
            scale += np.sin(t_sec * 1.2) * 0.012

        # Applica trasformazione ritaglio centrato
        scaled_w = int(WIDTH * scale)
        scaled_h = int(HEIGHT * scale)
        scaled_img = base_img.resize((scaled_w, scaled_h), Image.BILINEAR)

        crop_x = int((scaled_w - WIDTH) / 2.0 - pan_x)
        crop_y = int((scaled_h - HEIGHT) / 2.0 - pan_y)
        crop_x = max(0, min(scaled_w - WIDTH, crop_x))
        crop_y = max(0, min(scaled_h - HEIGHT, crop_y))

        frame = scaled_img.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

        # Desaturazione per la scena della panchina
        if scene["id"] == 5:
            desat = min(80, int(progress * 80))
            if desat > 0:
                gray = frame.convert("L").convert("RGB")
                frame = Image.blend(frame, gray, desat / 100.0)

        # Applica vignettatura
        frame.paste(vignette_overlay, (0, 0), vignette_overlay)

        # Applica sottotitolo attivo se presente
        cap_idx = next((i for i, c in enumerate(CAPTIONS) if t_sec >= c["start"] and t_sec < c["end"]), None)
        if cap_idx is not None:
            overlay = caption_overlays[cap_idx]
            frame.paste(overlay, (0, 0), overlay)

        # Scrive il frame su FFmpeg
        proc.stdin.write(frame.tobytes())

        if frame_idx % 150 == 0 or frame_idx == TOTAL_FRAMES - 1:
            pct = int((frame_idx + 1) / TOTAL_FRAMES * 100)
            elapsed = time.time() - t0
            fps_speed = (frame_idx + 1) / max(0.1, elapsed)
            print(f"  ⏳ Progresso: {pct:3d}% ({frame_idx+1}/{TOTAL_FRAMES} fotogrammi | {fps_speed:.1f} fps)")

    proc.stdin.close()
    proc.wait()

    if proc.returncode != 0:
        err = proc.stderr.read().decode("utf-8", errors="ignore")
        print(f"❌ Errore rendering FFmpeg:\n{err}")
        sys.exit(1)

    elapsed_total = time.time() - t0
    out_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\n🎉 RENDERING COMPLETATO IN {elapsed_total:.1f}s!")
    print(f"📁 Video: {OUTPUT_FILE}")
    print(f"⚖️ Dimensione: {out_size_mb:.2f} MB")

if __name__ == "__main__":
    main()
