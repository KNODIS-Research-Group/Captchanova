import argparse
import csv
import io
import os
import random

from PIL import Image, ImageDraw, ImageFont

from captchanova import fonts


def random_color():
    """Genera un color aleatorio en formato RGB.

    :return: Una tupla con tres valores enteros entre 0 y 255
    """
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def get_font(image_size, text, min_size=10):
    """Dado el tamaño de la imagen y el texto, selecciona la fuente
    más grande que cabe en dicha imagen.

    :param image_size: Tamaño de la imagen (ancho, alto)
    :param text: Texto del captcha
    :param min_size: Tamaño de fuente mínimo legible. Por defecto 10
    :return: La fuente seleccionada
    """
    width, height = image_size
    font_bytes = fonts.get_font_as_bytes()

    font = ImageFont.truetype(io.BytesIO(font_bytes), min_size)

    # Empezamos con letra grande y bajamos hasta que el texto encaje
    font_size = height * 2
    while font_size > min_size:
        font = ImageFont.truetype(io.BytesIO(font_bytes), font_size)
        l, t, r, b = font.getbbox(text)
        text_width, text_height = r - l, b - t
        if text_width < width and text_height < height:
            break
        font_size -= 1
    return font


def generate_captcha(
        alphabet,
        length,
        size,
        move_vertical_letters,
        rotation,
):
    """Genera un captcha.

    :param alphabet: Caracteres a usar para el captcha
    :param length: Longitud del captcha
    :param size: Tamaño de la imagen (ancho, alto)
    :param move_vertical_letters: Mover aleatoriamente los caracteres en vertical
    :param rotation: Rotación aleatoria de caracteres (min, máx)
    :return: El texto del captcha y la imagen del captcha
    """
    image_width, image_height = size

    # Creamos el bloque de la imagen
    image = Image.new('RGB', size, color=random_color())
    draw = ImageDraw.Draw(image)

    # Generamos el texto del captcha
    text = ''.join(random.choice(alphabet) for _ in range(length))

    x = 0
    for char in text:
        temp_image = Image.new('RGBA', (image_width // length, image_height), (255, 255, 255, 0))  # fondo transparente
        temp_draw = ImageDraw.Draw(temp_image)

        # Ajustamos la fuente para que el texto encaje en la imagen
        font = get_font(size, text)

        # Dibujar el carácter en la imagen temporal
        temp_draw.text((0, 0), char, font=font, fill=random_color())

        # Rotar la imagen temporal
        angle = random.randint(*rotation)
        rotated_char = temp_image.rotate(
            angle,
            expand=True,
            fillcolor=(255, 255, 255, 0)
        )

        # Calcular la nueva posición y considerar el movimiento vertical si está habilitado
        y = 0 if not move_vertical_letters else random.randint(-20, 10)

        # Pegar el carácter rotado en la imagen final
        image.paste(rotated_char, (int(x), int(y)), rotated_char)

        # Ajustar x para el siguiente carácter
        x += image_width // length

    return text, image


def add_noise_lines(image, size, lines_num, lines_width):
    """Agrega líneas aleatorias a la imagen.

    :param image: Imagen a la que se le agregará el ruido
    :param size: Tamaño de la imagen (ancho, alto)
    :param lines_num: Número de líneas aleatorias a agregar (min, máx)
    :param lines_width: Tamaño de las líneas aleatorias (min, máx)
    :return: La imagen con el ruido agregado
    """
    image_width, image_height = size

    draw = ImageDraw.Draw(image)
    for _ in range(random.randint(*lines_num)):
        x1 = random.randint(0, image_width)
        x2 = random.randint(0, image_width)
        y1 = random.randint(0, image_height)
        y2 = random.randint(0, image_height)

        draw.line(
            xy=((x1, y1), (x2, y2)),
            fill=random_color(),
            width=random.randint(*lines_width)
        )

    return image


def add_noise_dots(image, size, width, number):
    """Agrega puntos aleatorios a la imagen.

    :param image: Imagen a la que se le agregará el ruido
    :param size: Tamaño de la imagen (ancho, alto)
    :param width: Tamaño de los puntos aleatorios
    :param number: Número de puntos aleatorios a agregar
    :return: La imagen con el ruido agregado
    """
    image_width, image_height = size

    draw = ImageDraw.Draw(image)
    for _ in range(number):
        x = random.randint(0, image_width)
        y = random.randint(0, image_height)

        draw.line(
            xy=((x, y), (x, y)),
            fill=random_color(),
            width=width
        )

    return image


def main():
    """Genera captchas y los guarda en un directorio junto a un CSV"""
    parser = argparse.ArgumentParser(
        description='Generador de Captchas - Captchanova'
    )
    parser.add_argument(
        '--alphabet', type=str, required=True,
        help='Caracteres para generar el captcha',
    )
    parser.add_argument(
        '--len', type=int, required=True,
        help='Número de caracteres del captcha',
    )
    parser.add_argument(
        '--num', type=int, required=True,
        help='Número de captchas a generar',
    )
    parser.add_argument(
        '--size', type=eval, required=True,
        help='Tupla de tamaño de la imagen (alto, ancho) en píxeles',
    )
    parser.add_argument(
        '--output', type=str, required=True,
        help='Directorio de salida para los captchas generados',
    )
    parser.add_argument(
        '--rotate', type=eval, default=(0, 0),
        help='Rotación aleatoria de caracteres (min, máx)',
    )
    parser.add_argument(
        '--move-vertical', action='store_false',
        help='Mover aleatoriamente los caracteres en vertical',
    )
    parser.add_argument(
        '--lines-num', type=eval, default=(0, 0),
        help='Líneas aleatorias a generear (min, máx)',
    )
    parser.add_argument(
        '--lines-width', type=eval, default=(0, 0),
        help='Tamaño en píxeles de las líneas aleatorias (min, máx)',
    )
    parser.add_argument(
        '--dots-number', type=eval, default=(0, 0),
        help='Número de puntos aleatorios a agregar (min, máx)',
    )
    parser.add_argument(
        '--dots-width', type=int, default=0,
        help='Tamaño en píxeles de los puntos aleatorios',
    )
    parser.add_argument(
        '--padding', type=int, default=0,
        help='Cuánto padding queremos en el nombre de las imágenes',
    )
    args = parser.parse_args()

    # Crear el directorio de salida si no existe
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Generar los captchas
    csv_path = os.path.join(args.output, 'labels.csv')
    with open(csv_path, mode='w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Id', 'Label'])

        for i in range(args.num):
            text, image = generate_captcha(
                alphabet=args.alphabet,
                length=args.len,
                size=args.size,
                move_vertical_letters=args.move_vertical,
                rotation=args.rotate,
            )
            # Agregamos un poco de ruido: líneas aleatorias
            image = add_noise_lines(
                image,
                args.size,
                args.lines_num,
                args.lines_width,
            )
            image = add_noise_dots(
                image,
                args.size,
                args.dots_width,
                random.randint(*args.dots_number),
            )

            filename = f'{i:0{args.padding}d}.png'
            image.save(os.path.join(args.output, filename))
            csv_writer.writerow([i, text])


if __name__ == '__main__':
    main()
