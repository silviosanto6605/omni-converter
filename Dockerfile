# Impostare l'immagine di base
FROM python:3.10-slim

RUN mkdir /app
# Installare LibreOffice e FFmpeg
RUN apt-get update && \
    apt-get install -y libreoffice ffmpeg gcc zlib1g-dev libjpeg-dev  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Impostare il direttorio di lavoro
WORKDIR /app

# Copiare i file requirements.txt
COPY requirements.txt requirements.txt

# Installare le dipendenze Python
RUN pip install -r requirements.txt

# Copiare il resto dei file dell'applicazione
COPY . .

# Esporre la porta necessaria
EXPOSE 8080

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]
