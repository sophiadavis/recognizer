import os
import random
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
    'french_argentina_clean_1.wav
    'french_argentina_clean_2.wav
    'french_argentina_clean_3.wav,']
    
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
    
    test_options =  list(en_1) + list(en_2) + \
            list(fr_1) + list(fr_2) + \
            list(ru_1) + list(ru_2)
    
    
    en_combos = []
    for en_1_file in en_1:
        for en_2_file in en_2:
            en_combos.append([en_1_file, en_2_file])
            
    fr_combos = []
    for fr_1_file in fr_1:
        for fr_2_file in fr_2:
            fr_combos.append([fr_1_file, fr_2_file])
            
    ru_combos = []
    for ru_1_file in ru_1:
        for ru_2_file in ru_2:
            ru_combos.append([ru_1_file, ru_2_file])
    
    training_combos = []
    for en in en_combos:
        for fr in fr_combos:
            for ru in ru_combos:
                training_combos.append([en, fr, ru])
    
    for training in training_combos:
        print training
    
    
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
#         training = en_train_1 + ' English ' + en_train_2 + ' English ' + \
#                 fr_train_1 + ' French ' + fr_train_2 + ' French ' + \
#                 ru_train_1 + ' Russian ' + ru_train_2 + ' Russian'
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
#             os.system("python recognizer.py " + file)
#             print '---'
#         
#         en_1.remove(en_train_1)
#         en_2.remove(en_train_2)
#         fr_1.remove(fr_train_1)
#         fr_2.remove(fr_train_2)
#         ru_1.remove(ru_train_1)
#         ru_2.remove(ru_train_2)
    

if __name__ == "__main__":
    main()