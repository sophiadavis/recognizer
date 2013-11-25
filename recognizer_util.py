"""
recognizer_util.py
Sophia Davis, for 11/25/2013
NLP final project

This file contains the following helper methods needed for other language recognizer programs:
get_deltas()
col_avg()
get_spectrum_max_freqs()

Formula for calculating deltas and conversion between frequency and Mels from:
http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/#computing-the-mel-filterbank
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
    get_spectrum_max_freqs((rate,sig))

### Calculates delta (index = 0) or double delta (index = 13) values from a matrix of 
    # vectors of MFCCs or MFCCs + delta values.
    # Returns matrix with new values appended to each vector. 
def get_deltas(matrix, index):
    
    if index == 0: # if adding deltas
        length = 26
    else: # if adding double deltas
        length = 39
    
    rows = numpy.shape(matrix)[0]  
    cols = numpy.shape(matrix)[1]
    
    new_matrix = numpy.zeros((rows, length))
    
    new_matrix[:2, :index + 13] = matrix[:2,] # cannot compute change over windows at first or last 2 windows
    new_matrix[-2:, :index + 13] = matrix[-2:,]
    
    # for each window
    for i in range(2, rows - 2):

        # copy over existing values (mfccs or mfccs + deltas)
        new_matrix[i, :index + 13] = matrix[i]
        
        # for each value in row (each mfcc or delta value)
        for j in range(index, index + 13):
            numerator = 0
            denominator = 0
            
            for n in [1, 2]:
                numerator += n*(matrix[i + n, j] - matrix[i - n, j])
                denominator += math.pow(n, 2)
            
            delta = numerator / (2 * denominator) 
            new_matrix[i, j + 13] = delta

    return new_matrix

### Averages values in each column of a matrix 
    # Returns nd.array() with one row
def col_avg(matrix):
    num_rows = numpy.shape(matrix)[0]
    colsums = numpy.cumsum(matrix, 0)[num_rows - 1] # sum over all rows
    colmeans = colsums / float(num_rows) # average over all rows
    return colmeans

### Finds the frequency associated with the maximum sound intensity on each window
    # (sampling_rate, stream_converted) = tuple output of wav.read(file)
    # Returns list of one frequency per window
def get_spectrum_max_freqs((sampling_rate, stream_converted), window_len_ms = 25.0, windowby_ms = 10.0):
    
    ### define parameters
    n_samps = numpy.shape(stream_converted)[0]
    samps_per_window = int(sampling_rate*(window_len_ms/1000)) # samples per window
    windowby_samps = int(sampling_rate*(windowby_ms/1000)) # samples per window step
    nyquist = samps_per_window/2
    
    ### store frequency associated with maximum intensity on each window
    max_freqs = [] 

    window_start = 0
    ### perform Discrete Fourier Transform given samples in each window 
    while (window_start + samps_per_window) < n_samps:
        current_window = stream_converted[window_start : window_start + samps_per_window]
        dft_values = numpy.fft.fft(current_window)
        
        # calculate magnitude of intensity at each frequency, save frequency of maximum
        window_max = 0
        max_freq = 0
        for i in range(0, nyquist):
            real = numpy.real(dft_values[i])
            imag = numpy.imag(dft_values[i])
            sq_mag = math.sqrt(math.pow(real, 2) + math.pow(imag, 2))
            mag = 2 * sq_mag/samps_per_window
            if  (mag > window_max):
                window_max = mag
                max_freq = i/(window_len_ms/1000.0)
            
        max_freqs.append(max_freq)
        
        # increment window_start by number of samples per window step
        window_start += windowby_samps
        
    return max_freqs

### Divides a range of frequencies into (n_bins) bins
    # Returns dictionary with bin endpoints as keys
    # if mel_binning = True, then bin endpoints are calculated on the mel scale
        # but each endpoint is re-converted into Hz before being appended to the dictionary
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

### Given a value and a list of bin endpoints, determines which 
    # bin the given value should fall into
def find_bin(value, end_pts):
    for n in end_pts:
        if value > n:
            continue    
        return n

if __name__ == "__main__":
    main()