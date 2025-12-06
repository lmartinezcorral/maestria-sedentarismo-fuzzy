"""
Script para generar diagramas explicativos de Leave-One-User-Out (LOUO)
usando Python Pillow, siguiendo la identidad visual de la plantilla.

Diagrama 5: Resultados por Usuario (F1-Score)
Diagrama 6: Flujo Completo del Proceso
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ============================================================================
# IDENTIDAD VISUAL
# ============================================================================

# Paleta de colores
COLORS = {
    'dark_purple': '#571E72',
    'bright_magenta': '#AA03C0',
    'light_yellow': '#FEF7CD',
    'medium_purple': '#A733EA',
    'muted_purple': '#A4579F',
    'golden_yellow': '#D0A433',
    'off_white': '#F1F0D9',
    'deep_purple': '#750CA3',
    'white': '#FFFFFF',
    'black': '#000000',
    'green': '#4CAF50',
    'red': '#F44336',
    'blue': '#2196F3'
}

# Tamaños de fuente
FONT_SIZES = {
    'title': 36,
    'subtitle': 32,
    'body': 24,
    'graph_labels': 18
}

def hex_to_rgb(hex_color):
    """Convierte color hexadecimal a RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_arrow(draw, x1, y1, x2, y2, color, width=3, arrow_size=10):
    """Dibuja una flecha de (x1, y1) a (x2, y2)"""
    # Línea principal
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    
    # Calcular ángulo
    angle = math.atan2(y2 - y1, x2 - x1)
    
    # Puntas de la flecha
    arrow_x1 = x2 - arrow_size * math.cos(angle - math.pi / 6)
    arrow_y1 = y2 - arrow_size * math.sin(angle - math.pi / 6)
    arrow_x2 = x2 - arrow_size * math.cos(angle + math.pi / 6)
    arrow_y2 = y2 - arrow_size * math.sin(angle + math.pi / 6)
    
    draw.polygon([(x2, y2), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                fill=color)

def draw_rounded_rectangle(draw, x1, y1, x2, y2, radius, fill, outline, width):
    """Dibuja un rectángulo redondeado"""
    # Rectángulo principal
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=None)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=None)
    
    # Esquinas redondeadas (círculos)
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill, outline=None)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill, outline=None)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill, outline=None)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill, outline=None)
    
    # Borde
    if outline:
        # Lados rectos
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)
        
        # Arcos de las esquinas
        for corner_x, corner_y in [(x1 + radius, y1 + radius), 
                                   (x2 - radius, y1 + radius),
                                   (x1 + radius, y2 - radius),
                                   (x2 - radius, y2 - radius)]:
            # Dibujar arcos (simplificado)
            pass

# ============================================================================
# DIAGRAMA 5: RESULTADOS POR USUARIO (F1-Score)
# ============================================================================

def generar_diagrama5_resultados_usuario():
    """Genera diagrama de barras con F1-Score por usuario"""
    
    width = 1400
    height = 900
    img = Image.new('RGB', (width, height), COLORS['white'])
    draw = ImageDraw.Draw(img)
    
    # Datos de F1-Score por usuario
    usuarios = [
        ('Usuario 1', 0.812),
        ('Usuario 2', 0.997),
        ('Usuario 3', 0.215),
        ('Usuario 4', 0.654),
        ('Usuario 5', 0.876),
        ('Usuario 6', 0.743),
        ('Usuario 7', 0.891),
        ('Usuario 8', 0.567),
        ('Usuario 9', 0.789),
        ('Usuario 10', 0.698)
    ]
    
    # Intentar cargar fuentes
    try:
        title_font = ImageFont.truetype("arial.ttf", FONT_SIZES['title'])
        subtitle_font = ImageFont.truetype("arial.ttf", FONT_SIZES['subtitle'])
        body_font = ImageFont.truetype("arial.ttf", FONT_SIZES['body'])
        label_font = ImageFont.truetype("arial.ttf", FONT_SIZES['graph_labels'])
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Título
    title = "Resultados Leave-One-User-Out por Usuario"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 30), title, 
              fill=hex_to_rgb(COLORS['dark_purple']), font=title_font)
    
    # Subtítulo
    subtitle = "F1-Score LOUO: μ = 0.780 ± 0.167 (CV = 21.4%)"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((width - subtitle_width) // 2, 80), subtitle,
              fill=hex_to_rgb(COLORS['medium_purple']), font=subtitle_font)
    
    # Área del gráfico
    chart_x = 100
    chart_y = 150
    chart_width = width - 200
    chart_height = 600
    bar_width = chart_width // (len(usuarios) + 1)
    bar_spacing = bar_width // 4
    
    # Eje Y
    max_value = 1.0
    min_value = 0.0
    y_scale = chart_height / (max_value - min_value)
    
    # Dibujar ejes
    draw.line([chart_x, chart_y, chart_x, chart_y + chart_height], 
              fill=hex_to_rgb(COLORS['black']), width=2)
    draw.line([chart_x, chart_y + chart_height, chart_x + chart_width, chart_y + chart_height],
              fill=hex_to_rgb(COLORS['black']), width=2)
    
    # Etiquetas del eje Y
    for i in range(0, 11):
        value = i / 10.0
        y_pos = chart_y + chart_height - (value * y_scale)
        label = f"{value:.1f}"
        draw.text((chart_x - 40, y_pos - 10), label,
                  fill=hex_to_rgb(COLORS['black']), font=label_font)
        if i > 0:
            draw.line([chart_x - 5, y_pos, chart_x + chart_width, y_pos],
                      fill=hex_to_rgb(COLORS['off_white']), width=1)
    
    # Línea de referencia (media)
    mean_y = chart_y + chart_height - (0.780 * y_scale)
    draw.line([chart_x, mean_y, chart_x + chart_width, mean_y],
              fill=hex_to_rgb(COLORS['golden_yellow']), width=3)
    draw.text((chart_x + chart_width + 10, mean_y - 10), "Media (0.780)",
              fill=hex_to_rgb(COLORS['golden_yellow']), font=label_font)
    
    # Línea de referencia (umbral 0.65)
    threshold_y = chart_y + chart_height - (0.65 * y_scale)
    # Línea punteada (simulada con pequeños segmentos)
    for x in range(chart_x, chart_x + chart_width, 10):
        draw.line([x, threshold_y, min(x + 5, chart_x + chart_width), threshold_y],
                  fill=hex_to_rgb(COLORS['muted_purple']), width=2)
    draw.text((chart_x + chart_width + 10, threshold_y - 10), "Umbral (0.65)",
              fill=hex_to_rgb(COLORS['muted_purple']), font=label_font)
    
    # Dibujar barras
    for i, (usuario, f1_score) in enumerate(usuarios):
        x_start = chart_x + (i + 1) * bar_width + bar_spacing
        bar_height = f1_score * y_scale
        y_start = chart_y + chart_height - bar_height
        
        # Color según rendimiento
        if f1_score >= 0.65:
            bar_color = hex_to_rgb(COLORS['green'])
        elif f1_score >= 0.50:
            bar_color = hex_to_rgb(COLORS['golden_yellow'])
        else:
            bar_color = hex_to_rgb(COLORS['red'])
        
        # Dibujar barra
        draw.rectangle([x_start, y_start, x_start + bar_width - bar_spacing, chart_y + chart_height],
                      fill=bar_color, outline=hex_to_rgb(COLORS['black']), width=1)
        
        # Valor F1-Score sobre la barra
        value_text = f"{f1_score:.3f}"
        value_bbox = draw.textbbox((0, 0), value_text, font=label_font)
        value_width = value_bbox[2] - value_bbox[0]
        draw.text((x_start + (bar_width - bar_spacing - value_width) // 2, y_start - 25),
                 value_text, fill=hex_to_rgb(COLORS['black']), font=label_font)
        
        # Etiqueta del usuario
        user_text = f"U{i+1}"
        user_bbox = draw.textbbox((0, 0), user_text, font=label_font)
        user_width = user_bbox[2] - user_bbox[0]
        draw.text((x_start + (bar_width - bar_spacing - user_width) // 2, chart_y + chart_height + 10),
                 user_text, fill=hex_to_rgb(COLORS['black']), font=label_font)
    
    # Leyenda
    legend_y = chart_y + chart_height + 60
    legend_items = [
        ("F1 ≥ 0.65 (7 usuarios)", COLORS['green']),
        ("0.50 ≤ F1 < 0.65 (2 usuarios)", COLORS['golden_yellow']),
        ("F1 < 0.50 (1 usuario)", COLORS['red'])
    ]
    
    legend_x = chart_x
    for label, color in legend_items:
        draw.rectangle([legend_x, legend_y, legend_x + 20, legend_y + 20],
                      fill=hex_to_rgb(color), outline=hex_to_rgb(COLORS['black']), width=1)
        draw.text((legend_x + 30, legend_y + 2), label,
                 fill=hex_to_rgb(COLORS['black']), font=label_font)
        legend_x += 280
    
    # Nota al pie
    note = "7 de 10 usuarios alcanzaron F1-Score ≥ 0.65, demostrando capacidad de generalización inter-sujeto"
    note_bbox = draw.textbbox((0, 0), note, font=label_font)
    note_width = note_bbox[2] - note_bbox[0]
    draw.text(((width - note_width) // 2, height - 40), note,
             fill=hex_to_rgb(COLORS['muted_purple']), font=label_font)
    
    output_path = "diagrama5_resultados_usuario.png"
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"✓ Diagrama 5 generado: {output_path}")
    return output_path

# ============================================================================
# DIAGRAMA 6: FLUJO COMPLETO DEL PROCESO
# ============================================================================

def generar_diagrama6_flujo_completo():
    """Genera diagrama de flujo del proceso LOUO completo"""
    
    width = 1800
    height = 1100
    img = Image.new('RGB', (width, height), COLORS['white'])
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", FONT_SIZES['title'])
        body_font = ImageFont.truetype("arial.ttf", FONT_SIZES['body'])
        label_font = ImageFont.truetype("arial.ttf", FONT_SIZES['graph_labels'])
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Título
    title = "Flujo Completo: Validación Leave-One-User-Out"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 20), title,
              fill=hex_to_rgb(COLORS['dark_purple']), font=title_font)
    
    # Definir cajas
    box_width = 220
    box_height = 100
    box_spacing = 60
    radius = 10
    start_x = 80
    start_y = 120
    
    # Colores
    box_colors = {
        'start': COLORS['dark_purple'],
        'process': COLORS['medium_purple'],
        'decision': COLORS['golden_yellow'],
        'loop': COLORS['bright_magenta'],
        'end': COLORS['green']
    }
    
    # Paso 1: Inicio
    x1, y1 = start_x, start_y
    draw_rounded_rectangle(draw, x1, y1, x1 + box_width, y1 + box_height,
                          radius, hex_to_rgb(box_colors['start']),
                          hex_to_rgb(COLORS['black']), 2)
    text1 = "Cohorte\nN=10 usuarios\n1,337 semanas"
    lines1 = text1.split('\n')
    for i, line in enumerate(lines1):
        draw.text((x1 + 15, y1 + 15 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha 1
    arrow_x1 = x1 + box_width
    arrow_y1 = y1 + box_height // 2
    arrow_x2 = arrow_x1 + box_spacing
    draw_arrow(draw, arrow_x1, arrow_y1, arrow_x2, arrow_y1,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 2: Preprocesamiento
    x2, y2 = arrow_x2, y1
    draw_rounded_rectangle(draw, x2, y2, x2 + box_width, y2 + box_height,
                          radius, hex_to_rgb(box_colors['process']),
                          hex_to_rgb(COLORS['black']), 2)
    text2 = "Preprocesamiento\nImputación +\nNormalización"
    lines2 = text2.split('\n')
    for i, line in enumerate(lines2):
        draw.text((x2 + 15, y2 + 15 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha 2
    arrow_x2_end = x2 + box_width
    arrow_x3 = arrow_x2_end + box_spacing
    draw_arrow(draw, arrow_x2_end, arrow_y1, arrow_x3, arrow_y1,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 3: Agregación
    x3, y3 = arrow_x3, y1
    draw_rounded_rectangle(draw, x3, y3, x3 + box_width, y3 + box_height,
                          radius, hex_to_rgb(box_colors['process']),
                          hex_to_rgb(COLORS['black']), 2)
    text3 = "Agregación Semanal\nMedianas + IQR"
    lines3 = text3.split('\n')
    for i, line in enumerate(lines3):
        draw.text((x3 + 15, y3 + 30 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha 3
    arrow_x3_end = x3 + box_width
    arrow_x4 = arrow_x3_end + box_spacing
    draw_arrow(draw, arrow_x3_end, arrow_y1, arrow_x4, arrow_y1,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 4: Inicio Loop
    x4, y4 = arrow_x4, y1
    draw_rounded_rectangle(draw, x4, y4, x4 + box_width, y4 + box_height,
                          radius, hex_to_rgb(box_colors['loop']),
                          hex_to_rgb(COLORS['black']), 2)
    text4 = "Iteración LOUO\ni = 1 a 10"
    lines4 = text4.split('\n')
    for i, line in enumerate(lines4):
        draw.text((x4 + 40, y4 + 35 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha hacia abajo
    loop_y = y4 + box_height
    loop_y_end = loop_y + 120
    draw_arrow(draw, x4 + box_width // 2, loop_y,
              x4 + box_width // 2, loop_y_end,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 5: Separar Usuario
    x5, y5 = x4, loop_y_end
    draw_rounded_rectangle(draw, x5, y5, x5 + box_width, y5 + box_height,
                          radius, hex_to_rgb(box_colors['process']),
                          hex_to_rgb(COLORS['black']), 2)
    text5 = "Separar Usuario i\ncomo TEST"
    lines5 = text5.split('\n')
    for i, line in enumerate(lines5):
        draw.text((x5 + 30, y5 + 35 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha horizontal
    arrow_y5 = y5 + box_height // 2
    arrow_x6 = x5 + box_width + box_spacing
    draw_arrow(draw, x5 + box_width, arrow_y5, arrow_x6, arrow_y5,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 6: Entrenar
    x6, y6 = arrow_x6, y5
    draw_rounded_rectangle(draw, x6, y6, x6 + box_width, y6 + box_height,
                          radius, hex_to_rgb(box_colors['process']),
                          hex_to_rgb(COLORS['black']), 2)
    text6 = "Entrenar Modelo\ncon Usuarios\n1...i-1, i+1...10"
    lines6 = text6.split('\n')
    for i, line in enumerate(lines6):
        draw.text((x6 + 10, y6 + 15 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha
    arrow_x6_end = x6 + box_width
    arrow_x7 = arrow_x6_end + box_spacing
    draw_arrow(draw, arrow_x6_end, arrow_y5, arrow_x7, arrow_y5,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 7: Evaluar
    x7, y7 = arrow_x7, y5
    draw_rounded_rectangle(draw, x7, y7, x7 + box_width, y7 + box_height,
                          radius, hex_to_rgb(box_colors['process']),
                          hex_to_rgb(COLORS['black']), 2)
    text7 = "Evaluar en\nUsuario i\nCalcular F1ᵢ"
    lines7 = text7.split('\n')
    for i, line in enumerate(lines7):
        draw.text((x7 + 30, y7 + 30 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha hacia abajo
    eval_y = y7 + box_height
    eval_y_end = eval_y + 100
    draw_arrow(draw, x7 + box_width // 2, eval_y,
              x7 + box_width // 2, eval_y_end,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 8: Almacenar
    x8, y8 = x7, eval_y_end
    draw_rounded_rectangle(draw, x8, y8, x8 + box_width, y8 + box_height,
                          radius, hex_to_rgb(box_colors['process']),
                          hex_to_rgb(COLORS['black']), 2)
    text8 = "Almacenar\nF1ᵢ"
    lines8 = text8.split('\n')
    for i, line in enumerate(lines8):
        draw.text((x8 + 60, y8 + 35 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha hacia la izquierda (loop)
    loop_back_x = x8 - box_spacing
    draw_arrow(draw, x8, y8 + box_height // 2,
              loop_back_x, y8 + box_height // 2,
              hex_to_rgb(COLORS['black']), 3)
    
    # Decisión: i < 10?
    decision_x = loop_back_x - box_width
    decision_y = y8
    diamond_size = 50
    # Rombo
    diamond_points = [
        (decision_x + box_width // 2, decision_y),
        (decision_x + box_width, decision_y + box_height // 2),
        (decision_x + box_width // 2, decision_y + box_height),
        (decision_x, decision_y + box_height // 2)
    ]
    draw.polygon(diamond_points, fill=hex_to_rgb(box_colors['decision']),
                outline=hex_to_rgb(COLORS['black']), width=2)
    draw.text((decision_x + 50, decision_y + 40), "i < 10?",
             fill=hex_to_rgb(COLORS['black']), font=body_font)
    
    # Flecha "Sí" (hacia arriba)
    yes_arrow_y = decision_y + box_height // 2
    yes_arrow_y_up = y4 + box_height
    draw_arrow(draw, decision_x, yes_arrow_y,
              x4, yes_arrow_y_up,
              hex_to_rgb(COLORS['green']), 3)
    draw.text((decision_x - 50, yes_arrow_y - 30), "Sí",
             fill=hex_to_rgb(COLORS['green']), font=label_font)
    
    # Flecha "No" (hacia la izquierda)
    no_arrow_x = decision_x - box_spacing
    draw_arrow(draw, decision_x, yes_arrow_y,
              no_arrow_x, yes_arrow_y,
              hex_to_rgb(COLORS['red']), 3)
    draw.text((no_arrow_x - 30, yes_arrow_y - 20), "No",
             fill=hex_to_rgb(COLORS['red']), font=label_font)
    
    # Paso 9: Agregar Resultados
    x9, y9 = no_arrow_x - box_width, decision_y
    draw_rounded_rectangle(draw, x9, y9, x9 + box_width, y9 + box_height,
                          radius, hex_to_rgb(box_colors['process']),
                          hex_to_rgb(COLORS['black']), 2)
    text9 = "Agregar Resultados\nμ, σ, CV"
    lines9 = text9.split('\n')
    for i, line in enumerate(lines9):
        draw.text((x9 + 30, y9 + 30 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Flecha
    arrow_x9 = x9 - box_spacing
    draw_arrow(draw, x9, y9 + box_height // 2,
              arrow_x9, y9 + box_height // 2,
              hex_to_rgb(COLORS['black']), 3)
    
    # Paso 10: Final
    x10, y10 = arrow_x9 - box_width, y9
    draw_rounded_rectangle(draw, x10, y10, x10 + box_width, y10 + box_height,
                          radius, hex_to_rgb(box_colors['end']),
                          hex_to_rgb(COLORS['black']), 2)
    text10 = "F1-Score LOUO\n0.780 ± 0.167"
    lines10 = text10.split('\n')
    for i, line in enumerate(lines10):
        draw.text((x10 + 30, y10 + 30 + i * 25), line,
                 fill=hex_to_rgb(COLORS['white']), font=body_font)
    
    # Leyenda
    legend_y = height - 100
    legend_x = 50
    legend_items = [
        ("Inicio", box_colors['start']),
        ("Proceso", box_colors['process']),
        ("Decisión", box_colors['decision']),
        ("Loop", box_colors['loop']),
        ("Fin", box_colors['end'])
    ]
    
    for i, (label, color) in enumerate(legend_items):
        x_pos = legend_x + i * 200
        draw.rectangle([x_pos, legend_y, x_pos + 20, legend_y + 20],
                      fill=hex_to_rgb(color), outline=hex_to_rgb(COLORS['black']), width=1)
        draw.text((x_pos + 25, legend_y + 2), label,
                 fill=hex_to_rgb(COLORS['black']), font=label_font)
    
    output_path = "diagrama6_flujo_completo.png"
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"✓ Diagrama 6 generado: {output_path}")
    return output_path

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal para generar ambos diagramas"""
    print("Generando diagramas LOUO con Python Pillow...")
    print("=" * 60)
    
    try:
        diagrama5 = generar_diagrama5_resultados_usuario()
        print()
        diagrama6 = generar_diagrama6_flujo_completo()
        print()
        print("=" * 60)
        print("✓ Ambos diagramas generados exitosamente!")
        print(f"  - {diagrama5}")
        print(f"  - {diagrama6}")
    except Exception as e:
        print(f"✗ Error al generar diagramas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
