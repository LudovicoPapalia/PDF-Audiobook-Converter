import time

#time.sleep(60*60)

# funziona! Converte il paper (path da definire) in un audio super naturale

from pathlib import Path
import fitz  # PyMuPDF
import spacy
from pydub import AudioSegment
import openai
import os

# Configurazione iniziale
OPENAI_API_KEY = "openai_api_insert_here"
openai.api_key = OPENAI_API_KEY
#nlp = spacy.load("en_core_web_sm")  # O usa 'it_core_news_sm' per l'italiano
nlp = spacy.load("it_core_news_sm")  # per l'italiano <---

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def pdf_to_text(pdf_path):
    print("Sto trasformando il PDF in testo...")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print("Trasformazione completata.")
    return text

def text_to_sentences(text):
    print("Sto dividendo il testo in frasi...")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    print(f"Trovate {len(sentences)} frasi.")
    return sentences

def generate_audio_files(sentences, output_dir):
    print("Inizio della generazione dei file audio...")
    ensure_directory_exists(output_dir)  # Assicurati che la directory esista
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    audio_files = []
    for i, sentence in enumerate(sentences):
        # Salta la frase se è vuota o contiene solo spazi bianchi
        if not sentence.strip():
            continue
        print(f"Vocalizzando la frase {i+1} di {len(sentences)}: \"{sentence[:50]}...\"")
        time.sleep(1.3)  # Rallento di 1.3 secondi per rispettare i limiti di rateo
        try:
            response = client.audio.speech.create(
                model="tts-1", #change if needed
                voice="shimmer",
                input=sentence
            )
            audio_path = Path(output_dir) / f"sentence_{i}.mp3"
            # Usa stream_to_file per salvare il file audio
            response.stream_to_file(str(audio_path))
            audio_files.append(audio_path)
        except Exception as e:  # Cattura qualsiasi tipo di errore
            print(f"Errore durante la generazione dell'audio per la frase {i+1}: {e}. Attendo 60 secondi prima di continuare.")
            time.sleep(60)  # Attende 60 secondi prima di continuare con la prossima frase
    print("Generazione dei file audio completata.")
    return audio_files


def merge_audio_files(audio_files, output_path):
    print("Sto unendo i file audio in un unico file...")
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        sound = AudioSegment.from_mp3(audio_file)
        combined += sound
    combined.export(output_path, format="mp3")
    print(f"File audio finale salvato in {output_path}")

# Percorso del file PDF da convertire
pdf_path = "/user/my/bok/path/mybook.pdf"
# Directory dove salvare i file audio temporanei
output_dir = "./audio_files"
# File audio finale
output_audio_path = "./myboook_audiofile.mp3"

text = pdf_to_text(pdf_path)
sentences = text_to_sentences(text)
audio_files = generate_audio_files(sentences, output_dir)
merge_audio_files(audio_files, output_audio_path)
