import librosa
import numpy as np
from audio.pipeline import AudioPipeline

AUDIO_FILE = "/Users/ajr/Documents/CLASS-2a-template-project/audio/ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"
pipelineInstance = AudioPipeline(file_path=AUDIO_FILE)

pipelineInstance.load()

pipelineInstance.position = 0
window = pipelineInstance.signal[int(pipelineInstance.position) : (int(pipelineInstance.position) + 1024)]




pipelineInstance.get_features()