import os
import numpy as np
import pickle

from LexicalEditor.LexicalEditor import LexicalEditor

class Vectorizer():
    def __init__(self, dictinary_path):
        self.lex_editor = LexicalEditor()
        self.word_dictionary = None
        self.inverse_dictionary = {}
        self.load_dictionary(dictinary_path)


    #Loads dictionary object from pickle binary data. Also creates inverse dictionary for "resentencing".
    def load_dictionary(self, filepath):
        file = open(filepath, 'rb')                         #Loading pickle dictionary
        self.word_dictionary = pickle.load(file)

        for key, value in self.word_dictionary.items():     #Building inverse dictionary
            self.inverse_dictionary[value] = key


    #Removes all punctuation and turns all words into base form.
    def preprocess_sentence(self, sentence):
        return self.lex_editor.process_sentence(sentence)


    #Returns a 0 - 1 vector representation of a sentence.
    def vectorize_sentence(self, sentence):
        if (self.word_dictionary == None):
            raise Exception("Dictionary not loaded!")
        
        sentence_array = self.preprocess_sentence(sentence)
        sentence_vector = np.zeros(len(self.word_dictionary))

        for word in sentence_array:
            if (word in self.word_dictionary):
                sentence_vector[self.word_dictionary[word]] = 1.0
            else:
                print("[WARNING] Word {} not in dictionary! Skipping word!".format(word))

        return sentence_vector

    #Returns list of words corresponding to the vector without any time data.
    def resentence(self, sentence_vector):
        if (self.word_dictionary == None):
            raise Exception("Dictionary not loaded!")

        word_list = []
        for i in range(0, len(sentence_vector)):
            if (sentence_vector[i] == 0):
                continue

            if (i in self.inverse_dictionary):
                word_list.append(self.inverse_dictionary[i])

        return word_list