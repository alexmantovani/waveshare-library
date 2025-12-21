#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Libreria di widget per display e-ink
Componenti riutilizzabili per creare interfacce grafiche su display e-paper
"""

from PIL import Image, ImageDraw, ImageFont
import os
import io
import math
import cairosvg


class EinkCanvas:
    """Canvas base per disegnare su display e-ink"""

    def __init__(self, width, height, picdir=None):
        """
        Args:
            width: larghezza del canvas
            height: altezza del canvas
            picdir: directory con font e risorse
        """
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.picdir = picdir or os.path.join(os.path.dirname(__file__), 'pic')

        # Font di default
        self._load_fonts()

    def _load_fonts(self):
        """Carica i font di default"""
        font_path = os.path.join(self.picdir, 'Font.ttc')
        try:
            self.fonts = {
                'small': ImageFont.truetype(font_path, 14),
                'medium': ImageFont.truetype(font_path, 18),
                'large': ImageFont.truetype(font_path, 24),
                'xlarge': ImageFont.truetype(font_path, 48)
            }
        except:
            # Fallback a font di default se Font.ttc non esiste
            self.fonts = {
                'small': ImageFont.load_default(),
                'medium': ImageFont.load_default(),
                'large': ImageFont.load_default(),
                'xlarge': ImageFont.load_default()
            }

    def add_custom_font(self, name, font_path, size):
        """
        Aggiunge un font personalizzato

        Args:
            name: nome del font (es. 'lato_small', 'custom_title')
            font_path: percorso al file TTF
            size: dimensione del font in pixel

        Example:
            canvas.add_custom_font('lato_medium', '/path/to/Lato-Regular.ttf', 16)
            canvas.add_widget(Text(10, 10, "Ciao", font='lato_medium'))
        """
        try:
            self.fonts[name] = ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"Errore nel caricamento del font {font_path}: {e}")
            self.fonts[name] = self.fonts.get('medium', ImageFont.load_default())

    def add_font_family(self, family_name, font_path, sizes=None):
        """
        Aggiunge una famiglia di font con diverse dimensioni

        Args:
            family_name: prefisso per i nomi dei font (es. 'lato')
            font_path: percorso al file TTF
            sizes: dizionario {suffix: size} (default: standard small/medium/large/xlarge)

        Example:
            canvas.add_font_family('lato', '/path/to/Lato-Regular.ttf')
            # Crea: lato_small, lato_medium, lato_large, lato_xlarge
            canvas.add_widget(Text(10, 10, "Ciao", font='lato_medium'))
        """
        if sizes is None:
            sizes = {'small': 14, 'medium': 18, 'large': 24, 'xlarge': 48}

        for suffix, size in sizes.items():
            font_name = f"{family_name}_{suffix}"
            self.add_custom_font(font_name, font_path, size)

    def clear(self, color=255):
        """Pulisce il canvas"""
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def get_image(self):
        """Restituisce l'immagine PIL"""
        return self.image

    def add_widget(self, widget):
        """Aggiunge un widget al canvas"""
        widget.draw(self.draw, self.image, self.fonts)
        return self


class Widget:
    """Classe base per tutti i widget"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, draw, image, fonts):
        """Da implementare nelle sottoclassi"""
        raise NotImplementedError


class Text(Widget):
    """Widget per testo semplice"""

    def __init__(self, x, y, text, font_size='medium', font=None, fill=0, anchor=None):
        """
        Args:
            x, y: posizione
            text: testo da visualizzare
            font_size: 'small', 'medium', 'large', 'xlarge' (usato se font=None)
            font: nome del font personalizzato (es. 'lato_medium', 'custom_title')
                  se specificato, ha priorità su font_size
            fill: colore (0=nero, 255=bianco)
            anchor: ancora del testo ('lt', 'mm', etc.)
        """
        super().__init__(x, y)
        self.text = str(text)
        self.font_size = font_size
        self.font = font  # Font personalizzato (opzionale)
        self.fill = fill
        self.anchor = anchor

    def draw(self, draw, image, fonts):
        # Usa font personalizzato se specificato, altrimenti usa font_size
        if self.font and self.font in fonts:
            font = fonts[self.font]
        else:
            font = fonts.get(self.font_size, fonts.get('medium', ImageFont.load_default()))

        if self.anchor:
            draw.text((self.x, self.y), self.text, font=font, fill=self.fill, anchor=self.anchor)
        else:
            draw.text((self.x, self.y), self.text, font=font, fill=self.fill)


class Box(Widget):
    """Widget per box/rettangoli"""

    def __init__(self, x, y, width, height, fill=255, outline=0, outline_width=1):
        """
        Args:
            x, y: posizione top-left
            width, height: dimensioni
            fill: colore riempimento
            outline: colore bordo
            outline_width: spessore bordo
        """
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.fill = fill
        self.outline = outline
        self.outline_width = outline_width

    def draw(self, draw, image, fonts):
        draw.rectangle(
            (self.x, self.y, self.x + self.width, self.y + self.height),
            fill=self.fill,
            outline=self.outline,
            width=self.outline_width
        )


class StatusBox(Widget):
    """Box con testo per indicatori di stato (ON/OFF)"""

    def __init__(self, x, y, width, height, text, is_active=False, font_size='medium'):
        """
        Args:
            x, y: posizione
            width, height: dimensioni
            text: testo da visualizzare
            is_active: True per stato attivo (invertito)
            font_size: dimensione font
        """
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.text = text
        self.is_active = is_active
        self.font_size = font_size

    def draw(self, draw, image, fonts):
        # Box esterno
        draw.rectangle(
            (self.x, self.y, self.x + self.width, self.y + self.height),
            outline=0, fill=255
        )

        # Box interno (invertito se attivo)
        draw.rectangle(
            (self.x + 2, self.y + 2, self.x + self.width - 2, self.y + self.height - 2),
            outline=0, fill=0 if self.is_active else 255
        )

        # Testo centrato (colore invertito se attivo)
        text_fill = 255 if self.is_active else 0
        font = fonts.get(self.font_size, fonts['medium'])
        text_x = self.x + self.width / 2
        text_y = self.y + self.height / 2
        draw.text((text_x, text_y + 1), self.text, font=font, fill=text_fill, anchor="mm")


class NotchBar(Widget):
    """Barra verticale con tacche discrete"""

    def __init__(self, x, y, width, height, level, num_notches=5, spacing=3):
        """
        Args:
            x, y: posizione top-left
            width: larghezza barra
            height: altezza barra
            level: livello in percentuale (0-100)
            num_notches: numero di tacche
            spacing: spazio tra le tacche
        """
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.level = level
        self.num_notches = num_notches
        self.spacing = spacing

    def draw(self, draw, image, fonts):
        # Calcola quante tacche devono essere piene
        filled_notches = round(self.level * self.num_notches / 100)
        filled_notches = min(self.num_notches, max(0, filled_notches))

        # Calcola dimensioni tacche
        total_spacing = self.spacing * (self.num_notches - 1)
        available_height = self.height - total_spacing
        notch_height = available_height // self.num_notches

        # Disegna le tacche dal basso verso l'alto
        for i in range(self.num_notches):
            y_bottom = self.y + self.height - (i * (notch_height + self.spacing))
            y_top = y_bottom - notch_height

            # Bordo della tacca
            draw.rectangle(
                (self.x, y_top, self.x + self.width, y_bottom),
                outline=0, fill=255
            )

            # Riempimento se necessario
            if i < filled_notches:
                draw.rectangle(
                    (self.x + 2, y_top + 2, self.x + self.width - 2, y_bottom - 2),
                    fill=0
                )


class ProgressBar(Widget):
    """Barra di progresso orizzontale"""

    def __init__(self, x, y, width, height, progress, show_percentage=True, font_size='small'):
        """
        Args:
            x, y: posizione
            width, height: dimensioni
            progress: progresso in percentuale (0-100)
            show_percentage: mostra il testo con la percentuale
            font_size: dimensione font per la percentuale
        """
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.progress = max(0, min(100, progress))
        self.show_percentage = show_percentage
        self.font_size = font_size

    def draw(self, draw, image, fonts):
        # Bordo esterno
        draw.rectangle(
            (self.x, self.y, self.x + self.width, self.y + self.height),
            outline=0, fill=255
        )

        # Riempimento in base al progresso
        fill_width = int((self.width - 4) * self.progress / 100)
        if fill_width > 0:
            draw.rectangle(
                (self.x + 2, self.y + 2, self.x + 2 + fill_width, self.y + self.height - 2),
                fill=0
            )

        # Testo percentuale (opzionale)
        if self.show_percentage:
            text = f"{int(self.progress)}%"
            font = fonts.get(self.font_size, fonts['small'])
            text_x = self.x + self.width / 2
            text_y = self.y + self.height / 2

            # Disegna testo bianco su sfondo nero per leggibilità
            bbox = draw.textbbox((text_x, text_y), text, font=font, anchor="mm")
            draw.rectangle(bbox, fill=255)
            draw.text((text_x, text_y), text, font=font, fill=0, anchor="mm")


class SVGIcon(Widget):
    """Widget per icone SVG"""

    def __init__(self, x, y, svg_string, size=None):
        """
        Args:
            x, y: posizione
            svg_string: contenuto SVG come stringa
            size: tupla (width, height) per ridimensionare
        """
        super().__init__(x, y)
        self.svg_string = svg_string
        self.size = size

    def draw(self, draw, image, fonts):
        # Converte SVG in immagine
        png_data = cairosvg.svg2png(bytestring=self.svg_string.encode('utf-8'))
        img = Image.open(io.BytesIO(png_data))

        # Gestisce trasparenza
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

        # Ridimensiona se necessario
        if self.size:
            img = img.resize(self.size, Image.Resampling.LANCZOS)

        # Converti in B/N e incolla
        img = img.convert('1')
        image.paste(img, (self.x, self.y))


class SVG(Widget):
    """Widget per SVG - supporta sia stringhe che file"""

    def __init__(self, x, y, svg_source, size=None, is_file=False):
        """
        Args:
            x, y: posizione
            svg_source: stringa SVG o percorso al file SVG
            size: tupla (width, height) per ridimensionare
            is_file: True se svg_source è un percorso file, False se è una stringa
        """
        super().__init__(x, y)
        self.svg_source = svg_source
        self.size = size
        self.is_file = is_file

    def draw(self, draw, image, fonts):
        # Carica SVG da file o stringa
        if self.is_file:
            with open(self.svg_source, 'r') as f:
                svg_string = f.read()
        else:
            svg_string = self.svg_source

        # Converte SVG in immagine
        png_data = cairosvg.svg2png(bytestring=svg_string.encode('utf-8'))
        img = Image.open(io.BytesIO(png_data))

        # Gestisce trasparenza
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

        # Ridimensiona se necessario
        if self.size:
            img = img.resize(self.size, Image.Resampling.LANCZOS)

        # Converti in B/N e incolla
        img = img.convert('1')
        image.paste(img, (self.x, self.y))


class DonutChart(Widget):
    """Widget per grafici a ciambella (donut chart)"""

    def __init__(self, x, y, diameter, data, labels=None, hole_ratio=0.5, show_labels=True, font_size='small', use_patterns=True):
        """
        Args:
            x, y: posizione del centro del grafico
            diameter: diametro del grafico
            data: lista di valori numerici (verranno convertiti in percentuali)
            labels: lista di etichette (opzionale)
            hole_ratio: rapporto del buco centrale (0.0-1.0, default 0.5)
            show_labels: mostra le etichette con percentuali
            font_size: dimensione font per le etichette
            use_patterns: usa retinature invece di riempimenti solidi
        """
        super().__init__(x, y)
        self.diameter = diameter
        self.data = data
        self.labels = labels or [f"Seg {i+1}" for i in range(len(data))]
        self.hole_ratio = max(0.0, min(1.0, hole_ratio))
        self.show_labels = show_labels
        self.font_size = font_size
        self.use_patterns = use_patterns

    def _apply_pattern(self, draw, bbox, start_angle, end_angle, pattern_type, spacing=4):
        """Applica un pattern di retinatura a un settore"""
        # Crea maschera per il settore
        mask = Image.new('1', (self.diameter + 20, self.diameter + 20), 255)
        mask_draw = ImageDraw.Draw(mask)

        # Offset per centrare la maschera
        offset = 10
        mask_bbox = [offset, offset, self.diameter + offset, self.diameter + offset]

        # Disegna il settore sulla maschera
        mask_draw.pieslice(mask_bbox, start_angle, end_angle, fill=0)

        # Rimuovi il buco centrale dalla maschera
        hole_radius = int((self.diameter // 2) * self.hole_ratio)
        if hole_radius > 0:
            center = self.diameter // 2 + offset
            hole_bbox = [
                center - hole_radius,
                center - hole_radius,
                center + hole_radius,
                center + hole_radius
            ]
            mask_draw.ellipse(hole_bbox, fill=255)

        # Applica il pattern in base al tipo
        x1, y1, x2, y2 = bbox

        if pattern_type == 'horizontal':
            # Linee orizzontali
            for y in range(int(y1), int(y2), spacing):
                for x in range(int(x1), int(x2)):
                    mx = x - int(x1) + offset
                    my = y - int(y1) + offset
                    if 0 <= mx < mask.width and 0 <= my < mask.height:
                        if mask.getpixel((mx, my)) == 0:
                            draw.point((x, y), fill=0)

        elif pattern_type == 'vertical':
            # Linee verticali
            for x in range(int(x1), int(x2), spacing):
                for y in range(int(y1), int(y2)):
                    mx = x - int(x1) + offset
                    my = y - int(y1) + offset
                    if 0 <= mx < mask.width and 0 <= my < mask.height:
                        if mask.getpixel((mx, my)) == 0:
                            draw.point((x, y), fill=0)

        elif pattern_type == 'diagonal1':
            # Linee diagonali /
            for i in range(int(x1 - y2), int(x2 - y1), spacing):
                for x in range(int(x1), int(x2)):
                    y = x - i
                    if y1 <= y < y2:
                        mx = x - int(x1) + offset
                        my = int(y) - int(y1) + offset
                        if 0 <= mx < mask.width and 0 <= my < mask.height:
                            if mask.getpixel((mx, my)) == 0:
                                draw.point((x, int(y)), fill=0)

        elif pattern_type == 'diagonal2':
            # Linee diagonali \
            for i in range(int(x1 + y1), int(x2 + y2), spacing):
                for x in range(int(x1), int(x2)):
                    y = i - x
                    if y1 <= y < y2:
                        mx = x - int(x1) + offset
                        my = int(y) - int(y1) + offset
                        if 0 <= mx < mask.width and 0 <= my < mask.height:
                            if mask.getpixel((mx, my)) == 0:
                                draw.point((x, int(y)), fill=0)

        elif pattern_type == 'dots':
            # Puntini
            for x in range(int(x1), int(x2), spacing):
                for y in range(int(y1), int(y2), spacing):
                    mx = x - int(x1) + offset
                    my = y - int(y1) + offset
                    if 0 <= mx < mask.width and 0 <= my < mask.height:
                        if mask.getpixel((mx, my)) == 0:
                            draw.point((x, y), fill=0)

        elif pattern_type == 'crosshatch':
            # Grigliato (linee orizzontali + verticali)
            for y in range(int(y1), int(y2), spacing):
                for x in range(int(x1), int(x2)):
                    mx = x - int(x1) + offset
                    my = y - int(y1) + offset
                    if 0 <= mx < mask.width and 0 <= my < mask.height:
                        if mask.getpixel((mx, my)) == 0:
                            draw.point((x, y), fill=0)
            for x in range(int(x1), int(x2), spacing):
                for y in range(int(y1), int(y2)):
                    mx = x - int(x1) + offset
                    my = y - int(y1) + offset
                    if 0 <= mx < mask.width and 0 <= my < mask.height:
                        if mask.getpixel((mx, my)) == 0:
                            draw.point((x, y), fill=0)

    def draw(self, draw, image, fonts):
        if not self.data:
            return

        # Calcola il totale e le percentuali
        total = sum(self.data)
        if total == 0:
            return

        # Calcola il bounding box per il cerchio
        radius = self.diameter // 2
        bbox = [
            self.x - radius,
            self.y - radius,
            self.x + radius,
            self.y + radius
        ]

        # Disegna i settori
        start_angle = -90  # Inizia dall'alto

        # Pattern disponibili
        pattern_types = ['horizontal', 'vertical', 'diagonal1', 'diagonal2', 'dots', 'crosshatch']

        for i, value in enumerate(self.data):
            # Calcola l'angolo del settore
            angle = 360 * value / total
            end_angle = start_angle + angle

            if self.use_patterns:
                # Disegna il settore con sfondo bianco e bordo
                draw.pieslice(bbox, start_angle, end_angle, fill=255, outline=0, width=2)

                # Applica il pattern
                pattern_type = pattern_types[i % len(pattern_types)]
                self._apply_pattern(draw, bbox, start_angle, end_angle, pattern_type, spacing=3)
            else:
                # Disegna il settore con riempimento solido
                fill_color = 0 if i % 2 == 0 else 255
                draw.pieslice(bbox, start_angle, end_angle, fill=fill_color, outline=0, width=2)

            # Calcola posizione per l'etichetta (all'esterno del grafico)
            if self.show_labels and angle > 3:  # Mostra solo se il settore è abbastanza grande
                mid_angle = (start_angle + end_angle) / 2

                # Posizione esterna al cerchio
                label_radius = radius * 1.3  # Fuori dal cerchio
                label_x = self.x + label_radius * math.cos(math.radians(mid_angle))
                label_y = self.y + label_radius * math.sin(math.radians(mid_angle))

                # Prepara il testo
                percentage = (value / total) * 100
                label_text = self.labels[i] if i < len(self.labels) else f"Seg{i+1}"
                font = fonts.get(self.font_size, fonts['small'])

                # Determina l'ancora in base alla posizione
                if mid_angle > -45 and mid_angle <= 45:  # Destra
                    anchor = "lm"
                elif mid_angle > 45 and mid_angle <= 135:  # Basso
                    anchor = "mt"
                elif mid_angle > 135 or mid_angle <= -135:  # Sinistra
                    anchor = "rm"
                else:  # Alto
                    anchor = "mb"

                # Disegna l'etichetta e la percentuale separatamente (anchor non supporta multilinea)
                # Prima linea: label
                draw.text((label_x, label_y - 6), label_text, font=font, fill=0, anchor=anchor)
                # Seconda linea: percentuale
                draw.text((label_x, label_y + 6), f"{percentage:.0f}%", font=font, fill=0, anchor=anchor)

            start_angle = end_angle

        # Disegna il buco centrale
        hole_radius = int(radius * self.hole_ratio)
        if hole_radius > 0:
            hole_bbox = [
                self.x - hole_radius,
                self.y - hole_radius,
                self.x + hole_radius,
                self.y + hole_radius
            ]
            draw.ellipse(hole_bbox, fill=255, outline=0, width=2)


class Line(Widget):
    """Widget per linee"""

    def __init__(self, x1, y1, x2, y2, fill=0, width=1):
        """
        Args:
            x1, y1: punto iniziale
            x2, y2: punto finale
            fill: colore
            width: spessore
        """
        super().__init__(x1, y1)
        self.x2 = x2
        self.y2 = y2
        self.fill = fill
        self.width = width

    def draw(self, draw, image, fonts):
        draw.line((self.x, self.y, self.x2, self.y2), fill=self.fill, width=self.width)


class SimpleGraph(Widget):
    """Grafico a linee semplice"""

    def __init__(self, x, y, width, height, data, min_val=None, max_val=None):
        """
        Args:
            x, y: posizione
            width, height: dimensioni
            data: lista di valori numerici
            min_val, max_val: range valori (None per auto)
        """
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.data = data
        self.min_val = min_val if min_val is not None else min(data) if data else 0
        self.max_val = max_val if max_val is not None else max(data) if data else 100

    def draw(self, draw, image, fonts):
        if not self.data or len(self.data) < 2:
            return

        # Bordo
        draw.rectangle(
            (self.x, self.y, self.x + self.width, self.y + self.height),
            outline=0, fill=255
        )

        # Normalizza i dati
        value_range = self.max_val - self.min_val
        if value_range == 0:
            return

        # Calcola i punti
        points = []
        step = (self.width - 4) / (len(self.data) - 1)

        for i, val in enumerate(self.data):
            px = self.x + 2 + int(i * step)
            normalized = (val - self.min_val) / value_range
            py = self.y + self.height - 2 - int(normalized * (self.height - 4))
            points.append((px, py))

        # Disegna la linea
        if len(points) >= 2:
            draw.line(points, fill=0, width=2)


class HorizontalLayout:
    """Layout helper per disporre widget orizzontalmente"""

    def __init__(self, x, y, spacing=10):
        self.x = x
        self.y = y
        self.spacing = spacing
        self.current_x = x

    def add(self, widget, width=None):
        """Aggiunge un widget al layout"""
        widget.x = self.current_x
        widget.y = self.y
        if width:
            self.current_x += width + self.spacing
        elif hasattr(widget, 'width'):
            self.current_x += widget.width + self.spacing
        return widget


class VerticalLayout:
    """Layout helper per disporre widget verticalmente"""

    def __init__(self, x, y, spacing=10):
        self.x = x
        self.y = y
        self.spacing = spacing
        self.current_y = y

    def add(self, widget, height=None):
        """Aggiunge un widget al layout"""
        widget.x = self.x
        widget.y = self.current_y
        if height:
            self.current_y += height + self.spacing
        elif hasattr(widget, 'height'):
            self.current_y += widget.height + self.spacing
        return widget
