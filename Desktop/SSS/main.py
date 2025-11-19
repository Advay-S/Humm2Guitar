import InstrumentSynthesizer
import subprocess 
import os

# Delete old files FIRST
for file in ['output.wav', 'guitar.wav', 'guitar.mid']: 
    if os.path.exists(file): 
        os.remove(file)
        print(f"Deleted old {file}")

# Now record (import happens here)
import Record

print("Starting recording...")

try:
    print("Creating guitar version...")
    InstrumentSynthesizer.synthesize_music('guitar.wav')
    
    # Check if file was actually created
    if not os.path.exists('guitar.wav'):
        print("Error: guitar.wav was not created!")
    else:
        print("Playing guitar.wav...")
        subprocess.run(['afplay', 'guitar.wav'])
        
except Exception as e:
    print(f"Error occurred: {e}")