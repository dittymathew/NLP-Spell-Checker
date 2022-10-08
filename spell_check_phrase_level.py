from word_level import WordLevel
from nltk import SimpleGoodTuringProbDist, FreqDist,WittenBellProbDist
from wordsegment import segment
from ngram import NGram
from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn
import operator
import math
from nltk.corpus import stopwords
from nltk.corpus import brown
import nltk
import itertools

wl = WordLevel()
inv_indx = wl.getInvertedIndex() ## generating inverted index from the file where we stored inverted index for dictionary


class PhraseLevel:
  def __init__(self,tx=None):
    self.tx =tx
 
  def getBigram(self,wList):
    if len(wList) <2 :
      return [] # returning null list if word length is < 3
    bigram =[]
    i=0
    for j in range(1,len(wList)): 
      bigram.append((wList[j-1],wList[j])) # storing bigrams
      i=i+1
    return bigram

  def getTrigram(self,wList):
    if len(wList) <3 :
      return [] # returning null list if word length is < 3
    trigram =[]
    i=0
    for j in range(2,len(wList)): 
      trigram.append((wList[j-2],wList[j-1],wList[j])) # storing bigrams
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
 
  def combineWordsinPhrase(self,p_words):
    np_words =[]
    i=0
    while(i<len(p_words)):  
      w=p_words[i]
      k=1
      for j in range(i+1,len(p_words)):
        if w+p_words[j] in dict_words:
          w +=p_words[j]
          k +=1 
        else:
          break
      np_words.append(w)
      i= i+k
    return np_words
          
    

  def getCandidateReplacement(self,phrase):
    p_words = nltk.word_tokenize(phrase)
    if len(p_words)==1:
      p_words =self.splitPhrase(p_words)
    p_words = self.combineWordsinPhrase(p_words)
    candidate_rep_list =[]
    i=0
    for w in p_words:
      if wl.checkDictionary(w) ==0:
        cs = wl.getCandidate(w,inv_indx)
    
          
        candidate_rep_list.append(cs[0:5])
      else:
        candidate_rep_list.append([w])
      i =i+1
    return self.permutenew(candidate_rep_list)


  def getBigramProbGdTuring(self,bigram):
    b1_count =u_gd_freq.prob(bigram[0])
    b12_count = b_gd_freq.prob(bigram)
#    print b1_count ,b12_count
    if b1_count != 0:
      p =float(b12_count)/float(b1_count)
    else:
      p=0
   
    return p

  def getTrigramProbGdTuring(self,trigram):
    t1_count =b_gd_freq.prob((trigram[0],trigram[1]))
    t12_count = t_gd_freq.prob(trigram)
#    print t1_count ,t12_count
    if t1_count !=0:
      p =float(t12_count)/float(t1_count)
    else:
      p=0
    return p
#--

  def getTotCount(self,ngram):
    count =0
    for i in ngram:
      count += ngram[i]
    return count

  def katzSmoothing(self,ngram,w):
    if ngram[w] >0:
      return ngram[w]


  def getUnigramProb(self,unigram):
    if unigram in u_freq:
      p =float(u_freq[unigram])/float(totfreq)
    else :
      p=0
    return p

  def getBigramProb(self,bigram):
    #b1_count=corpus_words.count(bigram[0])
    #b12_count=c_bigram.count(bigram)
    if bigram[0] in u_freq:
      b1_count=int(u_freq[bigram[0]])
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
    v =len(b_freq)
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
        
    
  def distributionalCooccur(self,p_words):
    pw =[]
    for w in p_words:
      if w not in cachedStopWords:
        pw.append(w)
    prod_p =1
    k=0
    for i in range(0,len(pw)-1):
      for j in range(i+1,len(pw)):
         if pw[i]+'_'+pw[j] in context_bigram:
           pij = context_bigram[pw[i]+'_'+pw[j]]
         else:
           pij =0
         if pw[i] in context_unigram:
           pi = context_unigram[pw[i]]
           p = float(pij)/float(pi)
         else:
           p=0
         prod_p *=p
         k +=1
    avg_p = prod_p**(1.0/k)
    return avg_p


  def distributionalOverlap(self,p_words):
    pw =[]
    for w in p_words:
      if w not in cachedStopWords:
        pw.append(w)
    sum_cos =1
    flg=0
    k=0
    for i in range(0,len(pw)-1):
      for j in range(i+1,len(pw)):
        t1 =wn.synsets(pw[i])
        t2 =wn.synsets(pw[j])
        if t1 !=[]  and t2 !=[]:
          sum_cos *=self.getLinSim(t1,t2)
        else:
          flg +=1
        k =k+1
    if flg == k:
      sum_cos =0
    avg_cos = sum_cos**(1.0/k)
    return avg_cos
        
  def getCountCooccur_5gram(self,words):
    log_cnt =0
    for p in p_freq:
      if words[0] in p and words[1] in p:
        log_cnt += math.log(p_freq[p])
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
    return p

  def getInterpolateProb(self,phrase):
    p_words = nltk.word_tokenize(phrase)
    p=0
    for i in range(0,len(p_words)):
      triP=0
      biP=0
      if i>1:
        triP =self.getTrigramProb((p_words[i],p_words[i-1],p_words[i-2]))
      if i>0:
        biP =self.getBigramProb((p_words[i],p_words[i-1]))
      uniP =self.getUnigramProb(p_words[i])
      p_ = (0.4*triP) + (0.4*biP) + (0.2*uniP)
      if p_ !=0:
        p += math.log(p_)
    return p
      
  

  def getProbability(self,phrase):
    p_words = nltk.word_tokenize(phrase)
    p_bigram = self.getBigram(p_words)
    p_trigram = self.getTrigram(p_words)
    prob_bigram=0
    for bigram in p_bigram:
      p = self.getBigramProb(bigram)
      if p !=0:
        prob_bigram +=math.log(p)
    prob_trigram=0

    for trigram in p_trigram:
      p =self.getTrigramProb(trigram)
      if p!=0:
        prob_trigram +=math.log(p)
#    dis_sim = self.distributionalOverlap(p_words)
#    dis_cooccur =self.distributionalCooccur(p_words)
#    print phrase,dis_cooccur
   # dis_cooccur =self.distriCooccur(p_words)
  #  prob = 0.5*prob_bigram +0.5*prob_trigram
 #   prob =-float(2*dis_cooccur* prob)/float(dis_cooccur+prob)
    prob = -(0.5*prob_bigram +0.5*prob_trigram)
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
      if wl.checkDictionary(w) ==0:
        m=p_words.index(w)
        misSpeltIndex[m] = c_words[m]
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
      if misSpeltIdx[m] in can[i]:
        rank += float(1)/float(can[i].index(misSpeltIdx[m])+1)
      print 'Misspelt Word:'+misSpeltIdx[m] +' Suggestions: '+str(can[i])
      i +=1
#    if len(misSpeltIdx) >0:
#      rank = float(rank) /float(len(misSpeltIdx))
    return rank
  
n=NGram()
pl =PhraseLevel()
wl=WordLevel()
u_freq = n.unigram('wordfrequency.txt')
b_freq =n.bigram('w2_.txt')
t_freq =n.trigram('w3_.txt')
totfreq=0
for u in u_freq:
  totfreq +=u_freq[u]
dw =open('count_big.txt').read()
dict_words =wl.words(dw)
ntext_bigram[b[0]+'_'+b[1]]=b[2]
  
if __name__ == "__main__":
  input_data =open('testdata/phrases2.txt').readlines()
  totMispelt =0
  sumRank =0
  for line in input_data:
    inp = line.strip().split('\t')
    inp_phrase =inp[0]
    correct_phrase =inp[1]
    misSpeltIndex = pl.findMispelt(inp_phrase,correct_phrase)    
    totMispelt +=len(misSpeltIndex)
    candidate_rep =pl.getCandidateReplacement(inp_phrase)
    phrase_rank={}
    for c in candidate_rep:
      phrase_rank[c]=pl.getProbability(c)
#      phrase_rank[c]=pl.getInterpolateProb(c)
    sorted_p =sorted(phrase_rank.iteritems(),key=operator.itemgetter(1))
    rank =pl.meanRR_Phrase(misSpeltIndex,sorted_p)
    sumRank += rank
    print inp_phrase, sorted_p[0][0] ,rank
  mrr =float(sumRank)/float(totMispelt)
  print totMispelt ,mrr
     
    
