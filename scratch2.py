from audio.pipeline import AudioPipeline
import numpy as np
AUDIO_FILE = "C:\\Users\\2502780\\Desktop\\CLASS-2a-template-project\\audio\\ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"

pipelineInstance = AudioPipeline(file_path=AUDIO_FILE)


pipelineInstance.load()


pipelineInstance.position = ((len(pipelineInstance.signal) +1 ) / 2)
# print(pipelineInstance.position)

window = pipelineInstance.signal[int(pipelineInstance.position): (int(pipelineInstance.position) + 1024)]
currentWindow = (window * np.hanning(1024))
spectrum = np.fft.rfft(currentWindow)
spectrum_frequency = np.fft.fftfreq(len(currentWindow), 22050)
# print(len(spectrum))
# print(spectrum[0])
# print(spectrum[512])
# print(abs(spectrum))

print(f"this is the maximum index in the loud part {np.argmax(abs(spectrum))}")
maxindex = np.argmax(abs(spectrum))
maxfreq = spectrum_frequency[maxindex]
print(f"this is the frequency of the maximum index in the loud spectrum {maxfreq}")




pipelineInstance.position = (0)
# print(pipelineInstance.position)

window = pipelineInstance.signal[int(pipelineInstance.position): (int(pipelineInstance.position) + 1024)]
currentWindow = (window * np.hanning(1024))
spectrum = np.fft.rfft(currentWindow)
spectrum_frequency = np.fft.fftfreq(len(currentWindow), 22050)
# print(len(spectrum))
# print(spectrum[0])
# print(spectrum[512])
# print(abs(spectrum))

print(f"this is the maximum index in the quiet part {np.argmax(abs(spectrum))}")
maxindex = np.argmax(abs(spectrum))
maxfreq = spectrum_frequency[maxindex]
print(f"this is the frequency of the maximum index in the quiet spectrum {maxfreq}")

pipelineInstance.position = ((len(pipelineInstance.signal) +1 ) / 2)
#print(pipelineInstance.position)

window = pipelineInstance.signal[int(pipelineInstance.position): (int(pipelineInstance.position) + 1024)]
currentWindow = (window)
spectrum = np.fft.rfft(currentWindow)
spectrum_frequency = np.fft.fftfreq(len(currentWindow), 22050)
# print(len(spectrum))
# print(spectrum[0])
# print(spectrum[512])
# print(abs(spectrum))

print(f"this is the maximum index {np.argmax(abs(spectrum))}")
maxindex = np.argmax(abs(spectrum))
maxfreq = spectrum_frequency[maxindex]
print(f"this is the frequency of the maximum index in the spectrum {maxfreq}")