import os
import tempfile
from flask import Flask, request, render_template
from openai import OpenAIError, AuthenticationError, RateLimitError
import openai

# Lê a chave da API do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # Limite de 25MB

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    transcription = ""

    if request.method == 'POST':
        if 'audio' not in request.files:
            return render_template('index.html', transcription="No file uploaded.")

        file = request.files['audio']

        if file.filename == '':
            return render_template('index.html', transcription="Invalid file.")

        if not allowed_file(file.filename):
            return render_template('index.html', transcription="Type of document not supported.")

        file.seek(0, os.SEEK_END)
        if file.tell() == 0:
            return render_template('index.html', transcription="No audio available.")
        file.seek(0)

        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            file.save(tmp.name)
            temp_filename = tmp.name

        try:
            with open(temp_filename, "rb") as audio_file:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                transcription = response
        except AuthenticationError:
            transcription = "API key error. Contact your administrator."
        except RateLimitError:
            transcription = "OpenAI API usage limit exceeded. Try again later."
        except OpenAIError as e:
            transcription = f"OpenAI error: {str(e)}"
        except Exception as e:
            transcription = f"Unexpected error: {str(e)}"
        finally:
            os.unlink(temp_filename)  # Apaga o arquivo temporário após o uso

    return render_template('index.html', transcription=transcription)

# Suporte para Render (PORT dinâmico)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
