# Noise Remover-v1

This script removes noise from an audio file using the Fourier Transform.

> [!NOTE] References - Noise Remover
>
> * [Remove Background Noise with Fourier Transform in Python - NeuralNine](https://www.youtube.com/watch?v=LURaBTYzhj0)
> * [Audio Data Processing in Python - Rob Mulla](https://www.youtube.com/watch?v=ZqpSb5p1xQo)

> [!CAUTION] soundfile.LibsndfileError: Error opening `input-audio-file-path`: Format not recognised
> 
> This error occurs because librosa uses the soundfile library under the hood by default, and soundfile does not support .m4a audio files (it primarily supports formats like .wav, .flac, and .ogg). The easiest and most reliable fix is to convert your audio file into a `.wav` file. You can use free tools like Audacity, FFmpeg, or online audio converters.

* v1 is a working version. You have to specify: 
  1. the input audio file (a `.wav` file), 
  2. the starting timestamp of pure noise (in HH:MM:SS:ssss),
  3. the ending timestamp of pure noise (in HH:MM:SS:ssss).
* In v2, I'd try to use some AI model to see if I can correct the residual noise, preferrably, without specifying the timestamps.
