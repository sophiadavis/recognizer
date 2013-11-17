"""
takes in .wav files to train MFCC codebooks

## at each relative maxima on a window, take the average of the features

bin range of frequencies
count up number of times there is a relative maximum on a frequency over a sound stream
normalize the number
use in regression model?? minimum edit distance?
"""
import deltas
import sys
import wave
from graphics import *
import Tkinter as TK
import numpy
import math
import array
from features import mfcc
from features import fbank
import scipy.io.wavfile as wav
import pickle

def main():
    # to run: python train_recognizer.py language1.wav language1_name language2.wav language2_name
    if (len(sys.argv) < 3) or ((len(sys.argv) - 1) % 2 is not 0):
		print len(sys.argv)
		print len(sys.argv[1]) 
		print len(sys.argv[2])
		for index in range(0, len(sys.argv)):
		    print sys.argv[index]
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' [language_data.wav files] [language_names]\n')
		sys.exit(1)
#     file = sys.argv[1]
    
    languages = {}

    for index in range(1, len(sys.argv), 2):
        
        language = sys.argv[index + 1]
        
        file = sys.argv[index]
        (rate,sig) = wav.read(file)
        mfcc_feat = mfcc(sig,rate)
        mfccs_deltas = deltas.get_deltas(mfcc_feat, 0)
        mfccs_deltas_ddeltas = deltas.get_deltas(mfccs_deltas, 13)
        avg = deltas.stream_avg(mfccs_deltas_ddeltas)
        
        languages[language] = avg
    
    print languages
    pickle.dump(languages, open('languages.dat', 'w'))
    
#     (rate,sig) = wav.read(file) # returns (sample rate, numpy.ndarray of samples)
#     print rate
#     print sig
#     print type(sig)

#     mfcc_feat = mfcc(sig,rate)
#     deltas = deltas.get_deltas(mfcc_feat, 0)
#     double_deltas = deltas.get_deltas(deltas, 13)
#     avg = deltas.stream_avg(double_deltas)
#     print mfcc_feat
#     print deltas
#     print double_deltas
#     print avg
    
#     file.close()


#     speech = wave.open(file)
#     
#     
#     
#     ### define parameters
#     n_samps = speech.getnframes() # total number of samples
#     window_len_ms = 25.0 # window length in milliseconds
#     windowby_ms = 10.0 # milliseconds between consecutive window starting positions 
#     sampling_rate = speech.getframerate() # samples per second
#     samps_per_window = int(sampling_rate*(window_len_ms/1000)) # samples per window
#     windowby_samps = int(sampling_rate*(windowby_ms/1000)) # samples between between consecutive window starting positions
#     nyquist = samps_per_window/2 # nyquist frequency
#     highest_freq = int(nyquist/(window_len_ms/1000.0))
#     
#     print sampling_rate
#     print n_samps/windowby_samps
#     
#     ### read in .wav file as string of bytes, convert to list of usable samples
#     stream = speech.readframes(n_samps)
#     stream_converted = array.array('h', stream)
#     stream_converted = stream_converted.tolist()
#     speech.close()
#     
#     ### store information about each window's spectrum in dictionary 
#     # index by time step 
#     time_steps = {}
# 
#     window_start = 0
#     time_step = 0
#     maximum = 0
#     minimum = 0
# 
#     ### perform Discrete Fourier Transform given samples in each window 
#     # use DFT at each frequency to determine magnitude 
#     while (window_start + samps_per_window) < n_samps:
#         current_window = stream_converted[window_start : window_start + samps_per_window]
#         dft_values = numpy.fft.fft(current_window)
#         
#         # calculate log magnitude at each frequency
#         magnitudes = []
#         for i in range(0, nyquist):
#             real = numpy.real(dft_values[i])
#             imag = numpy.imag(dft_values[i])
#             sq_mag = math.sqrt(math.pow(real, 2) + math.pow(imag, 2))
#             mag = 2 * sq_mag/samps_per_window
#             if mag > maximum:
#                 maximum = mag
#             if mag < minimum:
#                 minimum = mag
#             magnitudes = magnitudes + [mag]
#         
#         magnitudes_numped = numpy.array(magnitudes)
#         maxes = argrelextrema(magnitudes_numped, numpy.greater)
#             
#         # store magnitudes for current window 
#         time_steps[time_step] = magnitudes
#         
#         # increment window_start by number of samples separating each window starting position
#         # increment index for storing magnitudes by 1
#         window_start += windowby_samps
#         time_step += 1
#     
#     ### get the cut offs of the filterbanks
#     # simplifying -- 10 log spaced bins
#     lowest_freq_mels = 1127.0*math.log(1.0 + 0.0)
#     print 'lowest mel: ', lowest_freq_mels
#     highest_freq_mels = 1127.0*math.log(1.0 + highest_freq/700)
#     print 'highest mel: ', highest_freq_mels
#     step = (highest_freq_mels - lowest_freq_mels)/11
#     print 'step: ', step
#     filterbank_starts_mels = [lowest_freq_mels]
#     while (filterbank_starts_mels[len(filterbank_starts_mels) - 1] < highest_freq_mels - 1): # prevent rounding error
#         next_start = filterbank_starts_mels[len(filterbank_starts_mels) - 1] + step
#         filterbank_starts_mels.append(next_start)
# #     filterbank_starts.append(highest_freq_mels)
#     
#     print 'filters: ', len(filterbank_starts_mels)
#     print 'filterbank start positions in mels: ', filterbank_starts_mels
#     print
#         
#     #### convert back to herz
#     filterbank_starts_hz = []
#     for mel in filterbank_starts_mels:
#         converted = 700.0*(math.exp(mel/1125) - 1)
#         filterbank_starts_hz.append(converted)
#     print 'filterbank start positions in hzs: ', filterbank_starts_hz
#     
#     ### capture while inside 0--2, 1--3, 2--4 ...
#     print    
# #     while
#     
# #     ### graph spectrogram
# #     window = GraphWin("Spectrogram", time_step, 200)
# #     window.setCoords(0, 0, time_step, highest_freq)
# #     
# #     # at each time step, plot all frequencies at gray-scale intensity corresponding to magnitude    
# #     # maximum magnitude is black, minimum is white 
# #     for i in range(0, time_step):
# # 
# #         for j in range(0, nyquist):
# #             mag = time_steps[i][j]
# #             freq = j/(window_len_ms/1000.0)
# #             val = 255 - 255*((mag - minimum)/(maximum-minimum))
# #             window.plot(i, freq, color_rgb(val, val, val))
# #     
# #     window.getMouse()
# #     TK.mainloop() 
    
if __name__ == "__main__":
    main()