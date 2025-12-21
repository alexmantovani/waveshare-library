# E-ink Widgets Library

Libreria Python semplice e veloce per creare interfacce grafiche su display e-paper Waveshare.

Trasforma poche righe di codice in interfacce complete per i tuoi progetti IoT, domotica, stazioni meteo e dashboard.

## Caratteristiche

- **Facile da usare**: Crea interfacce in poche righe di codice
- **Widget pronti all'uso**: Text, Box, ProgressBar, NotchBar, SVG, DonutChart, SimpleGraph e altro
- **Layout helpers**: Disponi widget automaticamente con VerticalLayout e HorizontalLayout
- **Font personalizzati**: Supporto completo per font TTF/OTF (Lato, Roboto, ecc.)
- **Aggiornamento parziale**: Supporto per animazioni e aggiornamenti rapidi
- **Grafici e-ink friendly**: DonutChart con retinature, grafici a linee e visualizzazioni ottimizzate

## Quick Start

```python
from eink_widgets import *
from waveshare_epd import epd2in13_V4

# Inizializza display
epd = epd2in13_V4.EPD()
epd.init()

# Crea canvas
canvas = EinkCanvas(epd.height, epd.width)

# Aggiungi widget
canvas.add_widget(Text(10, 10, "Ciao!", font_size='xlarge'))
canvas.add_widget(Text(10, 60, "Temperatura: 22°C", font_size='medium'))
canvas.add_widget(ProgressBar(10, 85, 150, 15, progress=75))

# Mostra sul display
epd.display(epd.getbuffer(canvas.get_image().rotate(180)))
epd.sleep()
```

## Installazione

### Requisiti
```bash
pip install Pillow
pip install cairosvg
```

### Driver Waveshare
Scarica i driver dal repository ufficiale Waveshare:
```bash
git clone https://github.com/waveshareteam/e-Paper.git
# Copia la directory waveshare_epd nel tuo progetto
```

### Libreria Widget
Copia semplicemente `eink_widgets.py` nella tua directory di lavoro. Nessuna installazione necessaria!

## Widget Disponibili

### Text
Testo semplice con supporto font personalizzati
```python
Text(x, y, "Testo", font_size='medium', fill=0, anchor=None)
Text(x, y, "Custom", font='lato_large')  # Font personalizzato
```

### Box
Rettangoli e bordi
```python
Box(x, y, width, height, fill=255, outline=0, outline_width=1)
```

### StatusBox
Indicatori di stato ON/OFF
```python
StatusBox(x, y, width, height, "ON", is_active=True)
```

### ProgressBar
Barra di progresso orizzontale
```python
ProgressBar(x, y, width, height, progress=75, show_percentage=True)
```

### NotchBar
Barra verticale con tacche discrete (livelli)
```python
NotchBar(x, y, width, height, level=60, num_notches=5)
```

### SimpleGraph
Grafico a linee
```python
data = [10, 15, 12, 18, 20, 17, 22]
SimpleGraph(x, y, width, height, data, min_val=0, max_val=30)
```

### DonutChart
Grafico a ciambella con retinature per e-ink
```python
DonutChart(x, y, diameter, data=[35,25,20,20],
           labels=['CPU','MEM','DISK','NET'],
           use_patterns=True)
```

### SVG
Icone e grafica vettoriale
```python
svg_icon = '<svg>...</svg>'
SVG(x, y, svg_icon, size=(48, 48))
# Oppure da file
SVG(x, y, 'icon.svg', size=(48, 48), is_file=True)
```

### Line
Linee e separatori
```python
Line(x1, y1, x2, y2, fill=0, width=1)
```

## Layout Helpers

### VerticalLayout
Disponi widget verticalmente
```python
layout = VerticalLayout(x=10, y=10, spacing=15)
canvas.add_widget(layout.add(Text(0, 0, "Titolo"), height=25))
canvas.add_widget(layout.add(Text(0, 0, "Sottotitolo"), height=20))
```

### HorizontalLayout
Disponi widget orizzontalmente
```python
layout = HorizontalLayout(x=10, y=10, spacing=10)
canvas.add_widget(layout.add(Text(0, 0, "CPU:"), width=40))
canvas.add_widget(layout.add(ProgressBar(0, 0, 100, 15, 65), width=100))
```

## Font Personalizzati

### Carica famiglia di font
```python
canvas = EinkCanvas(width, height)
canvas.add_font_family('lato', 'path/to/Lato-Regular.ttf')

# Usa: lato_small, lato_medium, lato_large, lato_xlarge
canvas.add_widget(Text(10, 10, "Ciao!", font='lato_medium'))
```

### Carica singolo font
```python
canvas.add_custom_font('title', 'Lato-Bold.ttf', 28)
canvas.add_widget(Text(10, 10, "Titolo", font='title'))
```

Vedi [FONT_USAGE.md](FONT_USAGE.md) per la guida completa.

## Esempi

Il progetto include 7 esempi completi in `esempio_widgets.py`:

1. **Dashboard semplice** - Interfaccia base con vari widget
2. **Uso con Layout** - Layout automatici
3. **Grafico dati** - Visualizzazione temperatura 24h
4. **Aggiornamento parziale** - Animazioni e-ink
5. **Dashboard completa** - Layout a 3 colonne
6. **SVG e Donut Chart** - Grafici e icone vettoriali
7. **Font personalizzati** - Uso di Lato e altri font

```bash
python esempio_widgets.py
# Scegli l'esempio desiderato (1-7)
```

### Esempio Completo: Dashboard

```python
from eink_widgets import *
from waveshare_epd import epd2in13_V4
import time

epd = epd2in13_V4.EPD()
epd.init()

canvas = EinkCanvas(epd.height, epd.width)

# Header
canvas.add_widget(Text(10, 5, "Dashboard", font_size='large'))
canvas.add_widget(Text(160, 10, time.strftime("%H:%M"), font_size='medium'))

# Temperatura
canvas.add_widget(Text(10, 40, "22°", font_size='xlarge'))

# Progress bars
canvas.add_widget(Text(10, 85, "CPU:", font_size='small'))
canvas.add_widget(ProgressBar(45, 85, 100, 12, progress=65))

# Status
canvas.add_widget(Text(10, 103, "Sistema:", font_size='small'))
canvas.add_widget(StatusBox(60, 100, 50, 18, "ON", is_active=True))

# Barra livello laterale
canvas.add_widget(NotchBar(240, 0, 10, 122, level=80, num_notches=5))

# Mostra
epd.display(epd.getbuffer(canvas.get_image().rotate(180)))
epd.sleep()
```

### Esempio: Aggiornamento Parziale (Animazione)

```python
# Primo refresh completo
canvas = EinkCanvas(epd.height, epd.width)
canvas.add_widget(Text(10, 10, "Livello", font_size='large'))
rotated = canvas.get_image().rotate(180)
epd.display(epd.getbuffer(rotated))
epd.displayPartBaseImage(epd.getbuffer(rotated))

# Aggiornamenti parziali veloci
for level in range(0, 101, 10):
    canvas.clear()
    canvas.add_widget(Text(10, 10, "Livello", font_size='large'))
    canvas.add_widget(ProgressBar(10, 50, 150, 20, progress=level))
    canvas.add_widget(Text(10, 80, f"{level}%", font_size='xlarge'))

    rotated = canvas.get_image().rotate(180)
    epd.displayPartial(epd.getbuffer(rotated))
    time.sleep(0.2)
```

## Documentazione

- [README_WIDGETS.md](README_WIDGETS.md) - Guida completa ai widget
- [FONT_USAGE.md](FONT_USAGE.md) - Guida all'uso dei font personalizzati
- `quick_example.py` - Esempio veloce 10 righe
- `esempio_widgets.py` - 7 esempi interattivi completi

## Display Supportati

Testato con display Waveshare e-Paper:
- 2.13" V4 (250x122)
- Facilmente adattabile ad altri modelli Waveshare

Per altri display, modifica le dimensioni del canvas e la rotazione:
```python
canvas = EinkCanvas(your_width, your_height)
# Regola rotazione se necessario: rotate(0), rotate(90), rotate(180), rotate(270)
```

## Tips & Tricks

### Colori
- `0` = nero
- `255` = bianco

### Performance
- Usa `displayPartial()` per aggiornamenti rapidi (animazioni)
- Usa `display()` per il primo refresh o ogni ~100 aggiornamenti parziali
- Gli aggiornamenti parziali sono veloci ma possono causare ghosting

### Rotazione
Per display Waveshare 2.13" V4:
```python
epd.display(epd.getbuffer(canvas.get_image().rotate(180)))
```

## Progetti Consigliati

Questa libreria è perfetta per:
- Stazioni meteo
- Dashboard domotica
- Monitora sistema (CPU, RAM, temperatura)
- Display IoT
- Badge e-ink
- Calendari e to-do list
- Visualizzatori dati sensori

## Licenza

Codice libero da usare e modificare come preferisci!

## Contributi

Contributi, issue e feature request sono benvenuti!

## Credits

- Display e-Paper: [Waveshare](https://www.waveshare.com/)
- Font suggeriti: [Google Fonts](https://fonts.google.com/)
