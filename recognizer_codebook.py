
import recognizer_util
import sys
import numpy
from features import mfcc
import scipy.io.wavfile as wav
import scipy.spatial.distance
import pickle

def main():
    
#     average = True
    
    if len(sys.argv) < 2:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' lang_test.wav')
		sys.exit(1)
    file = sys.argv[1]
    
    languages = pickle.load( open('languages_codebook.dat', 'r') )
    
    highest_freq = 3500.0 # the files I'm using have a sampling rate of 48000
    lowest_freq = 200.0
    n_bins = 7
    mel_binning = True
    
    intervals = recognizer_util.get_intervals(highest_freq, lowest_freq, n_bins, mel_binning)
#     print intervals
#     print intervals.keys()
    keys = list(intervals.keys())
    keys.sort()
#     print keys
    intervals_list = keys

    (rate,sig) = wav.read(file) # returns (sample rate, numpy.ndarray of samples)
    mfcc_feat = mfcc(sig,rate)
    mfccs_deltas = recognizer_util.get_deltas(mfcc_feat, 0)
    mfccs_deltas_ddeltas = recognizer_util.get_deltas(mfccs_deltas, 13)
    spectrum_max_freqs = recognizer_util.get_spectrum_max_freqs((rate,sig))
    
    n_rows = numpy.shape(mfccs_deltas_ddeltas)[0]
    
    for i in range(2, n_rows - 2):
        max_freq = spectrum_max_freqs[i]
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
    
    results = {}
    results_average_languages = {}
    results_average_values = {}
    
    print
#     if average == True:
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
    print
    
    # below code allows you to see average euclidean distance between test data and each language model
    for dist in sorted:
        print results_average_values[dist], ':', dist
    print
#         
#     else:
#         for language in languages.keys():
#             for interval in intervals_list:
#                 dist = get_distance(languages[language][interval], intervals[interval])
#                 results[dist] = language
#                 if language in results_average.keys():
#                     current = results_average[language]
#                     results_average[language] = numpy.mean((current, dist))      
#                 else:
#                     results_average[language] = dist
# 
#         sorted = results.keys()
#         sorted.sort()
#         print
#         language = results[sorted[0]]
#         sys.stdout.write(language) 
#         print
#         # below code allows you to see euclidean distance between test data and each language model
#         for dist in sorted:
#             print results[dist], ':', dist
#         print
    
    print


def get_distance(known, test):
    return scipy.spatial.distance.euclidean(known, test)


    
if __name__ == "__main__":
    main()