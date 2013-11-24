
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
    spectrum_max_freqs = recognizer_util.get_spectrum_max_freqs((rate,sig))
    
    results = {}
    
    for i in range(2, n_rows - 2):
        max_freq = spectrum_max_freqs[i]
        vector = mfccs_deltas_ddeltas[i,]
        if (max_freq < highest_freq) and (max_freq > lowest_freq): # not dealing with freqs outside human voice range
            interval = recognizer_util.find_bin(max_freq, intervals_list)
            if intervals[interval] is None:
                intervals[interval] = mfccs_deltas_ddeltas[i,]
            else:
                current = intervals[interval]
                intervals[interval] = numpy.vstack((current, mfccs_deltas_ddeltas[i,]))
        else:
            continue # if its not human voice, skip it
        
    for interval in intervals.keys():
        current = intervals[interval]
        if current is None:
            intervals[interval] = numpy.zeros((1,39))
        else:
            intervals[interval] = recognizer_util.col_avg(current)
    
    print intervals
            
            
    for mfcc_deltas_ddeltas
    for language in languages.keys():
        for interval in language
        
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