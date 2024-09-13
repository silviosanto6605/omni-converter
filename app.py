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
import dotenv
import shutil

app = Flask(__name__)

dotenv.load_dotenv(".env")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

ALLOWED_TEXT_TO_PDF_EXTENSIONS = {
    "doc",
    "docx",
    "odt",
    "pptx",
    "html",
    "rtf",
    "txt",
}  # Estensioni consentite


# Controlla se il percorso di upload esiste, altrimenti lo crea
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Controllo se l'estensione del file è consentita
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_TEXT_TO_PDF_EXTENSIONS
    )


# Route per visualizzare il form di upload
@app.route("/")
def upload_form():
    return render_template("index.html")


# Route per caricare e convertire il file
@app.route("/upload", methods=["POST"])
def upload_and_convert_file():
    try:
        if "file" not in request.files:
            return redirect(url_for("error_page", message="No file part"))

        file = request.files["file"]

        # Verifica se è stato selezionato un file
        if file.filename == "":
            return redirect(url_for("error_page", message="No selected file"))

        # Verifica se l'estensione è consentita
        if file and allowed_file(file.filename):
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


# Route per scaricare il file convertito
@app.route("/uploads/<filename>")
def download_file(filename):
    try:
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )
    except Exception as e:
        return redirect(url_for("error_page", message=str(e)))

    finally:
        clean()


def clean():
    try:
        shutil.rmtree(app.config["UPLOAD_FOLDER"])
        os.makedirs(app.config["UPLOAD_FOLDER"])
        return render_template("index.html")

    except FileNotFoundError:
        return redirect(url_for("error_page", message="No files to delete"))


# Route per la pagina di errore
@app.route("/error")
def error_page():
    error_message = request.args.get("message", "An unknown error occurred.")
    return render_template("error.html", error_message=error_message)
