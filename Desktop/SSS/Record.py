import wave
import sys
import  pyaudio

try:
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16

    #channels is used to describe the audio channels . btw macOS kernel is named darwin ?!

    CHANNELS = 1 if sys.platform == 'darwin' else 2

    RATE = 44100
    RECORD_SECONDS = 10
    #wb here means write binary 
    with wave.open('output.wav', 'wb') as wf: 

        #wf is just a variable name 
        p = pyaudio.PyAudio()

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print("Recording...")

        for _ in range(0, RATE // CHUNK * RECORD_SECONDS): 
              wf.writeframes(stream.read(CHUNK)) 

        print('Done recording!')

        stream.close()

        p.terminate()
        
except Exception as e:
    print(f"Recording error: {e}")
    print("Make sure microphone permissions are enabled!")