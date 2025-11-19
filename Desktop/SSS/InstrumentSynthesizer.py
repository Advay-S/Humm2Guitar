import pretty_midi
import os
import subprocess
import MelodyExtractor


def synthesize_music(output_file, soundfont='FluidR3_GM.sf2'): 

 # Check if soundfont exists
 if not os.path.exists(soundfont):
     print(f"Error: Soundfont file '{soundfont}' not found!")
     return
 
 # Check if output.wav exists
 if not os.path.exists('output.wav'):
     print("Error: output.wav not found! Record audio first.")
     return
 
 notes = MelodyExtractor.extract_melody('output.wav')
 
 # Check if we got any notes
 if not notes or len(notes) == 0:
     print("Error: No notes extracted from audio!")
     return

 pmObj = pretty_midi.PrettyMIDI()
 guitar_program = pretty_midi.instrument_name_to_program('Guitar')
 guitar = pretty_midi.Instrument(program=guitar_program)

 for note_name in notes: 
    note_num = note_name['midi_note']
    note = pretty_midi.Note(velocity=100, pitch=note_num, start=note_name['start_duration' ], end=note_name['duration'] + note_name['start_duration'])
    guitar.notes.append(note)

 pmObj.instruments.append(guitar)
 
 temp_midi = output_file.replace('.wav', '.mid')
 pmObj.write(temp_midi)

 # Convert MIDI to WAV using FluidSynth via subprocess
 result = subprocess.run([
     'fluidsynth',
     '-ni',
     soundfont,  
     temp_midi,
     '-F',
     output_file,
     '-r',
     '44100'
 ])
 
 if result.returncode != 0:
     print(f"Error: FluidSynth failed with code {result.returncode}")
     return
 
 print(f"✓ Successfully created {output_file}")