Language Recognizer

Sophia Davis
Final Project for Carleton NLP, Fall 2013
For detailed information on methods and results, please see report.pdf


To train models:

    codebook method:
        python train_recognizer_codebook.py language1.wav language1_name language2.wav language2_name ...
    simple method:
        python train_recognizer.py language1.wav language1_name language2.wav language2_name ...


To test sound recordings:

    codebook method: python recognizer_codebook.py 'english_obama_clean_1.wav'
    simple method: python recognizer.py 'english_obama_clean_1.wav'


The current languages.dat and languages_codebook.dat have been trained on the following:

english_obama_clean_1.wav

english_sweden_clean_2.wav

french_obama_clean_1.wav

french_sweden_clean_3.wav

russian_obama_clean_2.wav

russian_sweden_clean_1.wav


The following scripts can be used to train and test many permutations of training and test sets:
    
    script_2speakers.py
    
    script_3speakers.py (unfamiliar-speaker model)
    
    script_4speakers.py
    

Sound files are clips of translations of speeches from the Sept. 24th, 2013 UN General Assembly 
(http://gadebate.un.org/).
