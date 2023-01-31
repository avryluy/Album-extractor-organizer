# Album-extractor-organizer

This python script will unzip a music album, parse artist and album name, and organize it into your music library. 
The intention behind this was to speed up the downloading and organizing of music purchased from BandCamp, but could be used in other music-downloading scenarios as well.
 Audio files will be trimmed to remove Album Artist - Album Name from the file title.

## Supported audio file extentions
- .wav
- .mp3
- .aac
- .flac
- .ogg
- .alac
- .aiff

## Configuration
1. Download the python file and store it in a location accessible by your systems PATH variables. \
*ex. C:\Users\username\AppData\Local\Programs\Python\Python311\Scripts*
2. Open the python file in a text editor. You will need to set your own directory paths.
3. Set your download path:
```py 
downloadPath = path.Path(r"path/to/directory")
```
4. Set your music library path:
```py
musicLibrary = path.Path(r"path/to/directory")
```
5. Save and close
6. Use the win+R command to open the run window
7. type "AlbumExtractor.py" and hit enter. The program will execute. \
![image](https://user-images.githubusercontent.com/40475826/215841886-ab3a10f1-0790-4796-a598-7c949abc4d3b.png)
