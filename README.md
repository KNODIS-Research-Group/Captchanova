# Generador de Captchas Aleatorios - Captchanova

## Descripción

CaptchaNova es una herramienta diseñada para la generación de captchas
aleatorios, orientada a prácticas universitarias de análisis de imágenes. Crea
imágenes de captchas que incluyen texto con variaciones aleatorias de color,
posición, y rotación, además de agregar ruido mediante líneas y puntos
aleatorios para aumentar la complejidad del análisis.

## Cómo Usar

Para utilizar CaptchaNova necesitarás un entorno con Python 3.10 o superior y
ciertas dependencias descritas en el fichero `pyproject.toml`.

En caso de usar Poetry, puedes instalar las dependencias ejecutando el comando
`poetry install` desde el directorio del proyecto.

Una vez completada la instalación de las dependencias, se pueden generar
los captchas ejecutando directamente el script a través de Poetry. Usa el
siguiente comando, personalizándolo con los argumentos deseados:

```bash
poetry run captchanova --alphabet "ABCDEFGHJKLMNPQRSTUVWXYZ23456789" \
                       --len 5 --num 100 --size "(200, 50)" \
                       --output "./captchas" --rotate "(0,30)" \
                       --move-vertical --lines-num "(1,3)" \
                       --lines-width "(1,3)" --dots-number "(100,150)" \
                       --dots-width 2
```

Este comando generará 100 captchas con textos de 5 caracteres de longitud,
agregará rotación a los caracteres, los moverá verticalmente, y añadirá ruido
en forma de líneas y puntos.

### Descripción de los Argumentos

- `--alphabet`: Define los caracteres posibles que pueden aparecer en el
  captcha. Debe ser una cadena de texto con los caracteres deseados sin
  espacios,
- `--len`: Establece el número de caracteres que tendrá el captcha,
- `--num`: Determina la cantidad de captchas que se generarán,
- `--size`: Especifica el tamaño de la imagen del captcha como una tupla
  (ancho, alto) en píxeles,
- `--output`: Define el directorio donde se guardarán los captchas generados,
- `--rotate`: Indica el rango de rotación aleatoria de los caracteres en
  grados como una tupla de la forma (min, máx); en caso de que no se desee
  rotación, se debe omitir este argumento,
- `--move-vertical`: Permite mover aleatoriamente los caracteres en vertical
  si está presente; en caso de que no se desee mover los caracteres, se debe
  omitir este argumento,
- `--lines-num`: Define el rango del número de líneas aleatorias a agregar en
  la imagen como una tupla de la forma (min, máx); en caso de que no se desee
  agregar líneas, se debe omitir este argumento,
- `--lines-width`: Establece el grosor de las líneas aleatorias en píxeles a
  agregar en la imagen; en caso de que
  no se desee agregar líneas, se debe omitir este argumento,
- `--dots-number`: Determina el rango del número de puntos aleatorios a
  agregar en la imagen como una tupla de la forma (min, máx); en caso de que
  no se desee agregar líneas, se debe omitir este argumento,
- `--dots-width`: Especifica el tamaño en píxeles de los puntos aleatorios.

## Licencia

Este proyecto está licenciado bajo la Licencia Pública General de GNU versión
3 (GPLv3). Para obtener más información, consulta el archivo LICENSE incluido
en este repositorio o visita https://www.gnu.org/licenses/gpl-3.0.html.
