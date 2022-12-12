from abc import abstractmethod

class Encoder():

    def __init__(self):
        feature_set = []
        label_set = []        

    @abstractmethod
    def encode_feature_set(self, input_file, output_file):
        pass

    @abstractmethod
    def encode_label_set(self, input_file, output_file):
        pass

    @abstractmethod
    def save_dataset(self, filename):
        pass
    
    @abstractmethod
    def save_dictionary(self, filename):
        pass

    @abstractmethod
    def load_dataset(self, filename):
        pass