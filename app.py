from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    # Save the audio file temporarily
    audio_path = 'temp_audio.wav'
    audio_file.save(audio_path)

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    # Convert speech to text using Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio_data)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Speech recognition could not understand the audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f"Could not request results from Google Speech Recognition service; {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
