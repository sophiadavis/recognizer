"""
recognizer.py
Sophia Davis, for 11/25/2013
NLP final project

This file is used to determine the source language of a test recording, based on 
comparison to a simple model of differences in spoken language calculated by train_recognizer.py, 
which trains a model based on speech recordings, and saves the data in a 'languages.dat' 
pickle file.

Both files calculate the MFCC vector on each 25 ms window in a sound file, 
and then average MFCC vectors over all windows.

The Euclidean distance is calculated between the average MFCC vector of the test 
recording and every language in the model. The language in the model which produced the 
pairing with the lowest distance is returned as a source language guess. 
"""

import recognizer_util
import sys
import numpy
from features import mfcc
import scipy.io.wavfile as wav
import scipy.spatial.distance
import pickle

def main():
    if len(sys.argv) < 2:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' lang_test.wav')
		sys.exit(1)
    file = sys.argv[1]
    
    languages = pickle.load( open('languages.dat', 'r') )

    (rate,sig) = wav.read(file) # returns (sample rate, numpy.ndarray of samples)
    mfcc_feat = mfcc(sig,rate)
    mfccs_deltas = recognizer_util.get_deltas(mfcc_feat, 0)
    mfccs_deltas_ddeltas = recognizer_util.get_deltas(mfccs_deltas, 13)
    test_avg = recognizer_util.col_avg(mfccs_deltas_ddeltas)
    
    results = {}
    
    for language in languages.keys():
        dist = get_distance(languages[language], test_avg)
        results[dist] = language
    
    sorted = results.keys()
    sorted.sort()
    print
    language = results[sorted[0]]
    sys.stdout.write(language) 
    print
    
    # uncomment to see Euclidean distance between test data and each language model
#     for dist in sorted:
#         print results[dist], ':', dist
#     print

def get_distance(known, test):
    return scipy.spatial.distance.euclidean(known, test)
    
if __name__ == "__main__":
    main()