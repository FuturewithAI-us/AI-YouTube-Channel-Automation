#!/usr/bin/env python3
import os
import ffmpeg

def create_video():
    # Define paths
    base_dir = os.path.expanduser("~")
    voiceover_file = os.path.join(base_dir, 
"Documents/youtube/Agents/4_Voiceover_Audio_Agent/code/voiceover.aiff")
    script_outline_file = os.path.join(base_dir, 
"Documents/youtube/Agents/2_Scriptwriting_Outline_Agent/code/script_outline.txt")
    output_video = os.path.join(base_dir, 
"Documents/youtube/Agents/5_Video_Creation_Editing_Agent/code/final_video.mp4")

    # Check if required files exist
    if not os.path.exists(voiceover_file):
        print("Voiceover file not found. Please run the Voiceover/Audio Agent first.") 
        return
    if not os.path.exists(script_outline_file):
        print("Script outline file not found. Please run the Scriptwriting & Outline Agent first.") 
        return

    # Get audio duration using ffmpeg.probe
    try:
        probe = ffmpeg.probe(voiceover_file)
        duration = float(probe['format']['duration'])
    except Exception as e:
        print("Error obtaining audio duration:", e)
        return

    # Read the script outline text and replace newlines with spaces
    with open(script_outline_file, "r") as f:
        text = f.read().replace('\n', ' ')

    print("Audio duration:", duration)
    print("Script text:", text)

    # Create a black background video with the same duration as the audio using ffmeg's lavfi input
    black_video = ffmpeg.input('color=c=black:s=1280x720:d={}'.format(duration), f='lavfi')

    # Overlay text using the drawtext filter (adjust parameters as needed)
    video_with_text = black_video.filter('drawtext',
                                           text=text,
                                           fontsize=24,
                                           fontcolor='white',
                                           x='(w-text_w)/2',
                                           y='(h-text_h)/2',
                                           box=1,
                                           boxcolor='black@0.5',
                                           
enable='between(t,0,{})'.format(duration))

    # Load the audio file
    audio = ffmpeg.input(voiceover_file)

    # Combine video and audio into the final output
    try:
        out = ffmpeg.output(video_with_text, audio, output_video,
                            vcodec='libx264', acodec='aac', 
pix_fmt='yuv420p', shortest=None)
        ffmpeg.run(out, overwrite_output=True)
        print("Final video saved to", output_video)
    except ffmpeg.Error as e:
        print("ffmpeg error:", e.stderr.decode())

if __name__ == '__main__':
    create_video()

