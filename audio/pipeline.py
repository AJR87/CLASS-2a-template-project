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
        self.prevMag = np.zeros(513)

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

            
            
            
            # sets the window chunk to start from self.postion in the spectrum and finish at that same postion + the self.window_size 
            # which is set at the top of the class
            windowChunk = self.signal[self.position:self.position + self.window_size]
            
            # this will stop the app from crashing when it runs out of windows to generate
            if len(windowChunk) < self.window_size:
                return {"amplitude": 0, "bass": 0, "mid": 0, "treble": 0, "cent": 0, "onset": 0}
            # creates the bins using hanning so that they dont have sharp edges and slowly rise and lower to and from 0
            spectrum = np.fft.rfft(windowChunk * np.hanning(len(windowChunk)))
            spectrum_frequency = np.fft.fftfreq(len(windowChunk), 22050)
            
            # this is how we calculate the onset. onset is the difference between the previous window and the current one
            # i set the previous window to start with an empty array of 0s that is 513 long so that python can run my code without it being ambigous
            # set the current magnitude to all the bins and uses the abs to remove the complex number
            currentMag = abs(spectrum)
            # sets onset total to 0 before the loop so that it doesnt repeatedly get put to 0 every run
            onsetTotal = 0
            # the loop runs for the length of magnitude so that it can compare each bin 
            for i in range(len(currentMag)):
                difference = currentMag[i] - self.prevMag[i]
            # only updates onset if it is a positive number and if it isnt the first in the spectrum because the first spectrum isnt acurate andm messes up results
                if difference > 0 and self.position != 0:
                    # adds difference to onset
                    onsetTotal += difference
            # sets self.prevMag to current mag ready for next set of bins we use self. so that it can be remembered even after the function ends
            self.prevMag = currentMag     
            
            # setting features to the correct bins in the spectrum
            bassBins = spectrum[1 : 5]
            midBins = spectrum[6 : 95]  
            trebleBins = spectrum[95 : 513]

            # usingh built in librosa centroid function so that we can calculate the centroid we use np.mean because it gives 3 numbers and we only want to log 1 in our dictionary
            cent = np.mean(librosa.feature.spectral_centroid(y=windowChunk, sr = 22050))

            # calculating the sum of all the magnitudes in each array and
            bassTotal = sum(abs(bassBins))
            midTotal = sum(abs(midBins))
            trebleTotal = sum(abs(trebleBins))

            # creating the dictionare to store all the values in
            Data = {"amplitude": self.RMS(windowChunk),
                    "bass": bassTotal,
                    "mid": midTotal,
                    "treble": trebleTotal,
                    "cent": cent,
                    "onset" : onsetTotal}
            self.position += self.window_size
            return Data
