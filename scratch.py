from audio.pipeline import AudioPipeline
AUDIO_FILE = "C:\\Users\\2502780\\Desktop\\CLASS-2a-template-project\\audio\\ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"
import math


pipelineInstance = AudioPipeline(file_path=AUDIO_FILE)

pipelineInstance.load()
samples = {
    "max" : {
        "value": float("-inf"),
        "current_window": 0
    },
    "min" : {
        "value" : float("inf"),
        "current_window" : 0
    }
}

windowNumber = int(len(pipelineInstance.signal) / pipelineInstance.window_size)
i = 0


while True:

    try:

        pipelineInstance.position = i * pipelineInstance.window_size

        current_rms = pipelineInstance.get_features()["amplitude"]
        max_value = max(samples["max"]["value"], current_rms)
        if max_value == current_rms:
            samples["max"]["value"] = current_rms
            samples["max"]["current_window"] = i

        min_value = min(samples["min"]["value"], current_rms)
        if min_value == current_rms:
            samples["min"]["value"] = current_rms
            samples["min"]["current_window"] = i
        i += 1

        if i >= windowNumber:
            print("looped")
            i = 0
            pipelineInstance.position = 0

    except Exception as e:
        print(e)

print(f"the maximum amplitude in the signal is {samples["max"]["value"]} and is in window {samples["max"]["current_window"]}")
print(f"the minimum amplitude in the signal is {samples["min"]["value"]} and is in window {samples["min"]["current_window"]}")


# for i in range(0, 15):
#     amplitude = pipelineInstance.get_features()["amplitude"]
#     print(amplitude)
        
