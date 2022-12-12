import numpy as np
import tensorflow as tf
import pickle
from tensorflow import keras

class LSTMPredictionService():
    def __init__(self, LSTM_model_path, input_dictionary_path, reverse_dictionary_path, max_sequence_lenght, latent_dim):
        self.latent_dim = latent_dim
        self.input_dict = self.load_dictionary(reverse_dictionary_path)[0]
        self.reverse_dict = self.load_dictionary(reverse_dictionary_path)[1]
        self.max_sequence_len = max_sequence_lenght

        self.encoder_model = None
        self.decoder_model = None
        self.load_model(LSTM_model_path)

        print("LSTM Prediction service initialized!")

    def load_model(self, path):
        model = keras.models.load_model(path)

        encoder_inputs = model.input[0]  # input_1
        encoder_outputs, state_h_enc, state_c_enc = model.layers[2].output  # lstm_1
        encoder_states = [state_h_enc, state_c_enc]
        self.encoder_model = keras.Model(encoder_inputs, encoder_states)
        self.encoder_model.summary()

        decoder_inputs = model.input[1]  # input_2
        decoder_state_input_h = keras.Input(shape=(self.latent_dim,), name="input_h")
        decoder_state_input_c = keras.Input(shape=(self.latent_dim,), name="input_c")
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_lstm = model.layers[3]
        decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
            decoder_inputs, initial_state=decoder_states_inputs
        )
        decoder_states = [state_h_dec, state_c_dec]
        decoder_dense = model.layers[4]
        decoder_outputs = decoder_dense(decoder_outputs)
        self.decoder_model = keras.Model(
            [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
        )
        self.decoder_model.summary()

    def load_dictionary(self, path):
        loaded_dictionary = None
        try:
            loaded_dictionary = pickle.load(open(path, 'rb'))
            if (loaded_dictionary is not None):
                return loaded_dictionary
            else:
                raise Exception("[ERROR] Dictionary object not loaded!")
        except Exception as e:
            print(e.with_traceback())


    def inference(self, sentence):
        #Encoding sentence to vector
        input_seq = np.zeros((1, self.max_sequence_len, len(self.input_dict)), dtype="float32")

        for t, char in enumerate(sentence):
            input_seq[0, t, self.input_dict[char]] = 1.0
        input_seq[0, t + 1 :, self.input_dict[" "]] = 1.0

        print(f"[DEBUG] Input sequence shape: {input_seq.shape}")

        # Encode the input as state vectors.
        states_value = self.encoder_model.predict(input_seq)

        # Generate empty target sequence of length 1.
        target_seq = np.zeros((1, 1, len(self.reverse_dict)))
        # Populate the first character of target sequence with the start character.
        target_seq[0, 0, self.input_dictionary_path["\t"]] = 1.0

        # Sampling loop for a batch of sequences
        # (to simplify, here we assume a batch of size 1).
        stop_condition = False
        decoded_sentence = ""
        while not stop_condition:
            output_tokens, h, c = self.decoder_model.predict([target_seq] + states_value)

            # Sample a token
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_char = self.reverse_dict[sampled_token_index]
            decoded_sentence += sampled_char

            # Exit condition: either hit max length
            # or find stop character.
            if sampled_char == "\n" or len(decoded_sentence) > self.max_sequence_len:
                stop_condition = True

            # Update the target sequence (of length 1).
            target_seq = np.zeros((1, 1, len(self.reverse_dict)))
            target_seq[0, 0, sampled_token_index] = 1.0

            # Update states
            states_value = [h, c]
        return decoded_sentence