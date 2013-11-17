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
#     print rate
#     print sig
#     print type(sig)

    mfcc_feat = mfcc(sig,rate)
    fbank_feat = fbank(sig,rate)
    
    print type(mfcc_feat)
    print len(mfcc_feat)
    print mfcc_feat
    print numpy.shape(mfcc_feat) # time_step rows * 13 columns
    print mfcc_feat[1]
    print type(mfcc_feat[1])
    print len(mfcc_feat[1])
    deltas = get_deltas(mfcc_feat, 0)
    double_deltas = get_deltas(deltas, 13)
    print 'len deltas', len(deltas)
    print 'len double deltas', len(double_deltas)
    print mfcc_feat[3, :13]
    print deltas[3, :13]
    print double_deltas[3, :13]
    print deltas[3, 14:26]
    print double_deltas[3, 14:26]
#     print len(deltas[1000])

def get_deltas(matrix, index):
    
    if index == 0: # adding deltas
        length = 26
    else: # adding double deltas
        length = 39
    cols = numpy.shape(matrix)[1]
    rows = numpy.shape(matrix)[0]
    print 'rows', rows
    new_matrix = numpy.zeros((rows, length))
    new_matrix[:2, :index + 13] = matrix[:2,]
    new_matrix[-2:, :index + 13] = matrix[-2:,]
#     print 'new matrix', new_matrix
    # for each window
    for i in range(2, rows - 2):
#         print matrix[i]
        # for each index of mfcc's or deltas
#         print '---'
#         print i
#         print matrix[i]
        new_matrix[i, :index + 13] = matrix[i]
        
#         print new_matrix[i]
        for j in range(index, index + 13):
#             print j, matrix[i, j]
            numerator = 0
            denominator = 0
            
            for n in [1, 2]:
                numerator += n*(matrix[i + n, j] - matrix[i - n, j])
                denominator += math.pow(n, 2)
            
            delta = numerator / (2 * denominator) 
#             print delta
#             print 'in get deltas', len(numpy.append(matrix[i], delta))
#             print matrix[i]
#             print delta
            new_matrix[i, j + 13] = delta
#             print new_matrix[i, j + 13]
#             print new_matrix[i]
        
#         print row
#         print numpy.shape(row)
#         print numpy.shape(new_matrix)
#         new_matrix = numpy.vstack((new_matrix, row))
    print new_matrix
    return new_matrix

if __name__ == "__main__":
    main()