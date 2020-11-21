"""

Unifies the gigaword and twitter parser into one object so the corpora can
easily be traversed when training the model.

"""

from gigaword_parse import GigawordParser
from twitter_parse import TwitterParser


class Parser:
    def __init__(self):
        self.gigaword_parser = GigawordParser()
        self.twitter_parser = TwitterParser()

        # This is true once we move on to the twitter parser
        self.has_advanced = False

    def next(self):
        if not self.has_advanced:
            next_sentence = self.gigaword_parser.next()

            if next_sentence:
                return 'giga', next_sentence

            self.has_advanced = True

            print("PARSER: Now parsing twitter corpus")

        next_sentence = self.twitter_parser.next()

        if next_sentence:
            return 'tweet', next_sentence

        return None, None
