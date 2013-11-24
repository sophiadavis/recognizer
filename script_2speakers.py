import os
import random
import re
import subprocess
"""
train on one obama and one swedish sentence per language
    run recognizer on all other files
    
    russian_obama_clean_1

"""
def main():
    codebook = False
    
    en_1 = [
    'english_obama_clean_1.wav',
    'english_obama_clean_2.wav',
    'english_obama_clean_3.wav']

    fr_1 = [
    'french_obama_clean_1.wav',
    'french_obama_clean_2.wav',
    'french_obama_clean_3.wav']

    ru_1 = [
    'russian_obama_clean_1.wav',
    'russian_obama_clean_2.wav',
    'russian_obama_clean_3.wav']

    en_2 = [
    'english_sweden_clean_1.wav',
    'english_sweden_clean_2.wav',
    'english_sweden_clean_3.wav']

    fr_2 = [
    'french_sweden_clean_1.wav',
    'french_sweden_clean_2.wav',
    'french_sweden_clean_3.wav']

    ru_2 = [
    'russian_sweden_clean_1.wav',
    'russian_sweden_clean_2.wav',
    'russian_sweden_clean_3.wav']
    
    test_options =  list(en_1) + list(en_2) + \
            list(fr_1) + list(fr_2) + \
            list(ru_1) + list(ru_2)
    
    # this test method finds all possible permutations of the files to train on
    # there are 3^7 = 2187 total sets, so it would take over 40 hours to train/test all...
    
    # total permutations of english files (1 from each speaker)
    en_combos = []
    for en_1_file in en_1:
        for en_2_file in en_2:
            en_combos.append(['english', en_1_file, en_2_file])
    
    # total permutations of french files (1 from each speaker)        
    fr_combos = []
    for fr_1_file in fr_1:
        for fr_2_file in fr_2:
            fr_combos.append(['french', fr_1_file, fr_2_file])
    
    # total permutations of russian files (1 from each speaker)    
    ru_combos = []
    for ru_1_file in ru_1:
        for ru_2_file in ru_2:
            ru_combos.append(['russian', ru_1_file, ru_2_file])
    
    # all permutations between languages
    training_combos = []
    for en in en_combos:
        for fr in fr_combos:
            for ru in ru_combos:
                training_combos.append([en, fr, ru])
    
    # train and test some of the sets formed above
    correct = []
    wrong = []
    
    num_trials = 0
    num_training_sets = 0
    
    while num_training_sets < 10:
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
            command = command + ' ' + file_1 + ' ' + language + ' ' + file_2 + ' ' + language + ' '
            test.remove(file_1)
            test.remove(file_2)

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