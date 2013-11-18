"""
takes in .wav files to train MFCC codebooks

## at each relative maxima on a window, take the average of the features

bin range of frequencies
count up number of times there is a relative maximum on a frequency over a sound stream
normalize the number
use in regression model?? minimum edit distance?
"""
import sys
import deltas
import numpy
from features import mfcc
import scipy.io.wavfile as wav
import pickle

def main():
    
    # to run: python train_recognizer.py language1.wav language1_name language2.wav language2_name
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
        mfccs_deltas = deltas.get_deltas(mfcc_feat, 0)
        mfccs_deltas_ddeltas = deltas.get_deltas(mfccs_deltas, 13)
        avg = deltas.col_avg(mfccs_deltas_ddeltas)
        
        if language in languages.keys():
            array = numpy.vstack((languages[language], avg))
            new_avg = deltas.col_avg(array)
            languages[language] = new_avg
        else:
            languages[language] = avg
    
    for language in languages.keys():
        print languages[language]
        print len(languages[language])
    pickle.dump(languages, open('languages_obama_1_sweden_1.dat', 'w'))
    print
    
if __name__ == "__main__":
    main()