from word_level import WordLevel
from nltk import SimpleGoodTuringProbDist, FreqDist,WittenBellProbDist
#from wordsegment import segment
from ngram import NGram
from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn
import operator
import re
import math
from nltk.corpus import stopwords
from nltk.corpus import brown
import nltk
import itertools

wl = WordLevel()
inv_indx = wl.getInvertedIndex() ## generating inverted index from the file where we stored inverted index for dictionary


class SentenceLevel:
  def __init__(self,tx=None):
    self.tx =tx
 
  def getBigram(self,wList):
    if len(wList) <2 :
      return [] # returning null list if word length is < 3
    bigram =[]
    i=0
    for j in range(1,len(wList)): 
      bigram.append((wList[j-1].lower(),wList[j].lower())) # storing bigrams
      i=i+1
    return bigram

  def getTrigram(self,wList):
    if len(wList) <3 :
      return [] # returning null list if word length is < 3
    trigram =[]
    i=0
    for j in range(2,len(wList)): 
      trigram.append((wList[j-2].lower(),wList[j-1].lower(),wList[j].lower())) # storing bigrams
      i=i+1
    return trigram


  def permutenew(self,l):
    if len(l)==1:
      return l[0]
    else:   
      lnew=[]
      for a in l[0]:
        for b in self.permutenew(l[1:]):
          lnew.append(a+' '+b)
      return lnew 

  def getReplacements(self,listoflist):
    replaceList =list(itertools.product(listoflist))
    

  def getCandidateReplacement(self,phrase):
    p_words = nltk.word_tokenize(phrase)
#    punt =['.','!',',',';',':','"','-','.-',",",'(',')','<','>','!','@','#','$','%','^','&','*','=','+','_']
#    for w in p_words:
#      if w in punt:

#        p_words.remove(w)
#    print p_words
 #   print p_words
#    if len(p_words)==1:
#      p_words =self.splitPhrase(p_words)
    candidate_rep_list =[]
    i=0
    for w in p_words:
      if wl.checkDictionary(w.lower()) ==0 :
        cs = wl.getCandidate(w.lower(),inv_indx)
    
          
        candidate_rep_list.append(cs[0:3])
      else:
        candidate_rep_list.append([w])
      i =i+1
    return self.permutenew(candidate_rep_list)

  def getBigramProbGdTuring(self,bigram):
    b1_count =u_gd_freq.prob(bigram[0])
    b12_count = b_gd_freq.prob(bigram)
    p =float(b12_count)/float(b1_count)
    return p

  def getTrigramProbGdTuring(self,trigram):
    t1_count =b_gd_freq.prob(trigram[0],trigram[1])
    t12_count = t_gd_freq.prob(trigram)
    p =float(t12_count)/float(t1_count)
    return p


  def getBigramProb(self,bigram):
    #b1_count=corpus_words.count(bigram[0])
    #b12_count=c_bigram.count(bigram)
    if bigram[0] in u_freq:
      b1_count=int(u_freq[bigram[0].lower()])
    else:
      b1_count=0
    if bigram in b_freq:
      
      b12_count=int(b_freq[bigram])
    else:
      b12_count =0
    v =len(u_freq)
    prob=float(b12_count+float(1)/float(v))/float(b1_count+1)
    return prob

  def getTrigramProb(self,trigram):
    #t1_count=c_bigram.count(trigram[1:3])
    #t12_count=c_trigram.count(trigram)
    if (trigram[1],trigram[2]) in b_freq:
      t1_count=int(b_freq[(trigram[1],trigram[2])])
    else:
      t1_count =0
    if trigram in t_freq:
      t12_count=int(t_freq[trigram])
    else:
      t12_count =0
    v = len(b_freq)    
    prob=float(t12_count+float(1)/float(v))/float(t1_count+1)
    return prob

  def synsetsWords(self,syns):
    sw =[]
    for s in syns:
      for l in s.lemmas:
        sw.append(l.name)
    return sw
  def getLinSim(self,syns1,syns2):
    max_sim =0
    for s1 in syns1:
      for s2 in syns2:
        if s1.pos == s2.pos:
          linsim =s1.lin_similarity(s2,semcor_ic)
          if linsim >max_sim:
            max_sim = linsim
    return max_sim
        
  def getCountCooccur_5gram(self,words):
    log_cnt =0
    for p in p_freq:
      if words[0] in p and words[1] in p:
        if words[0] in u_freq :
          log_cnt += float(math.log(p_freq[p]))/float(u_freq[words[0]])
    return log_cnt

  def distriCooccur(self,p_words): # using 5gram data , k=2
    p=0
    k=2
    for i in range(0,len(p_words)-1):
      if i+k+1 > len(p_words):
        k=1
      for j in range(i+1,i+k+1):
        log_cnt = self.getCountCooccur_5gram([p_words[i],p_words[j]])
        if log_cnt != 0:
          p += math.log(log_cnt)
      if i ==0:
        l=i
      elif i ==1:
        l =i-1
      else:
        l=i-2
      for j in range(l,i):
        log_cnt = self.getCountCooccur_5gram([p_words[i],p_words[j]])
        if log_cnt != 0:
          p += math.log(log_cnt)
    return p


  def getProbability(self,phrase):
    p_words = nltk.word_tokenize(phrase)
    p_words = ['<s>']+p_words+['</s>']
    p_bigram = self.getBigram(p_words)
    p_trigram = self.getTrigram(p_words)
    prob_bigram=0
    for bigram in p_bigram:
      prob_bigram +=math.log(self.getBigramProb(bigram))
    prob_trigram=0

    for trigram in p_trigram:
      prob_trigram +=math.log(self.getTrigramProb(trigram))
#    dis_sim = self.distributionalOverlap(p_words)
    dis_cooccur =self.distriCooccur(p_words)
    prob = 0.5*prob_bigram +0.5*prob_trigram
    prob =-float(2*dis_cooccur* prob)/float(dis_cooccur+prob)
    return prob

  def getsplitWords(self,w):
    j=len(w)
    words=[]
    i=len(w)-1
    while i>0:
      if w[i:j] in brown.words():
        words.insert(0,w[i:j])
        j=i
    return words

  def splitPhrase(self,p_words):
    p_words = segment(p_words[0])
    #p_tmp =[w for w in p_words]
    #for w in p_tmp:
    #  w1 =self.getsplitWords(w)
    #  if len(w1)>1:
    #    j=p_words.index(w)
    #    p_words.remove(w)
    #    for i in range(0,len(w1)):
    #      p_words.insert(j+i,w1[i])
    return p_words
  

  def findMispelt(self,phrase,c_phrase):
    p_words = nltk.word_tokenize(phrase)
    c_words = nltk.word_tokenize(c_phrase)
    misSpeltIndex ={}
    for w in p_words:
      if wl.checkDictionary(w.lower()) ==0:
        m=p_words.index(w)
        misSpeltIndex[m] = (c_words[m],w)
    return misSpeltIndex

  def meanRR_Phrase(self,misSpeltIdx,candidates):
    i=0
    can=[]
    for m in misSpeltIdx:
      can.append([])
      i +=1
    for c in candidates:
      c=c[0]
      c = nltk.word_tokenize(c)
      i=0
      for m in misSpeltIdx:
#        m=misSpeltIdx[i]
        if c[m] not in can[i]:
          can[i].append(c[m])
        i =i+1
    rank =0
    i=0
    for m in misSpeltIdx:
      if misSpeltIdx[m][0] in can[i]:
        rank += float(1)/float(can[i].index(misSpeltIdx[m][0])+1)
      print 'Misspelt Word:'+misSpeltIdx[m][1] +' Suggestions: '+str(can[i])
      i +=1
#    if len(misSpeltIdx) >0:
#      rank = float(rank) /float(len(misSpeltIdx))
    return rank
  

n=NGram()
sl =SentenceLevel()
#u_freq = n.unigram('Data/sen_1gram_brgw.txt')
#b_freq =n.bigram('Data/sen_2gram_brgw.txt')
#t_freq =n.trigram('Data/sen_3gram_brgw.txt')
u_freq = n.unigram('wordfrequency.txt')
b_freq =n.bigram('w2_.txt')
t_freq =n.trigram('w3_.txt')
p_freq =n.pentagram('w5_.txt')
#u_fd =FreqDist(u_freq)
#u_gd_freq =WittenBellProbDist(u_fd)
#b_fd =FreqDist(b_freq)
#b_gd_freq =WittenBellProbDist(b_fd)
#t_fd =FreqDist(t_freq)
#t_gd_freq =WittenBellProbDist(t_fd)
#corpus_words =[w.lower() for w in brown.words()]
#cachedStopWords = stopwords.words("english")
#semcor_ic = wordnet_ic.ic('ic-semcor.dat')
#context_unigram = n.unigram('Data/co_unigram_rbgw.txt')
#context_bigram =n.bigram('Data/co_bigram_rbgw.txt')
dw =open('count_big.txt').read()
dict_words =wl.words(dw)
#c_bigram =pl.getBigram(corpus_words)
#c_trigram =pl.getTrigram(corpus_words)
#con_uni =open('co_unigram1.txt').readlines()
#con_bi =open('co_bigram1.txt').readlines()
#context_unigram ={}
#for l in con_uni:
#  u=l.strip().split('\t')
#  context_unigram[u[0]]=u[1]
#context_bigram ={}
#for l in con_bi:
#  b=l.strip().split('\t')
#  context_bigram[b[0]+'_'+b[1]]=b[2]
#  
if __name__ == "__main__":
  input_data =open('sentence_input.tsv').readlines()
#  input_data =open('phrases_input.tsv').readlines()
  totMispelt =0
  sumRank =0
  for line in input_data:
    inp = line.strip().split('\t')
    inp_sen =inp[0]
    print inp_sen
    inp_sen = re.sub('[\,!\.\:\;\'\"\?]', '', inp_sen)
    correct_sen =inp[1]
    correct_sen = re.sub('[\,!\.\:\;\'\"\?]', '', correct_sen)
    misSpeltIndex = sl.findMispelt(inp_sen,correct_sen)    
    totMispelt +=len(misSpeltIndex)
    candidate_rep =sl.getCandidateReplacement(inp_sen)
    sen_rank={}
    for c in candidate_rep:
      sen_rank[c]=sl.getProbability(c)
    sorted_p =sorted(sen_rank.iteritems(),key=operator.itemgetter(1))
    rank =sl.meanRR_Phrase(misSpeltIndex,sorted_p)
    sumRank += rank
    print '---------------'
    #print inp_sen, sorted_p[0][0],rank
  mrr =float(sumRank)/float(totMispelt)
  print totMispelt ,mrr
     
    
