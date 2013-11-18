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
    stream_avg(double_deltas)
    
    
    
    
    print type(mfcc_feat)
    print len(mfcc_feat)
    print mfcc_feat
    print numpy.shape(mfcc_feat) # time_step rows * 13 columns
    print mfcc_feat[1]
    print type(mfcc_feat[1])
    print len(mfcc_feat[1])
    
    print 'len deltas', len(deltas)
    print 'len double deltas', len(double_deltas)
    print mfcc_feat[3, :13]
    print deltas[3, :13]
    print double_deltas[3, :13]
    print deltas[3, 14:26]
    print double_deltas[3, 14:26]
#     print len(deltas[1000])
    print col_avg(double_deltas)

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

if __name__ == "__main__":
    main()