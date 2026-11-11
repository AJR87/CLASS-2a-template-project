import librosa
import numpy as np
from audio.pipeline import AudioPipeline

AUDIO_FILE = "/Users/ajr/Documents/CLASS-2a-template-project/audio/ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"
pipelineInstance = AudioPipeline(file_path=AUDIO_FILE)

pipelineInstance.load()

pipelineInstance.position = 0
window = pipelineInstance.signal[int(pipelineInstance.position) : (int(pipelineInstance.position) + 1024)]

# for i in range(1, 51):
#     data = pipelineInstance.get_features()
#     amp = data["amplitude"]
#     if i % 10 == 0:
#         print(f"this is the amplitude: {amp}")
#     elif i == 0:
#         print(f"this is the amplitude: {amp}")

ampList = []
bassList = []
midList = []
trebleList = []
centList = []


for i in range(0 , len(pipelineInstance.signal), 1024):
    data = pipelineInstance.get_features()
    amp = data["amplitude"]
    ampList.append(amp)

ampRange = (max(ampList) - min(ampList))
print(ampRange) 

pipelineInstance.position = 0

for i in range(0 , len(pipelineInstance.signal), 1024):
    data = pipelineInstance.get_features()
    bass = data["bass"]
    bassList.append(bass)

bassRange = (max(bassList) - min(bassList))
print(bassRange) 

pipelineInstance.position = 0

for i in range(0 , len(pipelineInstance.signal), 1024):
    data = pipelineInstance.get_features()
    mid = data["mid"]
    midList.append(mid)

midRange = (max(midList) - min(midList))
print(midRange)

pipelineInstance.position = 0

for i in range(0 , len(pipelineInstance.signal), 1024):
    data = pipelineInstance.get_features()
    treble = data["treble"]
    trebleList.append(treble)

trebleRange = (max(trebleList) - min(trebleList))
print(trebleRange) 

pipelineInstance.position = 0

for i in range(0 , len(pipelineInstance.signal), 1024):
    data = pipelineInstance.get_features()
    cent = data["cent"]
    centList.append(cent)

centRange = (max(centList) - min(centList))
print(centRange) 
