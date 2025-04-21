import os
import openai
from flask import Flask, request, render_template
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

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

# ✅ Final com porta dinâmica para Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
