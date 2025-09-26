import numpy as np
import librosa
import soundfile as sf

def preprocess_wav(fpath_or_wav, source_sr=None):
    wav, sr = librosa.load(fpath_or_wav, sr=None)
    if source_sr is not None and sr != source_sr:
        wav = librosa.resample(wav, orig_sr=sr, target_sr=source_sr)
    return wav
