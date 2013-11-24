"""
Sophia Davis
11/12/13
Problem 1, part a
This program gives a pitch estimation of a .wav file every 10 ms of audio.
"""
import sys
import wave
from graphics import *
import Tkinter as TK
import numpy
import math
import array
from scipy.signal import argrelextrema
import scipy.io.wavfile as wav

def main():
    if len(sys.argv) < 2:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' file.wav')
		sys.exit(1)
    file = sys.argv[1]

    (sampling_rate, stream_converted) = wav.read(file) # returns (sample rate, numpy.ndarray of samples)
    
    ### define parameters
    n_samps = len(stream_converted)
    window_len_ms = 25.0 # window length in milliseconds
    windowby_ms = 10.0 # milliseconds between consecutive window starting positions 
    samps_per_window = int(sampling_rate*(window_len_ms/1000)) # samples per window
    windowby_samps = int(sampling_rate*(windowby_ms/1000)) # samples between between consecutive window starting positions
    nyquist = samps_per_window/2 # nyquist frequency
    
    ### store maximum frequency (F1, ideally) from each window in a list
    # index by time step 
#     time_steps = {}

    window_start = 0
#     time_step = 0
#     maximum = 0
#     print n_samps/windowby_samps
    
    max_freqs = []
    
    ### perform Discrete Fourier Transform given samples in each window 
    # use DFT at each frequency to determine magnitude 
    while (window_start + samps_per_window) < n_samps:
        current_window = stream_converted[window_start : window_start + samps_per_window]
        dft_values = numpy.fft.fft(current_window)
        
        # calculate log magnitude at each frequency
        magnitudes = []
        window_max = 0
        max_freq = 0
        for i in range(0, nyquist):
            real = numpy.real(dft_values[i])
            imag = numpy.imag(dft_values[i])
            sq_mag = math.sqrt(math.pow(real, 2) + math.pow(imag, 2))
            mag = 10*math.log10(sq_mag)
            if  (mag > window_max):
                window_max = mag
                max_freq = i
            magnitudes = magnitudes + [mag]
            
        # store magnitudes for current window 
#         time_steps[time_step] = [magnitudes, window_max, max_freq]
        max_freqs.append(max_freq)
        
        # increment window_start by number of samples separating each window starting position
        # increment index for storing magnitudes by 1
        window_start += windowby_samps
    
    highest_freq = int(nyquist/(window_len_ms/1000.0))

#     for i in range(0, time_step):
#         window = GraphWin("spectrum", 400, 200)
#         window.setCoords(0, 0, highest_freq, time_steps[i][1]) # maximum
#         
#         for j in range(0, nyquist):
#             mag = time_steps[i][0][j]
#             freq = j/(window_len_ms/1000.0)
#             point1 = Point(freq, 0) 
#             point2 = Point(freq + 1, mag)
#             rect = Rectangle(point1, point2)
#             rect.draw(window)
#     
#         window.getMouse()
#         window.close()

    print max_freqs
#     print (window_len_ms/1000.0)
    
if __name__ == "__main__":
    main()