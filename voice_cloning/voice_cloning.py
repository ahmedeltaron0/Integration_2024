from TTS.api import TTS
import torch
from pydub import AudioSegment
from text_spliter import split_text
from language import check_lang

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def voice_cloning(input_audio,result,chunks):
    audio=input_audio
    lang =result
    print(lang)
    output_audio = AudioSegment.empty()
    for chunk in chunks:
        tts.tts_to_file(text=chunk,
                        file_path="output_temp.wav",
                        speaker_wav=audio,
                        language=lang)
        chunk_audio = AudioSegment.from_wav("output_temp.wav")
        output_audio += chunk_audio

    return output_audio.export("output_combined.wav", format="wav")