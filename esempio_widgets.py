#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Esempio di utilizzo della libreria eink_widgets
Mostra come creare un'interfaccia completa in poche righe
"""

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import time
from eink_widgets import *
from waveshare_epd import epd2in13_V4

# ============= ESEMPIO 1: Dashboard Semplice =============
def esempio_dashboard():
    """Esempio di dashboard con vari widget"""

    # Inizializza display
    epd = epd2in13_V4.EPD()
    epd.init()

    WIDTH = epd.height
    HEIGHT = epd.width

    # Crea canvas
    canvas = EinkCanvas(WIDTH, HEIGHT, picdir)

    # ===== HEADER: Titolo e data =====
    canvas.add_widget(Text(10, 5, "Dashboard", font_size='large', fill=0))
    canvas.add_widget(Text(160, 10, time.strftime("%H:%M"), font_size='medium'))

    # ===== ICONA SVG =====
    svg_sun = """
    <svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
      <circle cx="24" cy="24" r="10" fill="black"/>
      <line x1="24" y1="0" x2="24" y2="10" stroke="black" stroke-width="2"/>
      <line x1="24" y1="38" x2="24" y2="48" stroke="black" stroke-width="2"/>
      <line x1="0" y1="24" x2="10" y2="24" stroke="black" stroke-width="2"/>
      <line x1="38" y1="24" x2="48" y2="24" stroke="black" stroke-width="2"/>
    </svg>
    """
    canvas.add_widget(SVGIcon(15, 35, svg_sun, size=(40, 40)))

    # ===== TEMPERATURA =====
    canvas.add_widget(Text(70, 40, "22°", font_size='xlarge'))

    # ===== PROGRESS BAR =====
    canvas.add_widget(Text(10, 85, "CPU:", font_size='small'))
    canvas.add_widget(ProgressBar(45, 85, 100, 12, progress=65))

    # ===== STATUS BOX =====
    canvas.add_widget(Text(10, 103, "Pompa:", font_size='small'))
    canvas.add_widget(StatusBox(55, 100, 50, 18, "ON", is_active=True, font_size='small'))

    # ===== BARRA CON TACCHE (a destra) =====
    canvas.add_widget(NotchBar(WIDTH - 12, 0, 10, HEIGHT, level=60, num_notches=5))

    # Mostra su display
    rotated = canvas.get_image().rotate(180)
    epd.display(epd.getbuffer(rotated))

    time.sleep(2)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)


# ============= ESEMPIO 2: Uso con Layout =============
def esempio_layout():
    """Esempio usando layout helpers"""

    epd = epd2in13_V4.EPD()
    epd.init()

    WIDTH = epd.height
    HEIGHT = epd.width

    canvas = EinkCanvas(WIDTH, HEIGHT, picdir)

    # Layout verticale
    layout = VerticalLayout(10, 10, spacing=15)

    # Aggiungi elementi al layout
    canvas.add_widget(layout.add(Text(0, 0, "Sistema di Monitoraggio", font_size='large'), height=25))
    canvas.add_widget(layout.add(Text(0, 0, "Temperatura: 22.5°C", font_size='medium'), height=20))
    canvas.add_widget(layout.add(Text(0, 0, "Umidità: 65%", font_size='medium'), height=20))

    # Progress bar per umidità
    canvas.add_widget(ProgressBar(10, layout.current_y, 180, 15, progress=65, show_percentage=False))
    layout.current_y += 20

    # Status
    canvas.add_widget(layout.add(StatusBox(0, 0, 80, 22, "ONLINE", is_active=True), height=25))

    # Mostra
    rotated = canvas.get_image().rotate(180)
    epd.display(epd.getbuffer(rotated))

    time.sleep(2)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)


# ============= ESEMPIO 3: Grafico Dati =============
def esempio_grafico():
    """Esempio con grafico a linee"""

    epd = epd2in13_V4.EPD()
    epd.init()

    WIDTH = epd.height
    HEIGHT = epd.width

    canvas = EinkCanvas(WIDTH, HEIGHT, picdir)

    # Titolo
    canvas.add_widget(Text(10, 5, "Temperatura 24h", font_size='medium'))

    # Dati di esempio (temperature delle ultime 24 ore)
    temperature_data = [18, 17, 16, 15, 15, 16, 18, 20, 22, 24, 25, 26,
                       27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 18, 17]

    # Grafico
    canvas.add_widget(SimpleGraph(10, 30, 200, 70, temperature_data, min_val=10, max_val=30))

    # Valori attuali
    canvas.add_widget(Text(10, 105, f"Min: {min(temperature_data)}°", font_size='small'))
    canvas.add_widget(Text(80, 105, f"Max: {max(temperature_data)}°", font_size='small'))
    canvas.add_widget(Text(150, 105, f"Now: {temperature_data[-1]}°", font_size='small'))

    # Mostra
    rotated = canvas.get_image().rotate(180)
    epd.display(epd.getbuffer(rotated))

    time.sleep(2)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)


# ============= ESEMPIO 4: Aggiornamento Parziale =============
def esempio_aggiornamento_parziale():
    """Esempio con aggiornamento parziale per animazioni"""

    epd = epd2in13_V4.EPD()
    epd.init()

    WIDTH = epd.height
    HEIGHT = epd.width

    # Primo refresh completo
    canvas = EinkCanvas(WIDTH, HEIGHT, picdir)
    canvas.add_widget(Text(10, 10, "Livello Acqua", font_size='large'))
    canvas.add_widget(Text(10, 35, "Monitoraggio in tempo reale", font_size='small'))

    rotated = canvas.get_image().rotate(180)
    epd.display(epd.getbuffer(rotated))
    epd.displayPartBaseImage(epd.getbuffer(rotated))

    # Aggiornamenti parziali
    for level in range(0, 101, 10):
        canvas.clear()

        canvas.add_widget(Text(10, 10, "Livello Acqua", font_size='large'))
        canvas.add_widget(Text(10, 35, "Monitoraggio in tempo reale", font_size='small'))

        # Barra progressiva
        canvas.add_widget(NotchBar(10, 60, 15, 50, level=level, num_notches=5))
        canvas.add_widget(Text(35, 85, f"{level}%", font_size='xlarge'))

        # Progress bar orizzontale
        canvas.add_widget(ProgressBar(10, 100, 150, 15, progress=level))

        rotated = canvas.get_image().rotate(180)
        epd.displayPartial(epd.getbuffer(rotated))
        time.sleep(0.5)

    time.sleep(2)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)


# ============= ESEMPIO 5: Mini Dashboard con Tutto =============
def esempio_completo():
    """Dashboard completa con tutti i widget disponibili"""

    epd = epd2in13_V4.EPD()
    epd.init()

    WIDTH = epd.height
    HEIGHT = epd.width

    canvas = EinkCanvas(WIDTH, HEIGHT, picdir)

    # Layout a 3 colonne

    # COLONNA 1: Info generali
    canvas.add_widget(Text(5, 5, time.strftime("%d/%m"), font_size='small'))
    canvas.add_widget(Text(5, 20, time.strftime("%H:%M"), font_size='medium'))
    canvas.add_widget(Text(5, 45, "22°", font_size='large'))

    # Separatore verticale
    canvas.add_widget(Line(60, 0, 60, HEIGHT, fill=0, width=1))

    # COLONNA 2: Status e progress
    canvas.add_widget(Text(70, 5, "Sistema", font_size='small'))
    canvas.add_widget(StatusBox(70, 20, 60, 18, "ONLINE", is_active=True, font_size='small'))

    canvas.add_widget(Text(70, 45, "CPU", font_size='small'))
    canvas.add_widget(ProgressBar(70, 60, 80, 10, progress=45, show_percentage=False))

    canvas.add_widget(Text(70, 75, "MEM", font_size='small'))
    canvas.add_widget(ProgressBar(70, 90, 80, 10, progress=72, show_percentage=False))

    # Separatore verticale
    canvas.add_widget(Line(165, 0, 165, HEIGHT, fill=0, width=1))

    # COLONNA 3: Grafico mini
    mini_data = [20, 25, 22, 28, 30, 27, 25]
    canvas.add_widget(Text(175, 5, "7d", font_size='small'))
    canvas.add_widget(SimpleGraph(175, 20, 60, 40, mini_data, min_val=15, max_val=35))

    # Barra tacche in basso
    canvas.add_widget(Text(175, 70, "H2O", font_size='small'))
    canvas.add_widget(NotchBar(185, 85, 10, 30, level=80, num_notches=5, spacing=2))

    # Mostra
    rotated = canvas.get_image().rotate(180)
    epd.display(epd.getbuffer(rotated))

    time.sleep(3)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)


# ============= ESEMPIO 6: SVG e Donut Chart =============
def esempio_svg_donut():
    """Esempio con widget SVG e grafico Donut"""

    epd = epd2in13_V4.EPD()
    epd.init()

    WIDTH = epd.height
    HEIGHT = epd.width

    canvas = EinkCanvas(WIDTH, HEIGHT, picdir)

    # Titolo
    canvas.add_widget(Text(10, 5, "SVG & Donut Charts", font_size='medium'))

    # ===== ESEMPIO SVG DA STRINGA =====
    # Icona cuore SVG
    svg_heart = """
    <svg width="40" height="40" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
            fill="black"/>
    </svg>
    """
    canvas.add_widget(SVG(15, 25, svg_heart, size=(30, 30)))

    # ===== ESEMPIO DONUT CHART CON RETINATURE =====
    # Dati di esempio: distribuzione risorse
    data_usage = [35, 25, 20, 20]  # CPU, MEM, DISK, NET
    labels = ['CPU', 'MEM', 'DISK', 'NET']

    canvas.add_widget(DonutChart(
        x=120,  # centro X
        y=60,  # centro Y
        diameter=70,
        data=data_usage,
        labels=labels,
        hole_ratio=0.4,
        show_labels=True,
        font_size='small',
        use_patterns=True  # Usa retinature per distinguere i settori
    ))

    # Titolo sotto il grafico
    canvas.add_widget(Text(120, 105, "Risorse", font_size='small', anchor='mm'))

    # ===== SECONDO SVG: Icona stella =====
    svg_star = """
    <svg width="30" height="30" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
            fill="black"/>
    </svg>
    """
    canvas.add_widget(SVG(170, 25, svg_star, size=(25, 25)))

    # Info aggiuntiva
    canvas.add_widget(Text(145, 105, "Rating: 5/5", font_size='small'))

    # Mostra
    rotated = canvas.get_image().rotate(180)
    epd.display(epd.getbuffer(rotated))

    time.sleep(3)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)


# ============= ESEMPIO 7: Font Personalizzati =============
def esempio_font_personalizzati():
    """Esempio con font personalizzati (es. Lato)"""

    epd = epd2in13_V4.EPD()
    epd.init()

    WIDTH = epd.height
    HEIGHT = epd.width

    canvas = EinkCanvas(WIDTH, HEIGHT, picdir)

    # ===== CARICA FONT PERSONALIZZATO =====
    # Opzione 1: Carica singolo font con dimensione specifica
    # canvas.add_custom_font('lato_title', '/path/to/Lato-Bold.ttf', 20)

    # Opzione 2: Carica famiglia di font (consigliato)
    # Cerca il font Lato nel sistema
    lato_paths = [
        '/usr/share/fonts/truetype/lato/Lato-Regular.ttf',  # Linux
        '/System/Library/Fonts/Supplemental/Lato-Regular.ttf',  # macOS
        'C:\\Windows\\Fonts\\Lato-Regular.ttf',  # Windows
        os.path.join(picdir, 'Lato-Regular.ttf'),  # Directory locale
    ]

    lato_found = False
    for path in lato_paths:
        if os.path.exists(path):
            canvas.add_font_family('lato', path)
            lato_found = True
            print(f"Font Lato caricato da: {path}")
            break

    if not lato_found:
        print("Font Lato non trovato. Usando font di default.")
        print("Scarica Lato da: https://fonts.google.com/specimen/Lato")
        print(f"E salvalo in: {os.path.join(picdir, 'Lato-Regular.ttf')}")

    # ===== TITOLO CON FONT PERSONALIZZATO =====
    if lato_found:
        canvas.add_widget(Text(10, 5, "Custom Fonts", font='lato_large'))
        canvas.add_widget(Text(10, 35, "Questo testo usa Lato Regular", font='lato_medium'))
        canvas.add_widget(Text(10, 55, "Font dimensione small", font='lato_small'))
        canvas.add_widget(Text(10, 75, "Font LARGE", font='lato_xlarge'))
    else:
        canvas.add_widget(Text(10, 5, "Custom Fonts", font_size='large'))
        canvas.add_widget(Text(10, 35, "Font Lato non trovato", font_size='medium'))
        canvas.add_widget(Text(10, 55, "Usando font di default", font_size='small'))

    # ===== CONFRONTO CON FONT DEFAULT =====
    canvas.add_widget(Text(10, 100, "Default font:", font_size='small'))

    # Mostra
    rotated = canvas.get_image().rotate(180)
    epd.display(epd.getbuffer(rotated))

    time.sleep(3)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)


# ============= MENU DI SCELTA =============
if __name__ == "__main__":
    print("\n=== Esempi Widget E-ink ===")
    print("1. Dashboard semplice")
    print("2. Uso con Layout")
    print("3. Grafico dati")
    print("4. Aggiornamento parziale (animazione)")
    print("5. Dashboard completa")
    print("6. SVG e Donut Chart")
    print("7. Font personalizzati (Lato)")
    print("\nPremi CTRL+C per uscire")

    try:
        scelta = input("\nScegli esempio (1-7): ")

        if scelta == "1":
            print("Eseguo esempio 1: Dashboard semplice...")
            esempio_dashboard()
        elif scelta == "2":
            print("Eseguo esempio 2: Layout...")
            esempio_layout()
        elif scelta == "3":
            print("Eseguo esempio 3: Grafico...")
            esempio_grafico()
        elif scelta == "4":
            print("Eseguo esempio 4: Animazione...")
            esempio_aggiornamento_parziale()
        elif scelta == "5":
            print("Eseguo esempio 5: Dashboard completa...")
            esempio_completo()
        elif scelta == "6":
            print("Eseguo esempio 6: SVG e Donut Chart...")
            esempio_svg_donut()
        elif scelta == "7":
            print("Eseguo esempio 7: Font personalizzati...")
            esempio_font_personalizzati()
        else:
            print("Scelta non valida!")

    except KeyboardInterrupt:
        print("\nUscita...")
        epd2in13_V4.epdconfig.module_exit(cleanup=True)
