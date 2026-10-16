import librosa
import numpy as np

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

    def load(self, path: str, sr: int = 22050) -> np.ndarray:
            signal, _ = librosa.load(path, sr=sr)
            self.signal = signal
            self.sample_rate = sr
            return signal 
    

    def get_features(self) -> dict:
        """Extract numerical features (amplitude at minimum) from the current
        window of the loaded signal, advance the pipeline's internal read
        position accordingly, and return them as a dict[str, float].

        This return value is passed directly into engine.update().
        """
        raise NotImplementedError
