import librosa
import numpy as np


AUDIO_FILE = "C:\\Users\\2502780\\Documents\\GitHub\\CLASS-2a-template-project\\audio\\ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"

y, sr = librosa.load(AUDIO_FILE)





cent = librosa.feature.spectral_centroid(y=y, sr = sr)
print(np.mean(cent))