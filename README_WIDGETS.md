# E-ink Widgets Library

Libreria Python per creare interfacce grafiche su display e-paper in modo veloce e semplice.

## Installazione

Nessuna installazione necessaria! Basta copiare `eink_widgets.py` nella tua directory di lavoro.

Dipendenze:
- PIL/Pillow
- cairosvg (per icone SVG)
- waveshare_epd (driver display)

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
canvas.add_widget(ProgressBar(10, 60, 150, 20, progress=75))

# Mostra
epd.display(epd.getbuffer(canvas.get_image().rotate(180)))
```

## Widget Disponibili

### Text
Testo semplice

```python
Text(x, y, "Testo", font_size='medium', fill=0, anchor=None)
```

**Font sizes:** `'small'`, `'medium'`, `'large'`, `'xlarge'`

### Box
Rettangolo/Box

```python
Box(x, y, width, height, fill=255, outline=0, outline_width=1)
```

### StatusBox
Box con testo per indicatori di stato

```python
StatusBox(x, y, width, height, "ON", is_active=True)
```

### NotchBar
Barra verticale con tacche discrete (tipo indicatore livello)

```python
NotchBar(x, y, width, height, level=60, num_notches=5, spacing=3)
```

**Parametri:**
- `level`: 0-100 (percentuale)
- `num_notches`: numero di tacche
- `spacing`: spazio tra le tacche in pixel

### ProgressBar
Barra di progresso orizzontale

```python
ProgressBar(x, y, width, height, progress=50, show_percentage=True)
```

### SimpleGraph
Grafico a linee semplice

```python
data = [10, 15, 12, 18, 20, 17, 22]
SimpleGraph(x, y, width, height, data, min_val=0, max_val=30)
```

### SVGIcon
Icone SVG

```python
svg = '<svg>...</svg>'
SVGIcon(x, y, svg, size=(48, 48))
```

### Line
Linea semplice

```python
Line(x1, y1, x2, y2, fill=0, width=1)
```

## Layout Helpers

Per disporre widget automaticamente:

### VerticalLayout

```python
layout = VerticalLayout(x=10, y=10, spacing=15)

canvas.add_widget(layout.add(Text(0, 0, "Titolo"), height=25))
canvas.add_widget(layout.add(Text(0, 0, "Sottotitolo"), height=20))
canvas.add_widget(layout.add(StatusBox(0, 0, 60, 20, "ON", True), height=25))
```

### HorizontalLayout

```python
layout = HorizontalLayout(x=10, y=10, spacing=10)

canvas.add_widget(layout.add(Text(0, 0, "CPU:"), width=40))
canvas.add_widget(layout.add(ProgressBar(0, 0, 100, 15, 65), width=100))
```

## Esempi Completi

### Dashboard Semplice

```python
canvas = EinkCanvas(250, 122)

canvas.add_widget(Text(10, 5, "Dashboard", font_size='large'))
canvas.add_widget(Text(10, 35, "22°C", font_size='xlarge'))
canvas.add_widget(ProgressBar(10, 80, 150, 15, progress=65))
canvas.add_widget(NotchBar(200, 0, 12, 122, level=80, num_notches=5))

epd.display(epd.getbuffer(canvas.get_image().rotate(180)))
```

### Aggiornamento Parziale

Per animazioni o aggiornamenti rapidi:

```python
# Prima volta: full refresh
rotated = canvas.get_image().rotate(180)
epd.display(epd.getbuffer(rotated))
epd.displayPartBaseImage(epd.getbuffer(rotated))

# Aggiornamenti successivi: partial refresh
for i in range(100):
    canvas.clear()
    canvas.add_widget(Text(10, 10, f"Valore: {i}"))
    canvas.add_widget(ProgressBar(10, 40, 150, 20, progress=i))

    rotated = canvas.get_image().rotate(180)
    epd.displayPartial(epd.getbuffer(rotated))
    time.sleep(0.1)
```

### Grafico Temperatura

```python
canvas = EinkCanvas(250, 122)

# Dati temperatura 24h
temp_data = [18, 17, 16, 15, 16, 18, 20, 22, 24, 25, 26, 27,
             26, 25, 24, 23, 22, 21, 20, 19, 18, 18, 17, 16]

canvas.add_widget(Text(10, 5, "Temperatura 24h", font_size='medium'))
canvas.add_widget(SimpleGraph(10, 30, 200, 70, temp_data, min_val=10, max_val=30))
canvas.add_widget(Text(10, 105, f"Attuale: {temp_data[-1]}°C", font_size='small'))

epd.display(epd.getbuffer(canvas.get_image().rotate(180)))
```

## Files di Esempio

- `quick_example.py` - Esempio velocissimo (10 righe)
- `esempio_widgets.py` - 5 esempi completi interattivi:
  1. Dashboard semplice
  2. Uso con Layout
  3. Grafico dati
  4. Aggiornamento parziale (animazione)
  5. Dashboard completa

Esegui:
```bash
python quick_example.py
# oppure
python esempio_widgets.py
```

## Tips & Tricks

### Colori
- `0` = nero
- `255` = bianco

### Rotazione Display
Per Waveshare 2.13" V4, usa `rotate(180)` prima di mostrare:
```python
epd.display(epd.getbuffer(canvas.get_image().rotate(180)))
```

### Performance
- Usa `displayPartial()` per aggiornamenti rapidi
- Usa `display()` solo per il primo refresh o ogni ~100 aggiornamenti parziali
- Gli aggiornamenti parziali sono molto più veloci ma possono causare ghosting

### Font Personalizzati
Puoi caricare font personalizzati:
```python
canvas = EinkCanvas(width, height, picdir="/path/to/fonts")
# Oppure modifica direttamente:
canvas.fonts['custom'] = ImageFont.truetype('/path/to/font.ttf', 20)
```

## API Reference

### EinkCanvas

```python
canvas = EinkCanvas(width, height, picdir=None)
canvas.clear(color=255)              # Pulisce il canvas
canvas.add_widget(widget)            # Aggiunge un widget
canvas.get_image()                   # Restituisce immagine PIL
```

### Font disponibili
- `canvas.fonts['small']` - 12pt
- `canvas.fonts['medium']` - 16pt
- `canvas.fonts['large']` - 24pt
- `canvas.fonts['xlarge']` - 48pt

## Licenza

Codice libero da usare e modificare come preferisci!
