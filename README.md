# Part-Of-Speech-Tagger

- Built a hidden markov model part-of-speech tagger which works on any language 
- Achieved an accuracy of 93% for Italian and 91% for Japanese test sets

1. hmmlearn3.py will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.
2. hmmdecode3.py will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data,    and write the results to a text file called hmmoutput.txt in the same format as the training data.

hmmmodel.txt : Model created for the tagged training data in the Italian language
hmmoutput.txt : Output file in the word/TAG format for the untagged Italian language development data
