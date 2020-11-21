from config import MIN_TWEET_CAP_CONFIDENCE


class TwitterParser:
    def __init__(self, input_file="classified.dev.csv", base_dir="./data/twitter/"):
        self.current_file = self.__load_tweets(base_dir, input_file)
        self.file_index = 0

        # Analytics that we will ask for at the end
        self.sentences_processed = 0

    def get_sentences_processed(self):
        return self.sentences_processed

    def __load_tweets(self, base_dir, file):
        tweets = []
        with open(base_dir + file, 'r') as file:
            for line in file:
                # Splits at most once from the right-most comma
                tweet, confidence = line.rsplit(',', 1)

                if float(confidence) > MIN_TWEET_CAP_CONFIDENCE:
                    tweets.append(tweet)

        return tweets

    def next(self):
        if self.file_index >= len(self.current_file):
            return None

        output_sentence = self.current_file[self.file_index]
        self.file_index += 1
        self.sentences_processed += 1

        return output_sentence
