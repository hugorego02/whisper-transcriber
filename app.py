import os
import openai
from flask import Flask, request, render_template
import tempfile

# Sua chave da OpenAI (pode proteger depois com variável de ambiente)
openai.api_key = "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"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transcription = ""
    if request.method == 'POST':
        if 'audio' not in request.files:
            return render_template('index.html', transcription="Nenhum arquivo enviado.")

        file = request.files['audio']
        if file.filename == '':
            return render_template('index.html', transcription="Arquivo inválido.")

        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name  # salva o caminho para usar depois

        # Abre o arquivo para enviar à OpenAI
        with open(tmp_path, "rb") as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        transcription = response
        os.unlink(tmp_path)  # apaga o arquivo temporário

    return render_template('index.html', transcription=transcription)

if __name__ == '__main__':
    app.run(debug=True)
