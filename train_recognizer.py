"""
train_recognizer.py
Sophia Davis, for 11/25/2013
NLP final project

This file is used to train a simple model of differences in spoken language based on speech 
recordings, and saves the data in a 'languages.dat' pickle file.
This pickle file can be used by recognizer.py to determine a guess at the source
language of a test recording.

Both files calculate the MFCC vector on each 25 ms window in a sound file, 
and then average MFCC vectors over all windows.
If multiple recordings from one language are used to form a model,
the average MFCC vectors from each recording are averaged together.

to run: python train_recognizer.py language1.wav language1_name language2.wav language2_name ...
"""

import sys
import recognizer_util
import numpy
from features import mfcc
import scipy.io.wavfile as wav
import pickle

def main():
     
    if (len(sys.argv) < 3) or ((len(sys.argv) - 1) % 2 is not 0):
		sys.stderr.write('Usage: python ' + sys.argv[0] + "' language_data.wav' 'language_names'\n")
		sys.exit(1)
    
    languages = {}
    
    print
    for index in range(1, len(sys.argv), 2):
        
        language = sys.argv[index + 1]
        file = sys.argv[index]
        
        print 'processing:', file, 'as', language
        print '...'
        
        (rate,sig) = wav.read(file)
        mfcc_feat = mfcc(sig,rate)
        mfccs_deltas = recognizer_util.get_deltas(mfcc_feat, 0)
        mfccs_deltas_ddeltas = recognizer_util.get_deltas(mfccs_deltas, 13)
        avg = recognizer_util.col_avg(mfccs_deltas_ddeltas)
        
        if language in languages.keys():
            array = numpy.vstack((languages[language], avg))
            new_avg = recognizer_util.col_avg(array)
            languages[language] = new_avg
        else:
            languages[language] = avg
            
    # uncomment to see dictionaries
#     for language in languages.keys():
#         print languages[language]
#         print len(languages[language])

    pickle.dump(languages, open('languages.dat', 'w'))
    print
    
if __name__ == "__main__":
    main()