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
    
    # Filter out very short notes and merge similar adjacent notes
    MIN_NOTE_DURATION = 0.1  # Minimum 100ms notes
    filtered_notes = []
    
    for note in notes:
        if note['duration'] >= MIN_NOTE_DURATION:
            # Merge with previous note if same pitch and close in time
            if filtered_notes and filtered_notes[-1]['midi_note'] == note['midi_note']:
                # Check if gap is small (less than 0.05s)
                gap = note['start_duration'] - (filtered_notes[-1]['start_duration'] + filtered_notes[-1]['duration'])
                if gap < 0.05:
                    # Merge: extend previous note's duration
                    filtered_notes[-1]['duration'] = (note['start_duration'] + note['duration']) - filtered_notes[-1]['start_duration']
                else:
                    filtered_notes.append(note)
            else:
                filtered_notes.append(note)
    
    print(f"Filtered: {len(notes)} → {len(filtered_notes)} notes (removed notes < {MIN_NOTE_DURATION}s)")
    
    # If still no notes, show warning but return what we have
    if len(filtered_notes) == 0:
        print("WARNING: No notes after filtering! Using top 30 longest notes instead...")
        # Sort by duration and take top 30
        sorted_notes = sorted(notes, key=lambda x: x['duration'], reverse=True)[:30]
        return sorted_notes
    
    return filtered_notes        


