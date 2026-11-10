import librosa
from audio.pipeline import AudioPipeline
import numpy as np


AUDIO_FILE = "C:\\Users\\2502780\\Documents\\GitHub\\CLASS-2a-template-project\\audio\\ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"

y, sr = librosa.load(AUDIO_FILE)

pipelineInstance = AudioPipeline(file_path=AUDIO_FILE)


pipelineInstance.load()


pipelineInstance.position = ((len(pipelineInstance.signal) +1 ) / 2)
# print(pipelineInstance.position)

window = pipelineInstance.signal[int(pipelineInstance.position): (int(pipelineInstance.position) + 1024)]
currentWindow = (window * np.hanning(1024))
#print(currentWindow)
spectrum = np.fft.rfft(currentWindow)
spectrum_frequency = np.fft.fftfreq(len(currentWindow), 22050)
# print(len(spectrum))
# print(spectrum[0])
# print(spectrum[512])
# print(abs(spectrum))

cent = librosa.feature.spectral_centroid(y = window, sr = sr)
print(np.mean(cent))

print(f"this is the maximum index in the loud part: {np.argmax(abs(spectrum))}")
maxindex = np.argmax(abs(spectrum))
maxfreq = spectrum_frequency[maxindex]
print(f"this is the frequency of the maximum index in the loud spectrum: {maxfreq}")
bassBins = spectrum[1 : 5]
print(bassBins)
midBins = spectrum[6 : 95]
trebleBins = spectrum[95 : 513]

bassTotal = sum(abs(bassBins))
midTotal = sum(abs(midBins))
trebleTotal = sum(abs(trebleBins))

#print(f"this is the total bass:{bassTotal} this is the total mid:{midTotal} this it the total treble: {trebleTotal}")

currentWindowWithout = (window)
#print(currentWindowWithout)

spectrum = np.fft.rfft(currentWindowWithout)
spectrum_frequency = np.fft.fftfreq(len(currentWindowWithout), 22050)
# print(len(spectrum))
# print(spectrum[0])
# print(spectrum[512])
# print(abs(spectrum))

print(f"this is the maximum index in the loud part: {np.argmax(abs(spectrum))}")
maxindex = np.argmax(abs(spectrum))
maxfreq = spectrum_frequency[maxindex]
print(f"this is the frequency of the maximum index in the loud spectrum: {maxfreq}")




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

cent = librosa.feature.spectral_centroid(y = window, sr = sr)
print(np.mean(cent))

print(f"this is the maximum index in the quiet part: {np.argmax(abs(spectrum))}")
maxindex = np.argmax(abs(spectrum))
maxfreq = spectrum_frequency[maxindex]
print(f"this is the frequency of the maximum index in the quiet spectrum: {maxfreq}")

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
print(spectrum_frequency[maxindex])
print(f"this is the maximum index: {np.argmax(abs(spectrum))}")
maxindex = np.argmax(abs(spectrum))
maxfreq = spectrum_frequency[maxindex]
print(f"this is the frequency of the maximum index in the spectrum: {maxfreq}")

#bin 5 corresponds to bass
#bin 95 corresponds to mids