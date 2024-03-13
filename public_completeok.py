#funziona bene e riesce a riprendere dal punto se bloccato


import time
from pathlib import Path
import fitz  # PyMuPDF
import spacy
from pydub import AudioSegment
import openai
import os
import re
import pygame
from tqdm import tqdm  # Importa tqdm per la barra di progresso

# Configurazione iniziale
OPENAI_API_KEY = "openai_api_insert_here"
openai.api_key = OPENAI_API_KEY
#nlp = spacy.load("en_core_web_sm")  # O use 'it_core_news_sm' for italian
nlp = spacy.load("it_core_news_sm")  # per l'italiano <---

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def pdf_to_text(pdf_path):
    print("transforming pdf into text...")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print("transformation complete.")
    return text

def text_to_sentences(text):
    print("dividing sentences..")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    print(f"found {len(sentences)} non empty sentences.")
    return sentences

def find_starting_point(output_dir):
    files = sorted(Path(output_dir).glob('sentence_*.mp3'), key=os.path.getmtime)
    if not files:
        return 0  # no file, strat form 0
    last_file_name = files[-1].stem
    last_index = int(re.search(r'(\d+)', last_file_name).group())
    return last_index + 1  # resuming from the ohrese next to the last one


def play_most_recent_mp3(output_dir): #with this function I start the most recent file if I had already run the program
    pygame.mixer.init()
    
    # Gets the list of all files in the specified directory
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.mp3')]
    
    # if there are no files, the function ends
    if not files:
        print("no mp3 file in directory.")
        return

    # Sorts files by last modified date, from newest to oldest
    files.sort(key=os.path.getmtime, reverse=True)
    
    # select most recent
    most_recent_file = files[0]
    
    # print file name 
    print(f"Riproduzione del file più recente: {most_recent_file}")
    
    # upload and start mp3
    pygame.mixer.music.load(most_recent_file)
    pygame.mixer.music.play()
    
    # whait for the end
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def confirm_starting_sentence(sentences, start_index):
    if start_index > 0 and start_index < len(sentences):
        play_most_recent_mp3(output_dir)
        print(f"last phrase is: \"{sentences[start_index-1][:50]}...\", right? (Y/N)")
        response = input().strip().upper()
        if response == 'N':
            play_most_recent_mp3(output_dir)
            return search_and_confirm_sentence(sentences)
    return start_index

def search_and_confirm_sentence(sentences):
    while True:
        search_term = input("Enter keywords to search for the phrase: ").strip()
        matches = [s for s in sentences if search_term.lower() in s.lower()]

        if not matches:
            print("Phrase not found. Do you want to (1) search again, (2) start from the beginning, (3) exit the program, (4) audio replay?")
            choice = input().strip()
            if choice == '1':
                continue
            elif choice == '2':
                return 0
            elif choice == '4':
                play_most_recent_mp3(output_dir)
                continue
            elif choice == '3':
                exit()
        else:
            for i, match in enumerate(matches):
                print(f"Match {i+1}: \"{match[:50]}...\". Do you want to start from this sentence? (Y/N), (N)new search, (P) next match, (R) audio replay?")
                decision = input().strip().upper()
                if decision == 'Y':
                    return sentences.index(match)
                elif decision == 'N':
                    break
                elif decision == 'R':
                    play_most_recent_mp3(output_dir)
                    continue
                elif decision == 'P':
                    continue

def generate_audio_files(sentences, output_dir, start_from):
    print(f"Start generating audio files from the phrase {start_from + 1}...")
    ensure_directory_exists(output_dir)
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    audio_files = []
    
    # Wrap the sentence iteration with tqdm to display the progress bar
    for i in tqdm(range(start_from, len(sentences)), desc="Generazione audio", unit="frase"):
        sentence = sentences[i]
        # Salta la frase se è vuota o contiene solo spazi bianchi
        if not sentence.strip():
            continue
        tqdm.write(f"Vocalizing the phrase {i+1} of {len(sentences)}: \"{sentence[:50]}...\"")  # use tqdm.write to print
        time.sleep(1.4)  # I slow down to respect the openai limits https://platform.openai.com/account/limits
        
        try:
            response = client.audio.speech.create(
                model="tts-1-1106",  # change model if needed
                voice="shimmer",
                input=sentence
            )
            #audio_path = Path(output_dir) / f"sentence_{start_from}_{i}.mp3"
            audio_path = Path(output_dir) / f"sentence_{i}.mp3"
            # Usa stream_to_file per salvare il file audio
            response.stream_to_file(str(audio_path))
            audio_files.append(audio_path)
        except Exception as e:
            tqdm.write(f"Errore durante la generazione dell'audio per la frase {i+1}: {e}. Attendo 60 secondi prima di continuare.")
            time.sleep(60)
    
    print("Generazione dei file audio completata.")
    return audio_files



def merge_audio_files(audio_files, output_path):
    print("Sto ordinando i file audio in base alla data dell'ultima modifica...")
    
    # Ordina i file in base alla data dell'ultima modifica (dal più vecchio al più recente)
    audio_files.sort(key=lambda file: os.path.getmtime(file))
    
    print("Sto unendo i file audio in un unico file...")
    combined = AudioSegment.empty()
    
    # Per ogni file audio nell'elenco ordinato
    for audio_file in audio_files:
        # Carica il file audio
        sound = AudioSegment.from_mp3(audio_file)
        # Aggiunge il suono al segmento audio combinato
        combined += sound
        
    # Esporta il file audio combinato
    combined.export(output_path, format="mp3")
    print(f"File audio finale salvato in {output_path}")

# Percorso del file PDF da convertire
pdf_path = "/user/my/bok/path/mybook.pdf"
# Directory dove salvare i file audio temporanei
output_dir = "./audio_files"
# File audio finale
output_audio_path = "./myboook_audiofile.mp3"

print("SVUOTA LA CARTELLA OUTPUT TEMP!!! RICORDATI!!!")
text = pdf_to_text(pdf_path)
sentences = text_to_sentences(text)
starting_index = find_starting_point(output_dir)
starting_index = confirm_starting_sentence(sentences, starting_index)
#starting_index = starting_index + 1 #senza questa linea viene generata due volte la frase iniziale se si riparte
#audio_files = generate_audio_files(sentences, output_dir, starting_index) #funzionava solo unendo però i file dall'ultimo avvio
generate_audio_files(sentences, output_dir, starting_index) #con questo comando genero i file con le vaire frasi
audio_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith("sentence")] #elenca tutti i file che iniziano con "sentece" in generale
merge_audio_files(audio_files, output_audio_path)
