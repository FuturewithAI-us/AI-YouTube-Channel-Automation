"""
Video Creation Agent (Alternative)

Purpose:
    Creates videos by combining a voiceover audio file with a text script overlay using ffmpeg.
Input:
    - voiceover_file: Path to the voiceover audio file.
    - script_outline_file: Path to the text file containing the script.
Output:
    - Returns the path to the generated video file.
Dependencies:
    - ffmpeg-python
    - os
    - logging
"""

import os
import ffmpeg
import logging

logging.basicConfig(level=logging.INFO)

def create_video(voiceover_file: str, script_outline_file: str, output_video: str = "output_video_alt.mp4") -> str:
    """
    Generates a video by overlaying text on a black background and adding a voiceover.

    Args:
        voiceover_file (str): Path to the audio file.
        script_outline_file (str): Path to the text script file.
        output_video (str): Path for the output video file (default: "output_video_alt.mp4").

    Returns:
        str: The path to the generated video file.

    Raises:
        FileNotFoundError: If the voiceover or script file is missing.
        RuntimeError: If an error occurs during video processing.
    """
    # Validate that the input files exist
    if not os.path.exists(voiceover_file):
        raise FileNotFoundError(f"Voiceover file {voiceover_file} not found")
    if not os.path.exists(script_outline_file):
        raise FileNotFoundError(f"Script file {script_outline_file} not found")
    
    try:
        # Get audio duration from the voiceover file
        probe = ffmpeg.probe(voiceover_file)
        duration = float(probe['format']['duration'])

        # Read the script text with explicit UTF-8 encoding
        with open(script_outline_file, "r", encoding="utf-8") as file:
            text = file.read().replace('\n', ' ')

        # Create a black background video using ffmpeg's lavfi input with the specified duration
        black_video = ffmpeg.input(f"color=c=black:s=1280x720:d={duration}", f="lavfi")

        # Apply a text overlay filter on the black video
        video_with_text = (
            black_video.filter(
                'drawtext',
                text=text,
                fontsize=24,
                fontcolor='white',
                x='(w-text_w)/2',
                y='(h-text_h)/2',
                box=1,
                boxcolor='black@0.5',
                enable=f'between(t,0,{duration})'
            )
        )

        # Add the audio input from the voiceover file
        audio = ffmpeg.input(voiceover_file)

        # Combine video and audio into the final output file
        ffmpeg.output(
            video_with_text,
            audio,
            output_video,
            vcodec='libx264',
            acodec='aac'
        ).run(overwrite_output=True)

        logging.info(f"Video created successfully: {output_video}")
        return output_video

    except ffmpeg.Error as error:
        error_message = error.stderr.decode('utf-8') if error.stderr else str(error)
        logging.error(f"FFmpeg error: {error_message}")
        raise RuntimeError(f"FFmpeg error: {error_message}") from error

if __name__ == "__main__":
    try:
        result = create_video("voiceover.mp3", "script.txt")
        print(f"Video created: {result}")
    except Exception as e:
        print(f"Error: {e}")
