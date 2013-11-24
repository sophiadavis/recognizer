"""
takes sound input, finds mfccs, deltas, double deltas, 
computes average of 39-value mfcc vector over entire audio stream

to do:
    make program to run this script for each file listed in command line, 
        (find stream_avg) output them all to a pickle file)
    
    make program to compare and get distance
"""

import sys
from features import mfcc
from features import fbank
import scipy.io.wavfile as wav
import numpy
import math

def main():
    if len(sys.argv) < 2:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' file.wav')
		sys.exit(1)
    file = sys.argv[1]
    
    (rate,sig) = wav.read(file) # returns (sample rate, numpy.ndarray of samples)

    mfcc_feat = mfcc(sig,rate)
    deltas = get_deltas(mfcc_feat, 0)
    double_deltas = get_deltas(deltas, 13)
    col_avg(double_deltas)
    print get_spectrum_maxes((rate,sig))
    
    
    
    
#     print type(mfcc_feat)
#     print len(mfcc_feat)
#     print mfcc_feat
#     print numpy.shape(mfcc_feat) # time_step rows * 13 columns
#     print mfcc_feat[1]
#     print type(mfcc_feat[1])
#     print len(mfcc_feat[1])
#     
#     print 'len deltas', len(deltas)
#     print 'len double deltas', len(double_deltas)
#     print mfcc_feat[3, :13]
#     print deltas[3, :13]
#     print double_deltas[3, :13]
#     print deltas[3, 14:26]
#     print double_deltas[3, 14:26]
# #     print len(deltas[1000])
#     print col_avg(double_deltas)

def get_deltas(matrix, index):
    
    if index == 0: # if adding deltas
        length = 26
    else: # if adding double deltas
        length = 39
    
    rows = numpy.shape(matrix)[0]  
    cols = numpy.shape(matrix)[1]
    
    new_matrix = numpy.zeros((rows, length))
    
    new_matrix[:2, :index + 13] = matrix[:2,] # can't 
    new_matrix[-2:, :index + 13] = matrix[-2:,]
    
    # for each window
    for i in range(2, rows - 2):

        # copy over existing values (mfcc's or mfcc's + deltas)
        new_matrix[i, :index + 13] = matrix[i]
        
        # for each value in row (each mfcc or delta)
        for j in range(index, index + 13):
            numerator = 0
            denominator = 0
            
            for n in [1, 2]:
                numerator += n*(matrix[i + n, j] - matrix[i - n, j])
                denominator += math.pow(n, 2)
            
            delta = numerator / (2 * denominator) 
            new_matrix[i, j + 13] = delta

    return new_matrix

def col_avg(matrix):
    num_rows = numpy.shape(matrix)[0]
    colsums = numpy.cumsum(matrix, 0)[num_rows - 1] # sum over all rows
    colmeans = colsums / float(num_rows) # average over all rows
    return colmeans

# argument = tuple produced by wav.read(file)
def get_spectrum_max_freqs((sampling_rate, stream_converted), window_len_ms = 25.0, windowby_ms = 10.0):
    
    ### define parameters
    n_samps = numpy.shape(stream_converted)[0]
    samps_per_window = int(sampling_rate*(window_len_ms/1000)) # samples per window
    windowby_samps = int(sampling_rate*(windowby_ms/1000)) # samples between between consecutive window starting positions
    nyquist = samps_per_window/2 # nyquist frequency
    
    ### store maximum frequency (F1, ideally) from each window in a list
    max_freqs = [] 

    window_start = 0
    ### perform Discrete Fourier Transform given samples in each window 
    # use DFT at each frequency to determine magnitude 
    while (window_start + samps_per_window) < n_samps:
        current_window = stream_converted[window_start : window_start + samps_per_window]
        dft_values = numpy.fft.fft(current_window)
        
        # calculate log magnitude at each frequency
        window_max = 0
        max_freq = 0
        for i in range(0, nyquist):
            real = numpy.real(dft_values[i])
            imag = numpy.imag(dft_values[i])
            sq_mag = math.sqrt(math.pow(real, 2) + math.pow(imag, 2))
            mag = 10*math.log10(sq_mag)
            if  (mag > window_max):
                window_max = mag
                max_freq = i/(window_len_ms/1000.0)
            
        max_freqs.append(max_freq)
        
        # increment window_start by number of samples separating each window starting position
        window_start += windowby_samps
        
    return max_freqs

def get_intervals(highest_freq, lowest_freq, n_bins, mel_binning = True):
    
    highest_freq_mels = math.floor(1125 * math.log(1 + highest_freq/700))
    lowest_freq_mels = math.floor(1125 * math.log(1 + lowest_freq/700))
    
    intervals = {}
    
    step_freq = (highest_freq - lowest_freq)/n_bins
    step_mels = (highest_freq_mels - lowest_freq_mels)/n_bins
    
    start_freq = lowest_freq + step_freq
    start_mels = lowest_freq_mels + step_mels
    
    if mel_binning:    
        while start_mels < highest_freq_mels:
            start_freq = math.floor(700 * (math.exp(start_mels/1125) - 1))
            intervals[start_freq] = None
            start_mels += step_mels
        intervals[highest_freq] = None
        
    else:
        while start_freq < highest_freq:
            start_freq = math.floor(start_freq)
            intervals[start_freq] = None
            start_freq += step_freq
        intervals[highest_freq] = None
        
    return intervals

def find_bin(value, end_pts):
    for n in end_pts:
        if value > n:
            continue    
        return n

if __name__ == "__main__":
    main()