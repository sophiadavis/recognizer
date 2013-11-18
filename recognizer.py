"""
takes in .wav files to train MFCC codebooks

## at each relative maxima on a window, take the average of the features

bin range of frequencies
count up number of times there is a relative maximum on a frequency over a sound stream
normalize the number
use in regression model?? minimum edit distance?
"""
import deltas
import sys
# import wave
# from graphics import *
# import Tkinter as TK
import numpy
# import math
# import array
from features import mfcc
# from features import fbank
import scipy.io.wavfile as wav
import scipy.spatial.distance
import pickle

def main():
    if len(sys.argv) < 3:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' lang_test.wav', ' data_file.dat')
		sys.exit(1)
    file = sys.argv[1]
    data = sys.argv[2]
    
    languages = pickle.load( open(data, 'r') )

    (rate,sig) = wav.read(file) # returns (sample rate, numpy.ndarray of samples)
    mfcc_feat = mfcc(sig,rate)
    mfccs_deltas = deltas.get_deltas(mfcc_feat, 0)
    mfccs_deltas_ddeltas = deltas.get_deltas(mfccs_deltas, 13)
    test_avg = deltas.col_avg(mfccs_deltas_ddeltas)
    
    results = {}
    for language in languages.keys():
        dist = get_distance(languages[language], test_avg)
        results[dist] = language
    
    sorted = results.keys()
    sorted.sort()
    print
    for dist in sorted:
        print results[dist], ':', dist
    print

def get_distance(known, test):
    return scipy.spatial.distance.euclidean(known, test)


    
if __name__ == "__main__":
    main()