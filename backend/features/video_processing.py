from spleeter.separator import Separator
from multiprocessing import freeze_support

if __name__ == '__main__':
    # Call freeze_support() to ensure correct multiprocessing behavior
    freeze_support()

    # Initialize separator
    separator = Separator('spleeter:2stems')  # '2stems' separates into vocals and accompaniment (music)

    # Provide path to your audio file
    audio_file_path = r'E:\Integration_2024\backend\static\uploads\tested.wav'
    # Separate the audio
    separator.separate_to_file(audio_file_path, r'E:\Integration_2024\output\audio')
