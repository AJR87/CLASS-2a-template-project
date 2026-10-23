from audio.pipeline import AudioPipeline
import numpy as np
AUDIO_FILE = "C:\\Users\\2502780\\Desktop\\CLASS-2a-template-project\\audio\\ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"

pipelineInstance = AudioPipeline(file_path=AUDIO_FILE)


pipelineInstance.load()


pipelineInstance.position = ((len(pipelineInstance.signal) +1 ) / 2)
print(pipelineInstance.position)

window = pipelineInstance.signal[int(pipelineInstance.position): (int(pipelineInstance.position) + 1024)]
currentWindow = (window * np.hanning(1024))
spectrum = np.fft.rfft(currentWindow)

print(spectrum)
