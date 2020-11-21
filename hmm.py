from datetime import datetime
from train import LanguageModel
import pickle
import twokenize
from nltk import word_tokenize


class HiddenMarkovModel:
    def __init__(self):
        self.lm = LanguageModel()
        self.n = self.lm.n
        self.model = None

    def viterbi(self, sentence, format='twitter'):
        # We lazily load the model
        if not self.model:
            self.model = self.lm.get_model()

        # First, we tokenize our sentence according to the format.
        tokens = twokenize.tokenize(sentence) if format == 'twitter' else word_tokenize(sentence) # TODO: Dont forget to lower case all the words!

        # Next, we set up some utility variables we will use in our algorithm.
        length = len(tokens)
        cap_lists = [self.__get_cap_list(word) for word in tokens]
        max_cap = max([len(cap) for cap in cap_lists])  # Find the maximum number of different types of capitalization.
        dp = [[0] * length for x in range(max_cap)]
        back = [[None] * length for x in range(max_cap)]

        # We initialize the first column of our dp matrix.
        num_caps = len(cap_lists[0])
        cap_list = cap_lists[0]
        for i in range(num_caps):
            back[i][0] = 0
            transition_probability = self.model['language_model'].score(cap_list[i], '<s>')
            if transition_probability == 0:
                dp[i][0] = float('-inf')
            else:
                emission_probability = self.model['langauge_model'].score(cap_list[i])
                dp[i][0] = transition_probability * emission_probability

        # Now, we populate our dp matrix.
        for i in range(1, length):
            num_caps = len(cap_lists[i])
            cap_list = cap_lists[i]
            for j in range(num_caps):
                temp_path, max_p = None, float('-inf')








    # def __get_

    def __get_cap_list(self, word):
        return list(self.model['capitalization'][word])






    # def train(self):
    #
    #
    #
    # def save_model(self, dir):
    #
    #
    #
    # def __create_backup(self, dir='/models/backups'):
    #     now = datetime.now()
    #     dt_string = now.strftime("%d.%m.%Y-%H.%M.%S")
    #     with open(f"{dt_string}.backup.model", "wb") as file:
    #         pickle.dump(self.model, file)
