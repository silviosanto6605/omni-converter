# 🔃 omni-converter

## A simple solution for file conversion 

# Overview

It's a simple web app that can convert several file types. 

File types supported:

- 📄 Documents (doc,docx,odt,pptx,html,rtf,txt) into PDF
- 🖼️ Images ("png", "jpg", "jpeg", "gif", "bmp", "tiff","webp")
- 📹 Video ("mp4", "avi", "mov", "wmv", "flv", "mkv","webm")
- 🎧 Audio ("aac","flac","mp3","opus","wav","mkv","webm")

# How to run it

The simplest way to run it would be to download the source code and run <br>
`docker compose up --build -d ` to build and run it. Subsequent starts will be easier, simply invoking<br>
### ` docker start omni-container `.


You can even pull only the image from Docker Hub:

[silviosanto/omni-converter](https://hub.docker.com/r/silviosanto/omni-converter)
or running: ` docker pull silviosanto/omni-converter `.

To run the image individually: ` docker run -p 8080:8080 -d silviosanto/omni-converter `.



# Requirements/other settings

If you are running everything from docker, you're all set! 
<br> If not, keep in mind the following things:

1. To run the server you should have installed the python packages in the requirements.txt file
2. You should have installed libreoffice and ffmpeg packages
3. The server runs by default on 0.0.0.0:8080, as specified in the gunicorn_config.py.

