# http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/#computing-the-mel-filterbank
# this lets me exclude windows where the highest frequency is out of human voice range
# http://fr.wikipedia.org/wiki/Formant French article gives similar range
# russian wiki neglects to use numbers http://ru.wikipedia.org/wiki/%D0%A4%D0%BE%D1%80%D0%BC%D0%B0%D0%BD%D1%82%D0%B0

import sys
import recognizer_util
import numpy
from features import mfcc
import scipy.io.wavfile as wav
import pickle
import math
# import pudb; pu.db

def main():
    
    # to run: python train_recognizer_codebook.py language1.wav language1_name language2.wav language2_name ... 
    if (len(sys.argv) < 3) or ((len(sys.argv) - 1) % 2 is not 0):
		sys.stderr.write('Usage: python ' + sys.argv[0] + "' language_data.wav' 'language_names'\n")
		sys.exit(1)
    
    # human max frequency is definitely below 3500 (http://en.wikipedia.org/wiki/Formant)
    highest_freq = 3500.0 # the files I'm using have a sampling rate of 48000
    lowest_freq = 200.0
    n_bins = 7
    mel_binning = True
    
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
        
        intervals = recognizer_util.get_intervals(highest_freq, lowest_freq, n_bins, mel_binning)
        intervals_list = sorted(intervals.keys())
        
        n_rows = numpy.shape(mfccs_deltas_ddeltas)[0]
        stop = False
        for i in range(2, n_rows - 2):
            print i
            print mfccs_deltas_ddeltas[i,]
            print type(mfccs_deltas_ddeltas[i,])
            print len(mfccs_deltas_ddeltas[i,])
            max_freq = spectrum_max_freqs[i]
            if (max_freq < highest_freq) and (max_freq > lowest_freq): # not dealing with freqs outside human voice range
                interval = recognizer_util.find_bin(max_freq, intervals_list)
                if interval == 3026.0:
                    stop = True
                    print 'STOP'
                else:
                    stop = False
                if intervals[interval] is None:
                    intervals[interval] = mfccs_deltas_ddeltas[i,]
                    if stop:
                        print 'in if'
                        print mfccs_deltas_ddeltas[i,]
                        print intervals[interval]
                        stop = False
                else:
                    current = intervals[interval]
                    intervals[interval] = numpy.vstack((current, mfccs_deltas_ddeltas[i,]))
                    print 'TYPE:', type(intervals[interval])
                    if stop:
                        print 'in else'
                        print current
                        print intervals[interval]

            else:
                continue # if its not human voice, skip it
            
        for interval in intervals.keys():
            print interval
            current = intervals[interval]
            if current is None:
                intervals[interval] = numpy.zeros((1,39))
            else:
                print language
                print current
                print 'current: ', numpy.shape(current)
                print type(current)
                if numpy.shape(current) == (39,): # awkward workaround, but I have no idea why this is happening
                    intervals[interval] = numpy.transpose(current)
                else:
                    intervals[interval] = recognizer_util.col_avg(current)
                print 'saving: ', intervals[interval]
                print
                    
        if language in languages.keys():
            print intervals_list
            for interval in intervals_list:
                print interval
                print 'numpy.shape(languages[language][interval]): ', numpy.shape(languages[language][interval])
                print 'numpy.shape(intervals[interval]): ', numpy.shape(intervals[interval])
                print languages[language][interval]
                print intervals[interval]
                array = numpy.vstack((languages[language][interval], intervals[interval]))
                new_avg = recognizer_util.col_avg(array)
                languages[language][interval] = new_avg
        else:
            languages[language] = intervals
#             print 'problem:', languages[language][3026.0]
            
    # uncomment if you want to see the dictionaries
    for language in languages.keys():
        print language
        print languages[language]
    pickle.dump(languages, open('languages_codebook.dat', 'w'))
    print
    
if __name__ == "__main__":
    main()