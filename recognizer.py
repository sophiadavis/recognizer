"""
takes in .wav files to train MFCC codebooks

## at each relative maxima on a window, take the average of the features

bin range of frequencies
count up number of times there is a relative maximum on a frequency over a sound stream
normalize the number
use in regression model?? minimum edit distance?
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
    # below code allows you to see euclidean distance between test data and each language model
    for dist in sorted:
        print results[dist], ':', dist
    print

def get_distance(known, test):
    return scipy.spatial.distance.euclidean(known, test)


    
if __name__ == "__main__":
    main()