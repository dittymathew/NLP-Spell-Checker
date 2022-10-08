from phrase_level import PhraseLevel
from nltk.corpus import brown

pl =PhraseLevel()
corpus_words =[w.lower() for w in brown.words()]
c_bigram =pl.getBigram(corpus_words)
c_trigram =pl.getTrigram(corpus_words)
b_unigram ={}
b_unigram = {word:corpus_words.count(word) for word in corpus_words} # bigram frequency
b_bigram ={}
b_bigram = {word:c_bigram.count(word) for word in c_bigram} # bigram frequency
b_trigram ={}
b_trigram = {word:c_trigram.count(word) for word in c_trigram} # bigram frequency
uni =open('unigram.txt','w')
for u in b_unigram:
  uni.write(b_unigram[u]+'\t'+u)
bi =open('bigram.txt','w')
for b in b_bigram:
  bi.write(b_bigram[b]+'\t'+b)
tri =open('trigram.txt','w')
for t in b_trigram:
  tri.write(b_trigram[t]+'\t'+t)
