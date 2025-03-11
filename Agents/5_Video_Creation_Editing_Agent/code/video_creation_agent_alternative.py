"""
Video Creation Agent (Alternative)

Purpose: Creates videos from audio/text inputs using ffmpeg
Input: Voiceover file path, script outline file path
Output: Video file path
Dependencies: ffmpeg-python, os
"""

import os
import ffmpeg

def create_video(voiceover_file: str, script_outline_file: str) -> str:
    """Generates video combining audio and text content.
    
    Args:
        voiceover_file: Path to audio file
        script_outline_file: Path to text script file
        
    Returns:
        Path to generated video file
        
    Raises:
        FileNotFoundError: If input files are missing
        ffmpeg.Error: For video processing failures
    """
    output_video = "output_video_alt.mp4"
    
    if not os.path.exists(voiceover_file):
        raise FileNotFoundError(f"Voiceover file {voiceover_file} not found")
    if not os.path.exists(script_outline_file):
        raise FileNotFoundError(f"Script file {script_outline_file} not found")

    try:
        # Get audio duration
        probe = ffmpeg.probe(voiceover_file)
        duration = float(probe['format']['duration'])
        
        # Read script text
        with open(script_outline_file, "r", encoding="utf-8") as f:
            text = f.read().replace('\n', ' ')
        
        # Create video with text overlay
        black_video = ffmpeg.input(
            f'color=c=black:s=1280x720:d={duration}', 
            f='lavfi'
        )
        video_with_text = black_video.filter(
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
        
        # Add audio and render
        audio = ffmpeg.input(voiceover_file)
        ffmpeg.output(
            video_with_text, 
            audio, 
            output_video, 
            vcodec='libx264', 
            acodec='aac'
        ).run(overwrite_output=True)
        
        return output_video
        
    except ffmpeg.Error as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}") from e

if __name__ == '__main__':
    try:
        result = create_video("voiceover.mp3", "script.txt")
        print(f"Video created: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
