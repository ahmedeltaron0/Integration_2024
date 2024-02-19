from spleeter.separator import Separator
import os

# Initialize separator
separator = Separator('spleeter:2stems')  # '2stems' separates into vocals and accompaniment (music)

# Provide path to your audio file
audio_file_path = '-----------'

# Separate the audio
separator.separate_to_file(audio_file_path, 'output_folder')