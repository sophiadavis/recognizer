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
    
    en_combos = []
    for en_1_file in en_1:
        for en_2_file in en_2:
            en_combos.append(['english', en_1_file, en_2_file])
            
    fr_combos = []
    for fr_1_file in fr_1:
        for fr_2_file in fr_2:
            fr_combos.append(['french', fr_1_file, fr_2_file])
            
    ru_combos = []
    for ru_1_file in ru_1:
        for ru_2_file in ru_2:
            ru_combos.append(['russian', ru_1_file, ru_2_file])
    
    training_combos = []
    for en in en_combos:
        for fr in fr_combos:
            for ru in ru_combos:
                training_combos.append([en, fr, ru])
    
    correct = []
    wrong = []
    
    num_trials = 0
    for training in training_combos:
#         print training
#         
        command = ''
        test = list(test_options)
        for lang_set in training:
            language = lang_set[0]
            file_1 = lang_set[1]
            file_2 = lang_set[2]
            command = command + ' ' + file_1 + ' ' + language + ' ' + file_2 + ' ' + language + ' '
            test.remove(file_1)
            test.remove(file_2)

        os.system("python train_recognizer.py " + command)
        
        
        for file in test:
            print 'testing: ' + file
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
    
    
    
#     while en_1:
#     
#         en_train_1 = random.choice(en_1)
#         en_train_2 = random.choice(en_2)
#         
#         fr_train_1 = random.choice(fr_1)
#         fr_train_2 = random.choice(fr_2)
#         
#         ru_train_1 = random.choice(ru_1)
#         ru_train_2 = random.choice(ru_2)
#         
#         training = en_train_1 + ' english ' + en_train_2 + ' english ' + \
#                 fr_train_1 + ' french ' + fr_train_2 + ' french ' + \
#                 ru_train_1 + ' russian ' + ru_train_2 + ' russian'
#         
#         test = list(test_options)
#         test.remove(en_train_1)
#         test.remove(en_train_2)
#         test.remove(fr_train_1)
#         test.remove(fr_train_2)
#         test.remove(ru_train_1)
#         test.remove(ru_train_2)
#         
#         print '---'
#         print training
#         print '-'
#         print test
#         print '---'
#                 
#         os.system("python train_recognizer.py " + training)
#         
#         for file in test:
#             print 'testing: ' + file
#             language = subprocess.check_output(["python", "recognizer.py", file]).strip('\n')
#             if re.search(language, file):
#                 print 'true', language, file
#             else:
#                 print 'false', language, file
#             print '---'
#             
#         
#         en_1.remove(en_train_1)
#         en_2.remove(en_train_2)
#         fr_1.remove(fr_train_1)
#         fr_2.remove(fr_train_2)
#         ru_1.remove(ru_train_1)
#         ru_2.remove(ru_train_2)
    

if __name__ == "__main__":
    main()