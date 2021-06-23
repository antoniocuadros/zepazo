# Zepazo :waning_crescent_moon:

## Description :collision:
Zepazo is a project that aims to facilitate the detection of lunar impacts in videos taken from telescopes and standard cameras by comparing the different frames of the videos, trying to minimize false positives as much as possible.

## Motivation :star:
This project originally arises for the completion of a Final Degree Project proposed by [Sergio Alonso Burgos](https://lsi.ugr.es/lsi/zerjioi) and is being carried out by [Antonio Cuadros Lapresta](https://github.com/antoniocuadros) with the help of Sergio with the aim of facilitating the detection of lunar impacts due to our great love for the astronomy. It is intended to carry out the implementation of a novel software due at present we have no record of such software exists and which will facilitate the work of astronomers.

## Manual de usuario Zepazo 🇪🇸
Zepazo es un conjunto de programas que pretende aportar una solución automatizada para la detección de impactos a través del análisis de grabaciones de zonas oscuras de la Luna. Con el objetivo de facilitar dicha tarea al usuario se proponen cuatro programas:

- __zepazo__: Programa principal encargado del análisis de las grabaciones.
- __zepazoParams__: Programa que aporta una sencilla interfaz para el establecimiento asistido de parámetros.
- __zepazoVerify__: Programa encargado de verificar/validar los impactos de dos grabaciones con el objetivo de encontrar impactos en momentos temporales similares y validarlos.
- __zepazoCrop__: Programa que pretende aportar una herramienta de recorte de vídeos con el objetivo de no tener que descargar los vídeos completos del servidor para ajustar los parámetros haciendo uso del programa ZepazoParams.

### Instalación del conjunto de programas
Para instalar el conjunto de programas simplemente debemos tener instalado poetry el cual se puede instalar de la siguiente forma:
```
pip install poetry
```

Una vez instalado poetry podemos instalar todas las dependencias de nuestro programa simplemente ejecutando:

```
poetry install
```

__Nota__: Si al ejecutar el programa ZepazoParams se obtiene un error de compatibilidad de PyQt con OpenCv deberemos bajar la versión de OpenCv de la siguiente forma:

```
pip install opencv-python==4.3.0.36
```

### Zepazo
Es el programa principal cuyo objetivo es analizar un vídeo dado por un usuario en busca de los posibles impactos que hayan podido tomar lugar durante dicha grabación.


Este programa se ejecuta de la siguiente forma:

```
python3 src/zepazo.py [lista de argumentos]
```

Y contamos con la siguiente lista de argumentos para ajustar el proceso de análisis:

| Abreviatura |   Completo  |   Utilidad  | Tipo | Obligatoriedad | Ejemplo | Valor por defecto |
|---|---|---|---|---|---|---|
|-h| --help|Ayuda de parámetros. Se muestran los posibles parámetros que el programa puede utilizar| |Opcional| python3 src/zepazo.py -h| |
|-v|--video|Ruta del vídeo a analizar.| Cadena de caracteres| Obligatorio| python3 src/zepazo.py -v "/home/user/video_path"| |
|-d|--debug|Mostrar una simulación del proceso de análisis con los parámetros indicados, no se guardan los posibles impactos detectados| | Opcional | python3 src/zepazo.py -d | |
|-cm|--coordinatesmask| Lista de puntos indicando las coordenadas de las máscaras a añadir. Cada dos elementos de la lista indicará una máscara, de esta forma, el primer elemento de cada par de coordenadas será la esquina superior izquierda del rectángulo y el segundo será la esquina inferior derecha.| Lista de enteros. | Opcional | python3 src/zepazo.py -cm 1 2 3 4 | |
| -l | --detectionlimit | Índice de detección de impactos, este valor depende del brillo del vídeo introducido|Entero positivo|Opcional|python3 src/zepazo.py -l 30|50|
|-cl|--circlelimit|Valor que sirve para ajustar la elipse al contorno lunar, si no se establece el argumento, se calculará un valor por defecto|Entero positivo|Opcional| python3 src/zepazo.py -cl 17 |Calculado dinámicamente|
|-f|--folder| Ruta de la carpeta donde almacenar los fotogramas de los impactos detectados|Cadena de caracteres|Opcional|python3 src/zepazo.py -f "/home/user/path_to_folder"|Ubicación del vídeo|
|-ssf|--saveSurroundingFrames|Número de fotogramas previos y posteriores al impacto  que se desean almacenar, por defecto únicamente se almacena el fotograma del impacto. | Entero positivo | Opcional | python3 src/zepazo.py -ssf 2 | 0 |
|-dt|--dilate|Valor del kernel a utilizar para dilatar los fotogramas previos y evitar  falsos positivos derivados de movimiento y zonas luminosas de la luna|Entero positivo| Opcional|python3 src/zepazo.py -dt 3|0|
|-cf| --configFile|Ruta de un archivo de configuración generado por ZepazoParams para importar valores de los parámetros. |Cadena de caracteres. | Opcional | python3 src/zepazo.py -cf "/home/user/path_to_save" | Ubicación del vídeo |
|-sf| --startingFrame|Número de fotograma desde el que comenzar el análisis |  Entero positivo | Opcional | python3 src/zepazo.py -sf 122 | 0 |
|-ef| --endingFrame|Número de fotograma hasta el que realizar el análisis |  Entero positivo | Opcional |python3 src/zepazo.py -ef 600 | Último fotograma |

Una vez ajustados los argumentos comenzará el análisis y una vez que este concluya obtendremos en la carpeta seleccionada por argumentos los fotogramas se ha detectado un posible impacto así como un archivo de log que resume los posibles impactos encontrados tras el análisis realizado.

### ZepazoParams
Este programa pretende ayudar al usuario a ajustar los valores de los parámetros que se van a utilizar en el programa 'zepazo'  a tarvés de una sencilla interfaz.

Este programa se ejecuta de la siguiente forma:

```
python3 src/Interface/zepazo_params.py
```

Y al ejecutar lo anterior se nos abre la interfaz:

![ImagenInterfaz](imagenes_readme/interfaz.png)

En primer lugar para poder empezar a ajustar parámetros el usuario deberá seleccionar un vídeo haciendo uso del menú superior izquierdo 'Vídeo' y seleccionando la opción 'Open File' para elegir un vídeo. Una vez elegido un vídeo se mostrará el primer fotograma del mismo en la parte central de la interfaz:

![ImagenInterfaz](imagenes_readme/interfazFinal.png)


Una vez el vídeo ha sido seleccionado y contamos con una imagen del vídeo en pantalla, podemos empezar a ajustar parámetros de la siguiente forma (menu inferior):

- __Índice de detección__: por defecto presenta el valor de 50 y para vídeos con condiciones normales no debería variar mucho, no obstante puede aumentarse o disminuirse y pulsando al botón de la derecha con el símbolo de 'play' de la barra superior podremos ver como afecta el cambio de dicho valor.
- __Elipse__: En cuanto a la elipse que recubre la superficie lunar, por defecto viene activada la opción 'auto' la cual intenta obtener de forma automática una buena estimación. No obstante se puede desmarcar esta casilla y ajustar manualmente mediante el uso de la casilla numérica. Un ejemplo es el siguiente:
![ImagenInterfaz](imagenes_readme/elipse.png)
- __Dilate__: en este apartado podemos elegir si queremos o no dilatar los fotogramas de nuestro vídeo, es recomendable activar esta opción cuando en nuestro vídeo aparecen zonas iluminadas en la superficie lunar. Si se activa se podrá elegir el valor de dilatación en la casilla numérica y ver una previsualización mediante el botón 'play'.
- __Máscaras__: Este apartado nos permite añadir máscaras, eliminar o restablecer todas. Por ejemplo podríamos añadir las siguientes máscaras:
![ImagenInterfaz](imagenes_readme/masks.png)
- __Impactos__: Este apartado nos permite elegir tanto la carpeta donde guardar los impactos como adicionalmente elegir el número de impactos previos y posteriores a guardar cuando se detecta un impacto.


En cuanto al menú superior, encontramos las siguientes opciones (de izquierda a derecha):
- __Visualizar todos los parámetros__: Este botón que cuenta con el icono de un ojo, nos permite ver aplicados tanto las máscaras como la elipse al mismo tiempo ya que como hemos viso anteriormente, cuando se elijen máscaras únicamente se ven las máscaras y cuando se elije el valor de la elipse únicamente se ve la elipse, en este caso permite ver todo junto.
- __Restablecer todo__: Este segundo botón superior restablece a los valores por defecto todos los parámetros modificados.
- __Botón comando__: Al pulsar este botón obtenemos el comando completo con los parámetros seleccionados para lanzar el análisis con los valores elegidos así como se copia al clipboard. Un ejemplo es el siguiente:
![ImagenInterfaz](imagenes_readme/command.png)
- __Botón preview__: Este botón permite lanzar en modo debug el proceso de análisis para comprobar si los valores elegidos para los parámetros son correctos o no.


Adicionalmente, en el menú superior llamado 'Parameters' encontraremos la opción de importar parámetros a JSON o importar desde JSON.

### ZepazoVerify
Este programa pretende tras analizar dos vídeos que se han grabado en instantes temporales similares con el programa Zepazo, recoger los logs con el objetivo de identificar si existe alguna relación temporal entre los impactos del primer vídeo y los del segundo en cuanto a que ocurran en el mismo instante.

Este programa se ejecuta de la siguiente forma:

```
python3 src/zepazoVerify.py [lista de argumentos]
```

Y contamos con la siguiente lista de argumentos para ajustar el proceso de validación:

| Abreviatura |   Completo  |   Utilidad  | Tipo | Obligatoriedad |
|---|---|---|---|---|
|-lgf1|--logFile1|Log resultado del análisis del primer vídeo|Cadena de caracteres|Obligatorio|
|-lgf2| --logFile2|Log resultado del análisis del segundo vídeo|Cadena de caracteres|Obligatorio|
|-rlfg| --resultingLogFile|Ruta donde guardar el log resultante|Cadena de caracteres| Obligatorio|
|-mt|--marginTime|Margen temporal para que dos impactos con una diferencia indicada por este parámetro sean emparejados|Entero positivo|Obligatorio|

De esta forma si ejecutamos el comando: 

```
python3 src/zepazoVerify.py -lgf1 "/home/user/logs/log1.json" -lgf2 "/home/user/logs/log2.json" -rlfg "/home/user/logs/log_verify.json" -mt 10 
```

Estaríamos intentando validar los impactos del vídeo que ha generado el log1 con los del vídeo que ha generado el log2 emparejando los mismos con una diferencia temporal máxima de 10 segundos y almacenando el resultado en el fichero log_verify.json.

De esta forma el resultado obtenido tras ejecutar este programa es un fichero como por ejemplo el siguiente:

```
[
    {
        " difference " : 5 ,
        " log_1_impact " : 1 ,
        " log_2_impact " : 0 ,
        " path_to_log1 " : "../ test/log.json" ,
        " path_to_log2 " : "../ test/log2.json"
    }
]
```

Donde podemos ver que se ha validado un impacto ya que la diferencia temporal ha sido de 5 segundos, en el log1 el impacto ha sido el número 1, en el log2 el impacto ha sido el número 0 y se aporta información adicional de la ubicación de los logs por si fuese necesario consultar información concreta de los impactos emparejados.

### ZepazoCrop

Este programa nos permite recortar vídeos con el objetivo de no sobrecargar la red del servidor, ya que si un usuario desea descargar un vídeo para utilizar el programa zepazoParams con el objetivo de ajustar los parámetros para posteriormente lanzar el análisis no necesita tener el vídeo completo, con un fragmento breve es suficiente.

Este programa se ejecuta de la siguiente forma:

```
python3 src/zepazoCrop.py [lista de argumentos]
```

Y contamos con la siguiente lista de argumentos para ajustar el proceso de recorte:

| Abreviatura |   Completo  |   Utilidad  | Tipo | Obligatoriedad |
|---|---|---|---|---|
|-vo|--videoOriginal|Ruta del vı́deo a recortar|Cadena de caracteres|Obligatorio|
|-vc|--videoCropped|Ruta donde guardar el vı́deo recortado|Cadena de caracteres|Obligatorio|
|-ss|--secondStart|Segundo desde el que recortar el vı́deo|Entero positivo|Obligatorio|
|-se|--secondEnd|Segundo hasta el que recortar el vı́deo|Entero positivo|Obligatorio|

De esta forma si ejecutamos el comando: 

```
python3 src/zepazoCrop.py -vo "/home/user/videos/video1" -vc "/home/user/videos/video1_crop" -ss 120 -se 140
```

Estaríamos recortando el vídeo cuyo nombre es video1 desde el segundo 120 hasta el 140 y almacenándo el resultado con el nombre video1_crop.



## Execute unit tests
`poetry run task test`

### Execute unit tests with Dockerfile
`docker build . -t zepazo`


`docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix zepazo`
# Additional documentation
- [OpenCV instalation](https://github.com/antoniocuadros/zepazo/blob/main/docs/Tools/opencv.md)