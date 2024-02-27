from moviepy.editor import *
import os
# for laptop --> from multiprocessing import freeze_support  # Step 1: Import freeze_support()

def convert_video_to_audio_and_split(local_video_path):
    # Ensure the output directory exists
    output_directory = r'E:\Integration_2024\uploads'
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



# # Assuming the function definition and necessary imports are above this code
# ------> TESTING <------
# def test_convert_video_to_audio_and_split():
#     # Path to the sample video file
#     video_path = r'E:\Integration_2024\uploads\tested.mp4'

#     # Call the function to convert video to audio
#     output_audio_path = convert_video_to_audio_and_split(video_path)

#     # Check if the output audio file was created
#     if output_audio_path:
#         print("Audio file created successfully:", output_audio_path)
#     else:
#         print("Error occurred during conversion.")


# # Call the test function
# if __name__ == "__main__":
#     test_convert_video_to_audio_and_split()
