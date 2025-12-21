#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
ESEMPIO VELOCISSIMO - Come scrivere su e-ink in 10 righe

Questo è il modo più rapido per visualizzare qualcosa sul display!
"""

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from eink_widgets import *
from waveshare_epd import epd2in13_V4
import time

# Inizializza display
epd = epd2in13_V4.EPD()
epd.init()

# Crea canvas
canvas = EinkCanvas(epd.height, epd.width, picdir)

# Aggiungi widget (comodo e veloce!)
canvas.add_widget(Text(10, 10, "Ciao Mondo!", font_size='xlarge'))
canvas.add_widget(Text(10, 60, "Temperatura: 22°C", font_size='medium'))
canvas.add_widget(ProgressBar(10, 85, 150, 15, progress=75))
canvas.add_widget(NotchBar(200, 0, 12, 122, level=60, num_notches=5))

# Mostra!
epd.display(epd.getbuffer(canvas.get_image().rotate(180)))

# Pulizia
time.sleep(3)
epd.sleep()
epd2in13_V4.epdconfig.module_exit(cleanup=True)

print("Fatto! Facile vero? 😊")
