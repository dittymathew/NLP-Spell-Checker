# NLP-Spell-Checker
#Word Level
1.1. Preprocessing

We have created tri-gram index for the dictionary. For the misspelt word, a
first level candidate set can be selected by look into the tri-gram index.

1.2. Pruning the search space
After selecting candidate words from the dictionary using tri-gram index,
a second level pruning is done based on edit distance between given word
and all the words in the current candidate set. Here all candidates having
edit distance less than or equal to 3 are selected. If given word length is less
than or equal to 2, then for first level pruning, all words having a length less
than or equal to 2 are selected.

1.3. Algorithm

Input : Word w
Output : Suggestions for w if w is a misspelt word
1. If w is in the dictionary, return w (correct word)
2. Else , get candidates based on pruning method mentioned above. Also,
to capture the candidates which have the same sound, candidates having
same Soundex are selected.
3. For each words in the candidate set,
(a) Find the edit distance transformations
(b) For each transformations find the probability from the confusion
tables of transformation operation and find product of probability
for all the transformations. This is the likelihood measure.
(c) Calculate the prior probability
(d) To give importance to candidate words having less edit distance
(especially for edit distance 1), setting more weight to edit distance
1 and less weight to edit distance 3. Learned weights after trained with some examples are, for edit distance 1 set 0.9, for 2
sets 0.1 and for 3 sets 0.001.
(e) To give importance to words having same Soundex values, setting
a Soundex score 0.9, if both the words are having the same sound,
otherwise Soundex score 0.001
(f) Calculate the probability of candidate words by using all these
values as follows
• prob = 0.3 * likelihood *prior + 0.4 *editDistanceScore * prior + 0.3 *soundexScore *prior
4. Sort the candidates based on ’prob’ and return the first five candidates
as suggestions

##Phrase Level

2.1. Algorithm

Input : Phrase to check for spelling correction Output : Misspelt word in
the phrase with suggestions
1. Each word in the input is checked against all the words in the dictionary.
If the word is present in the dictionary, then it becomes its own
candidate replacement. If not, then the word is passed as input to the
Word Spell Check and its candidate replacements are obtained.
2. For each misspelt word in the given phrase , its candidate replacements
are substituted and a set of candidate suggestions for complete phrase
is got.
3. For each candidate suggestion obtained in the above step, the set of
tri-grams and bi-grams contained in it are extracted.
4. The frequencies of the tri-grams, bi-grams and uni-grams are obtained
from the N gram data set (Free frequent n-grams data based on Corpus
of Contemporary American English).
5. Using these frequencies, we compute the joint probability of each candidate
suggestion using ngram model in log space. We used interpolation
technique to mix bi-grams and tri-grams.
6. The candidate suggestion having the maximum score is reported as
the correct phrase

#Sentence Level

3.1. Algorithm

Input : Sentence to check for spelling correction Output : Misspelt word in
the sentence with suggestions
1. Got the candidate replacements as per the method mentioned in the
phrase level.
2. Same N gram data set used in the phrase level are used here also.
3. Probability obtained using ngram model are also obtained.
4. To obtain the distributional co-occurrence score of each word with a
context window size 2, we used 5gram data obtained from same Ngram
dataset.
5. Combined distributional co-occurrence score and Ngram score using
F1 score.
6. The candidate suggestion having the maximum score is reported as
the correct sentence.


#Smoothing method

Used Add K smoothing with m=1

#Resources

Dictionary

Corpora
• Brown corpus from nltk library
• Free frequent n-grams data based on Corpus of Contemporary American
English downloaded from the url http://www.ngrams.info

#Evaluation

Evaluation is done using the Mean Reciprocal Rank measure.