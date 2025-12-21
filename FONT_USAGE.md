# Guida all'uso dei Font Personalizzati

La libreria `eink_widgets` supporta l'uso di font personalizzati in formato TTF/OTF.

## Installazione Font Lato

### Metodo 1: Script Automatico
```bash
python3 download_lato_font.py
```

### Metodo 2: Download Manuale
1. Visita https://fonts.google.com/specimen/Lato
2. Clicca "Download family"
3. Estrai i file `.ttf` nella cartella `pic/`

### Metodo 3: Installazione Sistema
**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install fonts-lato
# Font sarà in: /usr/share/fonts/truetype/lato/
```

**macOS:**
- Scarica e apri il file TTF
- Clicca "Installa Font" in Font Book

**Windows:**
- Scarica il file TTF
- Tasto destro → "Installa"
- Font sarà in: `C:\Windows\Fonts\`

## Utilizzo nel Codice

### Opzione 1: Carica Famiglia Completa
```python
from eink_widgets import EinkCanvas, Text

# Crea canvas
canvas = EinkCanvas(250, 122)

# Carica famiglia Lato (crea lato_small, lato_medium, lato_large, lato_xlarge)
canvas.add_font_family('lato', 'pic/Lato-Regular.ttf')

# Usa il font
canvas.add_widget(Text(10, 10, "Ciao Mondo!", font='lato_medium'))
canvas.add_widget(Text(10, 30, "Titolo Grande", font='lato_xlarge'))
```

### Opzione 2: Carica Font Singolo
```python
# Carica una dimensione specifica
canvas.add_custom_font('title', 'pic/Lato-Bold.ttf', 28)
canvas.add_custom_font('body', 'pic/Lato-Regular.ttf', 14)

# Usa i font
canvas.add_widget(Text(10, 10, "Titolo", font='title'))
canvas.add_widget(Text(10, 40, "Testo normale", font='body'))
```

### Opzione 3: Dimensioni Personalizzate
```python
# Definisci le tue dimensioni
custom_sizes = {
    'tiny': 8,
    'normal': 14,
    'big': 20,
    'huge': 32
}

canvas.add_font_family('lato', 'pic/Lato-Regular.ttf', sizes=custom_sizes)

# Usa: lato_tiny, lato_normal, lato_big, lato_huge
canvas.add_widget(Text(10, 10, "Enorme!", font='lato_huge'))
```

## Font Disponibili con Lato

Il font Lato include diverse varianti:
- **Lato-Regular.ttf** - Normale
- **Lato-Bold.ttf** - Grassetto
- **Lato-Italic.ttf** - Corsivo
- **Lato-Light.ttf** - Leggero
- **Lato-Black.ttf** - Nero (molto grassetto)

### Esempio con Varianti
```python
canvas.add_font_family('lato', 'pic/Lato-Regular.ttf')
canvas.add_font_family('lato_bold', 'pic/Lato-Bold.ttf')
canvas.add_font_family('lato_light', 'pic/Lato-Light.ttf')

canvas.add_widget(Text(10, 10, "Normale", font='lato_medium'))
canvas.add_widget(Text(10, 30, "Grassetto", font='lato_bold_medium'))
canvas.add_widget(Text(10, 50, "Leggero", font='lato_light_medium'))
```

## Altri Font Consigliati per E-ink

### Roboto (Google Fonts)
```python
canvas.add_font_family('roboto', 'pic/Roboto-Regular.ttf')
```
Download: https://fonts.google.com/specimen/Roboto

### Open Sans (Google Fonts)
```python
canvas.add_font_family('opensans', 'pic/OpenSans-Regular.ttf')
```
Download: https://fonts.google.com/specimen/Open+Sans

### Source Sans Pro (Adobe)
```python
canvas.add_font_family('sourcesans', 'pic/SourceSansPro-Regular.ttf')
```
Download: https://fonts.google.com/specimen/Source+Sans+Pro

### Font Monospazio (Codice)
```python
canvas.add_font_family('mono', 'pic/RobotoMono-Regular.ttf')
canvas.add_widget(Text(10, 10, "CPU: 45%", font='mono_small'))
```
Download: https://fonts.google.com/specimen/Roboto+Mono

## Widget che Supportano Font Personalizzati

Tutti i widget di testo supportano il parametro `font`:

```python
# Text
Text(x, y, "testo", font='lato_medium')

# StatusBox
StatusBox(x, y, w, h, "ON", font_size='small')  # usa font_size
# Per font custom, modifica il codice interno del widget

# ProgressBar
ProgressBar(x, y, w, h, 75, font_size='small')  # usa font_size

# DonutChart
DonutChart(x, y, diameter, data, font_size='small')  # usa font_size
```

## Risoluzione Problemi

### Font non caricato
```python
# Verifica percorso
import os
font_path = 'pic/Lato-Regular.ttf'
if os.path.exists(font_path):
    print("Font trovato!")
else:
    print(f"Font non trovato in: {os.path.abspath(font_path)}")
```

### Font sfocato/pixelato
- Usa dimensioni appropriate per il display (12-24px per display piccoli)
- Evita dimensioni troppo piccole (<10px) su display a bassa risoluzione

### Testo troppo grande
```python
# Regola le dimensioni
canvas.add_font_family('lato', 'pic/Lato-Regular.ttf',
                       sizes={'small': 10, 'medium': 14, 'large': 18})
```

## Esempio Completo

Vedi `esempio_widgets.py` → Esempio 7: Font personalizzati

```bash
python3 esempio_widgets.py
# Scegli opzione 7
```
