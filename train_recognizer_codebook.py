"""
train_recognizer_codebook.py
Sophia Davis, for 11/25/2013
NLP final project

This file is used to train a model of differences in spoken language based on speech 
recordings, and saves the data in a 'languages_codebook.dat' pickle file.
This pickle file can be used by recognizer_codebook.py to determine a guess at the source
language of a test recording.

Both files calculate the MFCC vector on each 25 ms window in a sound file, 
and average MFCC vectors from windows where the maximum intensity occurred
at similar frequencies. 
If multiple recordings from one language are used to form a model, the average MFCC 
vectors at each corresponding bin from each recording are averaged together.

The parameters
    n_bins -- the number of frequency bins of maximum intensity
    mel_binning -- whether or not bin endpoints are calculated on the Mel scale
    highest_freq 
    lowest_freq -- the highest and lowest frequencies to be considered 
should be set to the same value in both files.

to run: python train_recognizer_codebook.py language1.wav language1_name language2.wav language2_name ...
"""

import sys
import recognizer_util
import numpy
from features import mfcc
import scipy.io.wavfile as wav
import pickle
import math

def main():

    #### These settings should correspond to settings in train_recognizer_codebook.py ####
    n_bins = 7
    mel_binning = True
    highest_freq = 3500.0 # human vocal range
    lowest_freq = 200.0
    ######
     
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
        spectrum_max_freqs = recognizer_util.get_spectrum_max_freqs((rate,sig))
        
        # dictionary for sorting windows by frequency of maximum intensity
        intervals = recognizer_util.get_intervals(highest_freq, lowest_freq, n_bins, mel_binning)
        intervals_list = sorted(intervals.keys())
        
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
                if numpy.shape(current) == (39,):  # if there is only one vector in a bin, it's getting transposed somehow
                    intervals[interval] = numpy.transpose(current) # can't figure out why, but this solves the problem
                else:
                    intervals[interval] = recognizer_util.col_avg(current)
        
        ### if multiple recordings from one language are used to train model
        # take average MFCC values in each frequency bin from each recording         
        if language in languages.keys():
            for interval in intervals_list:
                array = numpy.vstack((languages[language][interval], intervals[interval]))
                new_avg = recognizer_util.col_avg(array)
                languages[language][interval] = new_avg
        else:
            languages[language] = intervals
            
    # uncomment to see dictionaries
#     for language in languages.keys():
#         print language
#         print languages[language]
    
    pickle.dump(languages, open('languages_codebook.dat', 'w'))
    print
    
if __name__ == "__main__":
    main()