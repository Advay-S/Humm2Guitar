# Humming to Guitar Converter 🎸

Convert your humming into guitar music!

## Features
- Records 10 seconds of audio
- AI-powered melody extraction using CREPE
- Converts to guitar using MIDI synthesis
- Auto-plays the result

## Requirements
- Python 3.x
- FluidSynth installed (`brew install fluid-synth` on macOS)
- Soundfont file (FluidR3_GM.sf2)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Advay-S/hum2guitar.git
cd hum2guitar
```

2. Create virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Download soundfont file:
Download [FluidR3_GM.sf2](https://member.keymusician.com/Member/FluidR3_GM/index.html) and place it in the project directory.

## Usage

```bash
python main.py
```

1. The program will record for 10 seconds
2. Hum your melody clearly and loudly
3. Wait for processing
4. The guitar version will auto-play!

## How it Works

1. **Record.py** - Captures audio input using PyAudio
2. **MelodyExtractor.py** - Extracts melody notes using CREPE AI model
3. **InstrumentSynthesizer.py** - Creates guitar MIDI and synthesizes to WAV
4. **main.py** - Orchestrates the entire pipeline

## Project Structure

```
hum2guitar/
├── main.py                    # Main orchestrator
├── Record.py                  # Audio recording module
├── MelodyExtractor.py         # AI melody extraction
├── InstrumentSynthesizer.py   # MIDI synthesis
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Dependencies

- `pyaudio` - Audio recording
- `librosa` - Audio processing
- `crepe` - AI pitch detection
- `tensorflow` - Required by CREPE
- `pretty_midi` - MIDI file creation
- `numpy` - Array operations

## Tips for Best Results

- Hum clearly and loudly
- Stay close to your microphone
- Hum simple melodies
- Keep humming for most of the 10 seconds
- Ensure microphone permissions are enabled

## License

MIT License
