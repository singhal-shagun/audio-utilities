from pathlib import Path
from datetime import datetime
import gc
import numpy as np              #!pip install numpy
import librosa                  #!pip install librosa
import matplotlib.pyplot as plt #!pip install matplotlib
import soundfile                #!pip install soundfile
import scipy.fftpack            #!pip install scipy
from scipy.signal import medfilt

# CONSTANTS
TIME_FORMAT = "%H:%M:%S.%f" #HH:MM:SS:ssss

# DEFINE THE PARAMETERS HERE
inputFileName = "2026-04-01 16-07-57 5.wav"
noiseStartTimeHHMMSSsss = datetime.strptime("00:00:00.000", "%H:%M:%S.%f")
noiseEndTimeHHMMSSsss = datetime.strptime("00:00:02.000", "%H:%M:%S.%f")

if __name__ == "__main__":

    # 1. Enter your input audio file name here.
    scriptDirectoryPath = Path(__file__).parent # Get the directory of the current script
    inputAudioFilePath = scriptDirectoryPath / inputFileName

    if inputAudioFilePath.is_file():
        outputAudioFilePath = inputAudioFilePath.with_stem(inputAudioFilePath.stem + "_cleaned")
    else:
        raise FileNotFoundError(f"Input audio file not found at {inputAudioFilePath.absolute()}")


    # 2. Extract the individual samples
    audioSamples, samplingRate = librosa.load(inputAudioFilePath, sr=None)

    # 3. Perform Short-Time Fourier Transform (STFT)
    stft = librosa.stft(audioSamples)
    del audioSamples
    gc.collect()

    # 4. Separate magnitude and phase
    magnitude, phase = librosa.magphase(stft)
    del stft
    gc.collect()

    # 5. Calculate the mean noise level (in decibal) that is to be removed.
    ## From the noise start time and end time, calculate the number of samples whose mean
    noiseStartTimeSec = noiseStartTimeHHMMSSsss.hour * 3600 + noiseStartTimeHHMMSSsss.minute * 60 + noiseStartTimeHHMMSSsss.second + (noiseStartTimeHHMMSSsss.microsecond / 1e6)
    noiseEndTimeSec = noiseEndTimeHHMMSSsss.hour * 3600 + noiseEndTimeHHMMSSsss.minute * 60 + noiseEndTimeHHMMSSsss.second + (noiseEndTimeHHMMSSsss.microsecond / 1e6)
    noiseStartFrame = librosa.time_to_frames(noiseStartTimeSec, sr=samplingRate)
    noiseEndFrame = librosa.time_to_frames(noiseEndTimeSec, sr=samplingRate)
    noisePower = np.mean(
        magnitude[:, noiseStartFrame:noiseEndFrame],
        axis=1)
    
    # 6. Create a mask that will only allow samples whose magnitude is greater than noisePower. 
    ## This is done by comparing the magnitude with the noisePower.
    mask = magnitude > noisePower[:, None]
    mask = mask.astype(float)
    # mask = medfilt(mask, kernel_size=(1, 5))    # This will smoothen the choppped down audio samples.

    # 8. Apply the mask to the audio samples
    magnitude = magnitude * mask
    del mask
    gc.collect()

    # 9. Transform the audio samples back to the time domain.
    denoisedAudioSTFT = magnitude * phase
    del magnitude, phase
    gc.collect()
    denoisedAudioSamples = librosa.istft(denoisedAudioSTFT)
    del denoisedAudioSTFT
    gc.collect()

    # 10. Write the denoised file on to the disk.
    soundfile.write(outputAudioFilePath, 
                    denoisedAudioSamples, 
                    samplingRate)
