from moviepy.editor import *
import os

def convert_video_to_audio(local_video_path):
    output_directory = r'E:\Integration_2024\backend\static\uploads'
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Check if the local video file exists
    if not os.path.exists(local_video_path):
        print(f"Error: The specified video file does not exist: {local_video_path}")
        return None, None

    # Construct the output audio file path
    output_file_name = os.path.splitext(os.path.basename(local_video_path))[0] + '.wav'
    output_audio_path = os.path.join(output_directory, output_file_name)

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
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None, None

    return output_audio_path, output_directory

# Example usage
local_video_path =  r'E:\Integration_2024\backend\static\uploads\tested.mp4'
output_audio_path, output_directory = convert_video_to_audio(local_video_path)

if output_audio_path:
    print(f"Audio file was saved to: {output_audio_path}")
else:
    print("There was an error converting the video to audio.")