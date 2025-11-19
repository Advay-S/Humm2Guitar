import librosa
import numpy as np
import crepe

def extract_melody(audio_file):

#load audio
    y, sr = librosa.load(audio_file, sr=44100)

#using crepe for pitch detection
    time, freq , confidence, activation = crepe.predict(y, sr, viterbi=True,step_size=10)



#convert to midi notes 
    midi_notes = librosa.hz_to_midi(frequencies=freq)

#used to correct notes 
    midi_notes = np.round(midi_notes).astype(int)

#empty dictionary 
    notes = []
    current_note = None 
    start_time = None

    for i , (timez , note) in enumerate(zip(time, midi_notes)): 
        if(note != current_note): 
            if(current_note is not None): 
                duration = timez - start_time
                notes.append({
                    'midi_note':  current_note,

                    'start_duration': start_time, 

                    'duration': duration, 
                    'note_name': librosa.midi_to_note(current_note)
                })
        current_note = note 
        start_time = timez 

    if current_note is not None: 
        notes.append({
                    'midi_note':  current_note,
                    'start_duration': start_time, 
                    'duration':time[-1] - start_time, 
                    'note_name': librosa.midi_to_note(current_note)
                })
    
    # Filter out very short notes
    MIN_NOTE_DURATION = 0.02  # Lowered from 0.05 to 0.02 (20ms)
    filtered_notes = [n for n in notes if n['duration'] >= MIN_NOTE_DURATION]
    
    print(f"Filtered: {len(notes)} → {len(filtered_notes)} notes (removed notes < {MIN_NOTE_DURATION}s)")
    
    # If still no notes, show warning but return what we have
    if len(filtered_notes) == 0:
        print("WARNING: No notes after filtering! Using top 50 longest notes instead...")
        # Sort by duration and take top 50
        sorted_notes = sorted(notes, key=lambda x: x['duration'], reverse=True)[:50]
        return sorted_notes
    
    return filtered_notes        


