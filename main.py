from train import LanguageModel

lm = LanguageModel()

# lm.load_model()

model = lm.get_model()

lm.save_model()

# print(len(model['language_model'].vocab))
#
# print(model['language_model'].counts[['itchy']]['and'])
#
# print(model['language_model'].score('Is'))
#
# print(model['capitalization']['sucks'])
#
#
