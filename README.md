# Evil YouTube 

## Instalación 

> *Por favor siga las instrucciones de instalación de este readme y lea las [consideraciones](#Consideraciones)*

### Windows 

> Para windows existen los binarios que pueden ser descargados mediante el archivo .zip desde el apartado **Releases**
> Descargue la ultima version para mejor experiencia de uso

Opcionalmente puede agregar un acceso directo a su escritorio si asi lo desea y mover la carpeta del binario donde desee

### Linux 

**Nota: el software nunca ha sido testeado en distribuciones Linux la compatibilidad podria afectar en la ejecucion**

> Actualmente no contamos con un binario establecido para todas las distribuciones de Linux, pero proximamente desarrollaremos
> un binario ejecutable para distribuciones Debian

Para instalar en linux para propositos de desarrollo:

<code>git clone https://github.com/Christianymoon/youtube_downloaderproject.git </code>



# Uso

## Video
- Abra la aplicación o ejecute el archivo principal de ejecucion si esta en un entorno de desarrollo
- Vaya a [YouTube](https://www.youtube.com/) y copie el link de el video de su preferencia
- pegue el link con **CTRL + V**
- Seleccione la opcion **High Quality** si lo desea a la maxima calidad posible
- Seleccione la opcion **Video** para que el software entienda que usted desea descargar un video y no una playlist
- De click en **Download** y espere a que se descarge su video
- **Voila!**

## Playlist

- Abra la aplicación o ejecute el archivo principal de ejecucion si esta en un entorno de desarrollo
- Vaya a [YouTube](https://www.youtube.com/) y copie el link de la playlist de su preferencia **tentiendo en cuenta las consideraciones**
- pegue el link con **CTRL + V**
- Seleccione la opcion **High Quality** si lo desea a la maxima calidad posible
- Seleccione la opcion **Playlist** para que el software entienda que descargara una playlist
- De click en **Download** y espere a que se descarge su playlist
- **Voila!**

## Consideraciones

> - El software de conversion de mp4 a mp3 es una apliacion independiente que requiere del software de codigo abierto [ffmpeg](https://www.ffmpeg.org/), el cual puede descargarse desde la misma aplicacion o puede hacerlo manualmente
> - El software de conversion requiere de un archivo script de PowerShell el cual necesita permisos de ejecucion para su funcionamiento
> - Las URL de Playlist deben estar **Pubilcas** de lo contrario, el software no indexara la playlist en la internet y no descargara la playlist

# Notas

> - **04/11/2024 - El proyecto depende de la libreria pytubefix en lugar de pytube por errores en la libreria de la version 15.0.0 puede instalar pytubefix desde pip3 <code>pip install pytubefix</code>**
