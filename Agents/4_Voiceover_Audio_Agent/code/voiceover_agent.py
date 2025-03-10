#!/usr/bin/env python3
import os
from TTS.api import TTS

def generate_voiceover():
    # Define the path to the script outline file from the Scriptwriting & Outline Agent
    outline_file = os.path.join(
        os.path.expanduser("~"),
        "Documents/youtube/Agents/2_Scriptwriting_Outline_Agent/code/script_outline.txt"
    )
    
    # Check if the file exists
    if not os.path.exists(outline_file):
        print("Script outline file not found. Please run the Scriptwriting & Outline Agent first.")
        return
    
    # Read and preprocess the script outline text
    with open(outline_file, "r") as f:
        text = f.read()
    # Replace newlines with spaces and periods with commas to reduce long pauses
    text = text.replace("\n", " ").replace(". ", ", ")

    print("Generating voiceover for the following text:")
    print(text)
    
    # Initialize the Coqui TTS model using the VCTK-based VITS model.
    # Experiment with different speaker IDs for a deeper, calming male voice.
    tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True, gpu=False)
    
    # Define the output file (using .wav format)
    output_file = os.path.join(
        os.path.expanduser("~"),
        "Documents/youtube/Agents/4_Voiceover_Audio_Agent/code/voiceover.wav"
    )
    
    try:
        # Specify a male speaker ID (try "p227" as an example)
        tts.tts_to_file(text=text, file_path=output_file, speaker="p227")
        print("Voiceover saved to", output_file)
    except Exception as e:
        print("Error generating voiceover:", e)

if __name__ == '__main__':
    generate_voiceover()
