import os
import openai
from flask import Flask, request, render_template
import tempfile

# Usa a variável de ambiente segura
openai.api_key = os.getenv("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")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transcription = ""
    if request.method == 'POST':
        if 'audio' not in request.files:
            return render_template('index.html', transcription="No file uploaded.")

        file = request.files['audio']
        if file.filename == '':
            return render_template('index.html', transcription="Invalid file.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            file.save(tmp.name)
            audio_file = open(tmp.name, "rb")

            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

            transcription = response
            os.unlink(tmp.name)

    return render_template('index.html', transcription=transcription)

if __name__ == '__main__':
    app.run(debug=True)
