# PDF-to-Audiobook-Converter

This Python program transforms PDF documents into audiobooks. 
Leveraging the capabilities of various libraries, it extracts text from PDF files, splits the text into sentences, and converts these sentences into spoken audio. If the process is interrupted, the program can resume from the last processed sentence, making it efficient for large documents.

The program uses the latest openai technology for text to speech and the pronunciation is quite natural (at least in Italian and English). The language detection is based on the text provided. The use of this script allows you to transform papers and your own documents into text without having to use very expensive special services. Unfortunately, to date it is not able to remove notes in the text and at the foot of the page.

# Main Features
- PDF Text Extraction: Converts entire PDF documents into text.
- Sentence Segmentation: Utilizes Spacy for accurate sentence segmentation, catering to the Italian language.
- Audio Generation: Transforms text sentences into audio files using OpenAI's GPT-3 model for a natural sounding voice.
- Progress Resumption: Capable of resuming audio file generation from the last processed sentence, preventing the need to start over.
- Audio File Management: Automatically merges individual sentence audio files into a single audiobook file.
- Interactive Search: Allows users to find and resume from a specific sentence using search keywords.

# How It Works
- Setup: Initialize with your OpenAI API key and choose the working directories.
- PDF to Text: The program reads a PDF file and converts its content into plain text.
- Text to Sentences: Utilizing Spacy, the text is divided into individual sentences.
- Finding the Starting Point: If the program is restarted, it finds the last generated sentence and offers to resume.
- Sentence to Audio: Each sentence is converted into an individual audio file using OpenAI's GPT-3 voice synthesis.
- Audio File Management: Finally, all sentence audio files are merged into a single audiobook file.

# Usage
- Insert your OpenAI API key in the OPENAI_API_KEY variable.
- Adjust the pdf_path, output_dir, and output_audio_path variables to your needs.
- Run the script. It will guide you through the process, offering resumption and search functionalities as needed.

# Requirements 
(requirements.txt file not included)

PyMuPDF
fitz
spacy
pydub
openai
pygame
tqdm
pathlib

# Translations
Main print statements have been translated into English below for clarity:

- "transforming pdf into text..." ➔ "Transforming PDF into text..."
- "dividing sentences..." ➔ "Dividing text into sentences..."
- "no mp3 file in directory." ➔ "No MP3 file found in the directory."
- "Riproduzione del file più recente: {most_recent_file}" ➔ "Playing the most recent file: {most_recent_file}"
- "Start generating audio files from the phrase {start_from + 1}..." ➔ "Starting audio file generation from sentence {start_from + 1}..."
- "Generazione dei file audio completata." ➔ "Audio file generation completed."
- "Sto ordinando i file audio in base alla data dell'ultima modifica..." ➔ "Sorting audio files by last modification date..."
- "Sto unendo i file audio in un unico file..." ➔ "Merging audio files into a single file..."
- "File audio finale salvato in {output_path}" ➔ "Final audio file saved at {output_path}"
- "SVUOTA LA CARTELLA OUTPUT TEMP!!! RICORDATI!!!" ➔ "CLEAR THE TEMP OUTPUT FOLDER!!! REMEMBER!!!"




# public_complete.py and public_simple.py differences

## Overview
Both `public_complete.py` and `public_simple.py` scripts are designed to convert text from PDF documents into audio format using OpenAI's text-to-speech technology. The primary aim is to make written content more accessible by providing an auditory version, benefiting users who prefer auditory learning or require it for convenience.

## `public_complete.py` - The Comprehensive Tool
This script is the more intricate of the two, offering additional features for enhanced user experience and flexibility.

### Key Features:
- **Resumption Capability:** Enables the script to continue from where it left off, which is particularly useful in cases of interruption.
- **Interactive Sentence Confirmation:** Allows users to confirm the starting sentence or search for a specific sentence to begin from before proceeding with audio generation. This feature enhances both accuracy and user control.
- **Progress Tracking:** Incorporates a progress bar via tqdm, offering visual feedback on the conversion process.
- **Audio File Management:** Organizes the generated audio files by sentence, making navigation through the output easier.
- **Error Handling and Rate Limit Management:** Implements mechanisms for sleep intervals and error handling to efficiently manage API rate limits and ensure a smooth operation.

### Operation:
The script first converts the PDF document into text, then splits the text into sentences. It identifies the starting point for resumption, confirms this starting point with the user, generates audio files for each sentence from the selected point, and finally merges these into a single audio file.

## `public_simple.py` - The Streamlined Version
A more straightforward version, focusing on the core functionality without the advanced features of its counterpart.

### Key Features:
- **Simplified Workflow:** Directly converts a PDF document to text, splits the text into sentences, generates audio for each sentence, and then merges them into a single audio file. This version lacks the interactive components of the comprehensive tool.
- **Basic Error Handling:** Includes basic mechanisms for error handling and rate limit management but does not offer the interactive and resumption capabilities found in the comprehensive version.

### Operation:
Operates in a similar manner to `public_complete.py` but lacks the functionality for resuming from a specific point, confirming starting sentences, or managing the process interactively. It processes the entire document in a straightforward, linear fashion.

## Differences Between the Scripts
- **Interactivity:** `public_complete.py` provides an interactive approach, allowing users to choose where the audio generation starts. `public_simple.py` processes the document in a linear manner without such interactions.
- **Resumption Capability:** Only the comprehensive script has the ability to resume processing from a specific sentence.
- **User Feedback:** `public_complete.py` enhances the user experience with progress bars and interactive sentence confirmation.
- **Error and Rate Limit Management:** The comprehensive script incorporates more sophisticated error handling and rate limit management, facilitating smoother operation over longer sessions.




