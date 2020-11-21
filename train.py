"""

States correspond to a certain capitalization structure for a particular word. This is done
because states are more complicated than just one letter capitalized or all capitalized --
as an example of an exception, we can look at names like "McKenna."

"""
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
from nltk import word_tokenize
from parse import Parser
from datetime import datetime
from collections import defaultdict
import pickle
import twokenize
from functools import partial

class LanguageModel:
    def __init__(self, n=3):
        self.n = n
        self.model_loaded = False
        self.model = {
            'language_model': MLE(n),
            'capitalization': {}
        }

    def __track_capitalization(self, capitalization_dict, tokens):
        for token in tokens:
            capitalization_dict[token.lower()].add(token)

    def __load_sentences(self):
        tokenized_sentences = []
        capitalization = defaultdict(partial(set))

        parser = Parser()

        type, sentence = parser.next()

        while sentence:
            if type == 'tweet':
                tokens = twokenize.tokenize(sentence)
            else:
                tokens = word_tokenize(sentence)

            self.__track_capitalization(capitalization, tokens)
            tokenized_sentences.append(tokens)

            type, sentence = parser.next()

        return capitalization, tokenized_sentences

    def get_model(self, retrain=False):
        if self.model_loaded:
            return self.model
        elif retrain:
            self.load_model()

            if self.model_loaded:
                return self.model

        capitalization, sentences = self.__load_sentences()
        train_data, padded_sentences = padded_everygram_pipeline(self.n, sentences)

        print("SYSTEM: Parsing done. Now training the language model.")

        self.model['capitalization'] = capitalization
        self.model['language_model'].fit(train_data, padded_sentences)
        self.model_loaded = True

        print("SYSTEM: Language model trained.")

        self.__create_backup()
        return self.model

    def save_model(self, name="language.model", dir="./models/"):
        with open(f'{dir}{name}', "wb") as file:
            pickle.dump(self.model, file)

    def load_model(self, name="language.model", dir="./models/"):
        try:
            with open(f'{dir}{name}', "rb") as file:
                self.model = pickle.load(file)
                self.model_loaded = True
        except:
            return None

    def __create_backup(self, dir='backups/'):
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y-%H.%M.%S")
        self.save_model(name=f"{dir}language.{dt_string}.backup.model")
