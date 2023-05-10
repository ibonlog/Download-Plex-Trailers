# Download Plex Trailers

Este programa descarga trailers de YouTube para películas y series que se almacenan en una carpeta especificada. El programa utiliza la API de YouTube para buscar videos y la biblioteca yt_dlp para descargar videos. También utiliza el paquete dotenv para cargar una variable de entorno que contiene la clave de API de YouTube. Las películas y series deben estar en directorios con los nombres de las peliculas de forma legible y el fichero de la pelicula igualmente legible. Las series estarán gerarquicamente orgranizadas por SerieName/Season X/ donde se creará un directorio SerieName/Trailers.

Este script se ha creado para obtener los trailers para España, puedes adaptarlo a tus necesidades de búsqueda de tu país.

## Requerimientos

Disponer de una clave API de Youtube. 

Para obtener una clave válida de acceso al API de YouTube, debes seguir los siguientes pasos:

1. Ve a la web de las APIs de Google e inicia sesión con tu cuenta de [Google Cloud](https://console.cloud.google.com/cloud-resource-manager).

2. Haz clic en el enlace "Crear Proyecto" situado en la parte superior de la ventana. Dale un nombre a tu proyecto y haz clic en el botón "Crear".

3. Haz clic en el enlace "Biblioteca" de la izquierda, en el menú de navegación. Debajo de la sección de las APIs de YouTube, haz clic en el enlace "YouTube Data API".

Organizacion de carpetas y archivos, para que el funcionamiento automatizado y que busque y encuentre las películas y series es necesario que las peliculas y series esten guardadas con la siguiente estructura:

- peliculas/
    - (nombre película 1)/
        - (nombre fichero película 1).(.mkv,.avi,.mp4)
    - (nombre película 2)/
        - (nombre fichero película 2).(.mkv,.avi,.mp4)
- series/
    - (nombre serie 1)/
        - Season 1/
            - (nombre capítulo 1).(.mkv,.avi,.mp4)
            - (nombre capítulo 2).(.mkv,.avi,.mp4)
        - Season 2/
            - (nombre capítulo 1).(.mkv,.avi,.mp4)
            - (nombre capítulo 2).(.mkv,.avi,.mp4)
    - (nombre serie 2)/
        - Season 1/
            - (nombre capítulo 1).(.mkv,.avi,.mp4)
            - (nombre capítulo 2).(.mkv,.avi,.mp4)
        - Season 2/
            - (nombre capítulo 1).(.mkv,.avi,.mp4)
            - (nombre capítulo 2).(.mkv,.avi,.mp4)


## Uso

El programa acepta dos argumentos de línea de comando: la ruta de la carpeta de búsqueda y el número máximo de descargas a realizar en la misma llamada. Ejecutar el programa con el siguiente comando:

`
python youtube_trailer_downloader.py <search_path> <downloads_limit>
`

Se necesita un fichero .env con las variables de entorno que usarán tanto el script python como el docker-compose:
```
YOUTUBE_API_KEY=
# only for use with docker-compose from here ...
SEARCH_PATH_FILMS=/home/john/media/films
SEARCH_PATH_SHOWS=/home/john/media/shows
# SCHEDULE E.g. @every 10s, @every 1m, @every 1h30m, @hourly, @daily, @weekly, @midnight
SCHEDULE=@every 5m
```


## Instalación

Para instalar las dependencias, ejecute el siguiente comando en la terminal:

`
pip install -r requirements.txt
`

## Dockerized

Si se usa con Docker o docker-compose 

Para ver la salida de logs y poder depurar:

`
docker logs -f trailers-cron
`

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
