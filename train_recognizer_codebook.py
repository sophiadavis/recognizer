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

def main():
    mel_binning = True
    
    # to run: python train_recognizer_codebook.py language1.wav language1_name language2.wav language2_name ... 
    if (len(sys.argv) < 3) or ((len(sys.argv) - 1) % 2 is not 0):
		sys.stderr.write('Usage: python ' + sys.argv[0] + "' language_data.wav' 'language_names'\n")
		sys.exit(1)
    
    n_bins = 7
    # human max frequency is definitely below 3500 (http://en.wikipedia.org/wiki/Formant)
    highest_freq = 3500.0 # the files I'm using have a sampling rate of 48000
    lowest_freq = 200
    highest_freq_mels = 1125 * math.log(1 + highest_freq/700) #
    lowest_freq_mels = 1125 * math.log(1 + lowest_freq/700) 
    intervals_list = []
    intervals = {}
    step_freq = highest_freq/n_bins
    step_mels = 1125 * math.log(1 + step_freq/700)
    
    start_freq = lowest_freq
    start_mels = lowest_freq_mels
    
    if mel_binning:    
        while start_mels < highest_freq_mels:
            start_mels += step_mels
            start_freq = 700 * (math.exp(start_mels/1125) - 1)
            intervals_list.append(start_freq)
            intervals[start_freq] = None
        print intervals
        print intervals_list
    
    else:
        while start_freq < highest_freq:
            start_freq += step_freq
            intervals_list.append(start_freq)
            intervals[start_freq] = None
        print intervals
        print intervals_list
        
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
#         avg = recognizer_util.col_avg(mfccs_deltas_ddeltas)
        spectrum_max_freqs = recognizer_util.get_spectrum_max_freqs((rate,sig))
        print spectrum_max_freqs
        print max(spectrum_max_freqs)
        print spectrum_max_freqs.index(max(spectrum_max_freqs))
        
        n_rows = numpy.shape(mfccs_deltas_ddeltas)[0]
        
        for i in range(2, n_rows - 2):
            max_freq = spectrum_max_freqs[i]
            vector = mfccs_deltas_ddeltas[i,]
            if (max_freq < highest_freq) and (max_freq > lowest_freq): # not dealing with freqs outside human voice range
                print max_freq
                print intervals_list
                interval = find_bin(max_freq, intervals_list)
                print interval
                print
                if intervals[interval] is None:
                    intervals[interval] = mfccs_deltas_ddeltas[i,]
                else:
                    current = intervals[interval]
    #                 print i
    #                 print current
    #                 print mfccs_deltas_ddeltas[i,]
    #                 print numpy.shape(current)
    #                 print numpy.shape(mfccs_deltas_ddeltas[i,])
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
            
        if language in languages.keys():
            for interval in languages[language]:
                array = numpy.vstack((languages[language][interval], intervals[interval]))
                new_avg = recognizer_util.col_avg(array)
                languages[language] = new_avg
        else:
            languages[language] = intervals
            
    # uncomment if you want to see the dictionaries
    for language in languages.keys():
        print language
        print languages[language]
    pickle.dump(languages, open('languages.dat', 'w'))
    print

def find_bin(value, end_pts):
    for n in end_pts:
        if value > n:
            continue    
        return n
    
if __name__ == "__main__":
    main()