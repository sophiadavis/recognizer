"""
script_4speakers.py
Sophia Davis, for 11/25/2013
NLP final project

This script trains and tests models of differences in spoken languages based on excerpts 
from translations of four UN speeches. It calculates all permutations of training sets 
(consisting of one recording excerpted from all speeches for each language), then randomly 
picks (n_reps) of these permutations. For each one, it trains a model, then tests the model 
on all recordings not used to form the model.

The parameter 'codebook' indicates which method should be used to guess the source 
of the test file:
If codebook = True, the 'codebook' method will be used (average MFCC vectors from windows 
where the maximum intensity occurred at similar frequencies).
If codebook = False, the simple method will be used (average MFCC vectors over all windows).
"""

import os
import random
import subprocess
import re

def main():
    codebook = True # use 'codebook' vs simple method of guessing source of test file
    n_reps = 10 # number of random permutations of training data to run
      
    en_1 = [
    'english_obama_clean_1.wav',
    'english_obama_clean_2.wav',
    'english_obama_clean_3.wav']

    en_2 = [
    'english_sweden_clean_1.wav',
    'english_sweden_clean_2.wav',
    'english_sweden_clean_3.wav']
    
    en_3 = [
    'english_ukraine_clean_1.wav',
    'english_ukraine_clean_2.wav',
    'english_ukraine_clean_3.wav']

    en_4 = [
    'english_argentina_clean_1.wav',
    'english_argentina_clean_2.wav',
    'english_argentina_clean_3.wav']
    
    fr_1 = [
    'french_obama_clean_1.wav',
    'french_obama_clean_2.wav',
    'french_obama_clean_3.wav']

    fr_2 = [
    'french_sweden_clean_1.wav',
    'french_sweden_clean_2.wav',
    'french_sweden_clean_3.wav']
    
    fr_3 = [
    'french_ukraine_clean_1.wav',
    'french_ukraine_clean_2.wav',
    'french_ukraine_clean_3.wav']

    fr_4 = [
    'french_argentina_clean_1.wav',
    'french_argentina_clean_2.wav',
    'french_argentina_clean_3.wav']
    
    ru_1 = [
    'russian_obama_clean_1.wav',
    'russian_obama_clean_2.wav',
    'russian_obama_clean_3.wav']
    
    ru_2 = [
    'russian_sweden_clean_1.wav',
    'russian_sweden_clean_2.wav',
    'russian_sweden_clean_3.wav']
    
    ru_3 = [
    'russian_ukraine_clean_1.wav',
    'russian_ukraine_clean_2.wav',
    'russian_ukraine_clean_3.wav']
    
    ru_4 = [
    'russian_argentina_clean_1.wav',
    'russian_argentina_clean_2.wav',
    'russian_argentina_clean_3.wav']
    
    test_options =  list(en_1) + list(en_2) + list(en_3) + list(en_4) +\
            list(fr_1) + list(fr_2) + list(fr_3) + list(fr_4) +\
            list(ru_1) + list(ru_2) + list(ru_3) + list(ru_4)
        
    
    en_combos = []
    for en_1_file in en_1:
        for en_2_file in en_2:
            for en_3_file in en_3:
                for en_4_file in en_4:
                    en_combos.append(['english', en_1_file, en_2_file, en_3_file, en_4_file])
            
    fr_combos = []
    for fr_1_file in fr_1:
        for fr_2_file in fr_2:
            for fr_3_file in fr_3:
                for fr_4_file in fr_4:
                    fr_combos.append(['french', fr_1_file, fr_2_file, fr_3_file, fr_4_file])
            
    ru_combos = []
    for ru_1_file in ru_1:
        for ru_2_file in ru_2:
            for ru_3_file in ru_3:
                for ru_4_file in ru_4:
                    ru_combos.append(['russian', ru_1_file, ru_2_file, ru_3_file, ru_4_file])
    
    # all permutations between languages
    training_combos = []
    for en in en_combos:
        for fr in fr_combos:
            for ru in ru_combos:
                training_combos.append([en, fr, ru])
    
    correct = []
    wrong = []
    
    num_trials = 0
    num_training_sets = 0
    
    while num_training_sets < n_reps:
        print num_training_sets
        training = random.choice(training_combos)
        training_combos.remove(training)
        num_training_sets += 1
        
        command = ''
        test = list(test_options)
        for lang_set in training:
            language = lang_set[0]
            file_1 = lang_set[1]
            file_2 = lang_set[2]
            file_3 = lang_set[3]
            file_4 = lang_set[4]
            command = command + ' ' + file_1 + ' ' + language + ' ' + file_2 + ' ' + language + ' ' + file_3 + ' ' + language + ' ' + ' ' + file_4 + ' ' + language
            test.remove(file_1)
            test.remove(file_2)
            test.remove(file_3)
            test.remove(file_4)
        
        if codebook:
            os.system("python train_recognizer_codebook.py " + command)
        else:
            os.system("python train_recognizer.py " + command)
        
        for file in test:
            print 'testing: ' + file
            if codebook:
                language = subprocess.check_output(["python", "recognizer_codebook.py", file]).strip('\n')
            else:
                language = subprocess.check_output(["python", "recognizer.py", file]).strip('\n')
            if re.search(language, file):
                print 'true', language, file
                correct.append([language, file])
            else:
                print 'false', language, file
                wrong.append([language, file])
            print '---'
            num_trials += 1
    
    print
    print '**********'
    print 'TRIALS: ', num_trials
    print '**********'
    print 'CORRECT: ', len(correct)
    for item in correct:
        print item
    print '**********'
    print 'INCORRECT: ', len(wrong)
    for item in wrong:
        print item
    print '**********'
    print
    
if __name__ == "__main__":
    main()