#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Script helper per scaricare il font Lato da Google Fonts
"""

import os
import urllib.request
import zipfile
import shutil

def download_lato_font():
    """Scarica e installa il font Lato nella directory pic"""

    # Directory di destinazione
    script_dir = os.path.dirname(os.path.realpath(__file__))
    pic_dir = os.path.join(script_dir, 'pic')

    if not os.path.exists(pic_dir):
        os.makedirs(pic_dir)

    # URL del font Lato da Google Fonts
    url = "https://fonts.google.com/download?family=Lato"
    zip_path = os.path.join(pic_dir, 'Lato.zip')

    print("Downloading Lato font from Google Fonts...")
    print(f"URL: {url}")

    try:
        # Scarica il file ZIP
        urllib.request.urlretrieve(url, zip_path)
        print(f"Downloaded to: {zip_path}")

        # Estrai il contenuto
        print("Extracting font files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(pic_dir)

        # Cerca i file TTF
        ttf_files = []
        for root, dirs, files in os.walk(pic_dir):
            for file in files:
                if file.endswith('.ttf'):
                    ttf_files.append(os.path.join(root, file))

        print(f"\nFont files extracted:")
        for ttf in ttf_files:
            print(f"  - {os.path.basename(ttf)}")

        # Pulisci il file ZIP
        os.remove(zip_path)

        print(f"\nFont Lato installato con successo in: {pic_dir}")
        print("\nVarianti disponibili:")
        print("  - Lato-Regular.ttf (normale)")
        print("  - Lato-Bold.ttf (grassetto)")
        print("  - Lato-Italic.ttf (corsivo)")
        print("  - Lato-Light.ttf (leggero)")
        print("\nOra puoi usare il font nei tuoi widget!")
        print("\nEsempio:")
        print("  canvas.add_font_family('lato', 'pic/Lato-Regular.ttf')")
        print("  canvas.add_widget(Text(10, 10, 'Ciao', font='lato_medium'))")

        return True

    except Exception as e:
        print(f"\nErrore durante il download: {e}")
        print("\nAlternativa: scarica manualmente da:")
        print("  https://fonts.google.com/specimen/Lato")
        print(f"E salva Lato-Regular.ttf in: {pic_dir}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Download Font Lato per E-ink Widgets")
    print("=" * 60)
    print()

    download_lato_font()
