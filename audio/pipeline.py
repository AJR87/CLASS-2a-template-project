import librosa
import numpy as np
import math
class AudioPipeline:
 
    """Loads an audio file and extracts features from it, frame by frame.

    Both load() and get_features() are stubs you must implement yourself —
    that's intentional, not an oversight. This unit is about the whole
    pipeline (data source -> feature extraction -> real-time rendering), not
    just feature extraction handed to you pre-solved.
    """

    def __init__(self, file_path: str, sample_rate: int = 22050) -> None:
        self.file_path = file_path
        self.sample_rate = sample_rate
        self.window_size = 1024
        self.position = 0

    def load(self) -> np.ndarray:
            signal, _ = librosa.load(self.file_path, sr=self.sample_rate)
            self.signal = signal
            return signal 
    
    def RMS(self, windowChunk):
        
        windowSquared = np.square(windowChunk)
        windowMean = np.mean(windowSquared)
        windowRoot = np.sqrt(windowMean)
        return windowRoot
        
    #    signalsamplelist = []
    #    addsample = 0
    #    for i in signalsample:
    #        iSquared = i*i
    #        signalsamplelist.append(iSquared)
    #    for i in signalsamplelist:
    #        addsample += i
    #    dividedsample = addsample / len(signalsample)
    #    return (math.sqrt(dividedsample))

    def get_features(self) -> dict:
            windowChunk = self.signal[self.position:self.position + self.window_size]
            Data = {"amplitude": self.RMS(windowChunk)}
            self.position += self.window_size
            # print(Data)
            return Data
