import os
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
    flash,
)
from werkzeug.utils import secure_filename
from converter import Converter
import shutil



UPLOAD_FOLDER = "temp"
FLASK_ENV = "production"


app = Flask(__name__, static_url_path="/static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


if 'FLASK_ENV' == 'development':
    app.config['DEBUG'] = True
elif 'FLASK_ENV' == 'production':
    app.config['DEBUG'] = False



ALLOWED_DOCS_EXTENSIONS = {"doc","docx","odt","pptx","html","rtf","txt"}
ALLOWED_IMG_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff","webp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "wmv", "flv", "mkv","webm"}
ALLOWED_AUDIO_EXTENSIONS = {"aac","flac","mp3","opus","wav","mkv","webm"}


# Controlla se il percorso di upload esiste, altrimenti lo crea
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Controllo se l'estensione del file è consentita
def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# Route per visualizzare le varie pagine
@app.route("/")
def root():
    return redirect(url_for("homepage"))


@app.route("/convert/")
def homepage():
    clean()
    return render_template("convert.html")


@app.route("/convert/docs", methods=["GET"])
def docs_conversion():
    clean()
    return render_template("docs.html")


@app.route("/convert/image", methods=["GET"])
def image_conversion():
    clean()
    return render_template("images.html")


@app.route("/convert/video", methods=["GET"])
def video_conversion():
    clean()
    return render_template("video.html")


@app.route("/convert/audio", methods=["GET"])
def audio_conversion():
    clean()
    return render_template("audio.html")






# Convert the uploaded document to PDF
@app.route("/convert/docs", methods=["POST"])
def convert_docs():
    try:
        if "file" not in request.files:
            return redirect(url_for("error_page", message="No file part"))

        file = request.files["file"]

        # Verifica se è stato selezionato un file
        if file.filename == "":
            return redirect(url_for("error_page", message="No selected file"))

        # Verifica se l'estensione è consentita
        if file and allowed_file(file.filename, ALLOWED_DOCS_EXTENSIONS):
            filename = secure_filename(file.filename)
            input_filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            # Salva il file caricato
            file.save(input_filepath)

            # Converte il file in PDF
            outputfiledir = app.config["UPLOAD_FOLDER"]
            error = Converter.convert_to_pdf(input_filepath, outputfiledir)

            if error:
                return redirect(
                    url_for("error_page", message=f"Error during conversion: {error}")
                )

            # Nome del file PDF convertito
            pdf_filename = filename.rsplit(".", 1)[0] + ".pdf"

            # Reindirizza alla pagina di download
            return redirect(url_for("download_file", filename=pdf_filename))

        return redirect(url_for("error_page", message="Invalid file type"))

    except Exception as e:
        return redirect(url_for("error_page", message=str(e)))


@app.route("/convert/image", methods=["POST"])
def convert_image():
    try:
        if "file" not in request.files:
            return redirect(url_for("error_page", message="No file part"))

        file = request.files["file"]

        # Verifica se è stato selezionato un file
        if file.filename == "":
            return redirect(url_for("error_page", message="No selected file"))

        # Verifica se l'estensione è consentita
        if file and allowed_file(file.filename, ALLOWED_IMG_EXTENSIONS):
            filename = secure_filename(file.filename)
            input_filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(input_filepath)
            outputfiledir = app.config["UPLOAD_FOLDER"]
            
            error = Converter.convert_image(input_filepath,filename.rsplit(".", 1)[0]+"."+request.form.get("format"),outputfiledir)

            if error:
                return redirect(
                    url_for("error_page", message=f"Error during conversion: {error}")
                )


            # Reindirizza alla pagina di download
            return redirect(url_for("download_file", filename=filename.rsplit(".", 1)[0]+"."+request.form.get("format")))

        return redirect(url_for("error_page", message="Invalid file type"))

    except Exception as e:
        return redirect(url_for("error_page", message=str(e)))
   
   
@app.route("/convert/video", methods=["POST"])
def convert_video(): 

    try:
            if "file" not in request.files:
                return redirect(url_for("error_page", message="No file part"))

            file = request.files["file"]

            # Verifica se è stato selezionato un file
            if file.filename == "":
                return redirect(url_for("error_page", message="No selected file"))

            # Verifica se l'estensione è consentita
            if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
                filename = secure_filename(file.filename)
                input_filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(input_filepath)
                outputfiledir = app.config["UPLOAD_FOLDER"]

                error = Converter.convert_video(input_filepath,filename.rsplit(".", 1)[0]+"."+request.form.get("format"),outputfiledir)

                if error:
                    return redirect(
                        url_for("error_page", message=f"Error during conversion: {error}")
                    )


                # Reindirizza alla pagina di download
                return redirect(url_for("download_file", filename=filename.rsplit(".", 1)[0]+"."+request.form.get("format")))

            return redirect(url_for("error_page", message="Invalid file type"))

    except Exception as e:
        return redirect(url_for("error_page", message=str(e)))
    
@app.route("/convert/audio", methods=["POST"])
def convert_audio(): 

    try:
            if "file" not in request.files:
                return redirect(url_for("error_page", message="No file part"))

            file = request.files["file"]

            # Verifica se è stato selezionato un file
            if file.filename == "":
                return redirect(url_for("error_page", message="No selected file"))

            # Verifica se l'estensione è consentita
            if file and allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
                filename = secure_filename(file.filename)
                input_filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(input_filepath)
                outputfiledir = app.config["UPLOAD_FOLDER"]

                error = Converter.convert_video(input_filepath,filename.rsplit(".", 1)[0]+"."+request.form.get("format"),outputfiledir)

                if error:
                    return redirect(
                        url_for("error_page", message=f"Error during conversion: {error}")
                    )


                # Reindirizza alla pagina di download
                return redirect(url_for("download_file", filename=filename.rsplit(".", 1)[0]+"."+request.form.get("format")))

            return redirect(url_for("error_page", message="Invalid file type"))

    except Exception as e:
        return redirect(url_for("error_page", message=str(e)))
    



# Route to download the converted file
@app.route("/download/<filename>")
def download_file(filename):
    try:
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )
    except Exception as e:
        return redirect(url_for("error_page", message=str(e)))


# Clean file remnants
def clean():
    try:
        shutil.rmtree(app.config["UPLOAD_FOLDER"])
        os.makedirs(app.config["UPLOAD_FOLDER"])
        return render_template("convert.html")

    except FileNotFoundError:
        pass


# Route for error page
@app.route("/error")
def error_page():
    error_message = request.args.get("message", "An unknown error occurred.")
    return render_template("error.html", error_message=error_message)



if __name__ == "__main__":
    app.run()