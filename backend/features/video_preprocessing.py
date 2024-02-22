from spleeter.separator import Separator
from moviepy.editor import *
import os
from multiprocessing import freeze_support  # Step 1: Import freeze_support()

def convert_video_to_audio_and_split(local_video_path):
    # Ensure the output directory exists
    output_directory = r'E:\Integration_2024\backend\static\uploads'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Construct the output audio file path
    output_audio_path = os.path.join(output_directory, os.path.splitext(os.path.basename(local_video_path))[0] + '.wav')
    try:
        # Load the video file
        video = VideoFileClip(local_video_path)
        # Extract audio from the video
        audio = video.audio
        # Write the audio to a WAV file
        audio.write_audiofile(output_audio_path)
        # Close the video and audio objects to free resources
        video.close()
        audio.close()
        print("Video was successfully converted to audio")
        return output_audio_path  # Return the output audio path
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None
    # Initialize separator
    separator = Separator('spleeter:2stems')  # '2stems' separates into vocals and accompaniment (music)
    try:
        # Separate the audio
        separator.separate_to_file(output_audio_path, r'E:\Integration_2024\output\audio')
        print("Audio was successfully separated")
    except Exception as e:
        print(f"An error occurred during separation: {e}")

# Example usage
#def main():
    local_video_path = input("Enter the path to the video file: ")
    convert_video_to_audio_and_split(local_video_path)
#if __name__ == "__main__":
    freeze_support()  # Step 2: Call freeze_support()
    main()
