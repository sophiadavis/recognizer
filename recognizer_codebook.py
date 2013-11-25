"""
recognizer_codebook.py
Sophia Davis, for 11/25/2013
NLP final project

This file is used to determine the source language of a test recording, based on 
comparison to a model of differences in spoken language calculated by 
train_recognizer_codebook.py, which trains a model based on speech recordings, and 
saves the data in a 'languages_codebook.dat' pickle file.

Both files calculate the MFCC vector on each 25 ms window in a sound file, 
and average MFCC vectors from windows where the maximum intensity occurred
at similar frequencies. This is accomplished by binning the range of human vocal
frequencies into (n_bins) bins.

The parameters
    n_bins -- the number of frequency bins of maximum intensity
    mel_binning -- whether or not bin endpoints are calculated on the Mel scale
    highest_freq 
    lowest_freq -- the highest and lowest frequencies to be considered 
should be set to the same value in both files.

The 'average' parameter determines how the source language guess should be calculated:
If average = True, the Euclidean distance between average MFCC vectors at all corresponding  
    bins is averaged for each language in the model. The language in the model which  
    produced the pairing with the lowest average distance is returned as a source 
    language guess.
If average = False, the Euclidean distance between average MFCC vectors at each 
    corresponding bin is calculated for each language in the model, and the language
    in the model which produced the pairing with the overall lowest distance is returned 
    as a source language guess.
"""

import recognizer_util
import sys
import numpy
from features import mfcc
import scipy.io.wavfile as wav
import scipy.spatial.distance
import pickle

def main():
    
    average = False # Which method should be used to determine similarity to languages in model?
    
    #### These settings should correspond to settings in train_recognizer_codebook.py ####
    n_bins = 7
    mel_binning = True
    highest_freq = 3500.0 # human vocal range
    lowest_freq = 200.0
    ######
    
    if len(sys.argv) < 2:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' lang_test.wav')
		sys.exit(1)
    
    file = sys.argv[1]
    
    languages = pickle.load( open('languages_codebook.dat', 'r') )
    
    # dictionary for sorting windows by frequency of maximum intensity
    intervals = recognizer_util.get_intervals(highest_freq, lowest_freq, n_bins, mel_binning)
    keys = list(intervals.keys())
    keys.sort()
    intervals_list = keys

    (rate,sig) = wav.read(file) # returns (sample rate, numpy.ndarray of samples)
    mfcc_feat = mfcc(sig,rate)
    mfccs_deltas = recognizer_util.get_deltas(mfcc_feat, 0)
    mfccs_deltas_ddeltas = recognizer_util.get_deltas(mfccs_deltas, 13)
    spectrum_max_freqs = recognizer_util.get_spectrum_max_freqs((rate,sig))
    
    n_rows = numpy.shape(mfccs_deltas_ddeltas)[0]
    
    ### bin MFCC vectors by frequency of maximum intensity
    for i in range(2, n_rows - 2): 
    # delta/double-delta values from first and last two windows cannot be calculated, so
    ## MFCC vectors from these windows can be ignored
        
        max_freq = spectrum_max_freqs[i]
        
        if (max_freq < highest_freq) and (max_freq > lowest_freq): # frequencies in human voice range
            interval = recognizer_util.find_bin(max_freq, intervals_list)
            if intervals[interval] is None:
                intervals[interval] = mfccs_deltas_ddeltas[i,]
            else:
                current = intervals[interval]
                intervals[interval] = numpy.vstack((current, mfccs_deltas_ddeltas[i,]))
        else:
            continue # ignore frequencies outside human voice range
    
    ### calculate average MFCC value in each frequency bin    
    for interval in intervals.keys():
        current = intervals[interval]
        if current is None:
            intervals[interval] = numpy.zeros((1,39))
        else:
            if numpy.shape(current) == (39,): # if there is only one vector in a bin, it's getting transposed somehow
                    intervals[interval] = numpy.transpose(current) # can't figure out why, but this solves the problem
            else:
                intervals[interval] = recognizer_util.col_avg(current)
        
    print
    
    if average:
    
        results_average_languages = {}
        results_average_values = {}
        
        for language in languages.keys():
            for interval in intervals_list:
                dist = get_distance(languages[language][interval], intervals[interval])
                if language in results_average_languages.keys():
                    current = results_average_languages[language]
                    results_average_languages[language] = numpy.mean((current, dist))      
                else:
                    results_average_languages[language] = dist
    
        for language in results_average_languages.keys():
            results_average_values[results_average_languages[language]] = language
        sorted = results_average_values.keys()
        sorted.sort()
        language = results_average_values[sorted[0]]
        sys.stdout.write(language) 
    
        # uncomment to see average Euclidean distance between test data and each language in model
#         for dist in sorted:
#             print results_average_values[dist], ':', dist
#         print
        
    else:
        
        results = {}
        
        for language in languages.keys():
            for interval in intervals_list:
                dist = get_distance(languages[language][interval], intervals[interval])
                results[dist] = language

        sorted = results.keys()
        sorted.sort()
        language = results[sorted[0]]
        sys.stdout.write(language) 
        # uncomment to see Euclidean distance between test data frequency bins and 
        ## frequency bins of each language in model
#         for dist in sorted:
#             print results[dist], ':', dist
    
    print

def get_distance(known, test):
    return scipy.spatial.distance.euclidean(known, test)

if __name__ == "__main__":
    main()