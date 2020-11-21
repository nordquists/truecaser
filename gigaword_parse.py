"""

We iterate through each article in the directories file, while there are DOCS
we read the P tags, each of which accessible through an API.

As far as the class works:
    (1) We read a single gzip into memory and give sentences as they are asked for
        with the next() method.
    (2) Once we are out of sentences, we open the next file in the list.

"""
import gzip


class GigawordParser:
    def __init__(self, input_file="giga_directories.txt", base_dir="../../../misc/proteus1/data/EnglishGigaWordCorpus/data/"):
        # Note: input file is a txt with all the gzips we are interested in

        self.base_dir = base_dir

        self.todo = self.__create_todo(input_file)
        self.todo_index = 0

        self.current_file = []
        self.file_index = 0

        # Analytics that we will ask for at the end
        self.sentences_processed = 0

    def get_sentences_processed(self):
        return self.sentences_processed

    @staticmethod
    def __create_todo(input_file):
        todo = []
        with open(input_file, 'r') as file:
            for line in file:
                todo.append(line.rstrip())

        return todo

    def __load_sentences(self, file):
        sentences = []
        is_sentence = False
        current_sentence = ""
        try:
            with gzip.open(self.base_dir + file, 'r') as file:
                for line in file:
                    line = line.decode('utf-8')
                    line = line.replace('\n', ' ')
                    if "<P>" in line:
                        is_sentence = True
                        current_sentence = ""
                    elif "</P>" in line:
                        is_sentence = False
                        sentences.append(str(current_sentence))
                        current_sentence = ""
                    elif is_sentence:
                        current_sentence += line

            return sentences
        except:
            print(f"ERROR: Could not find {file}")
            return []

    def next(self):
        # If we don't have a current_file yet or we are out of bounds, we read the next file.
        if not self.current_file or self.file_index >= len(self.current_file):
            # We have read through every file already
            if self.todo_index > len(self.todo):
                return None

            file_to_read = self.todo[self.todo_index]
            self.todo_index += 1

            print(f'PARSER: Now parsing {file_to_read}')

            self.current_file = self.__load_sentences(file_to_read)
            self.file_index = 0

        output_sentence = self.current_file[self.file_index]
        self.file_index += 1
        self.sentences_processed += 1

        return output_sentence
