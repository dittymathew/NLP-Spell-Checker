from nltk.corpus import reuters
from nltk.corpus import brown
from nltk.corpus import words
from nltk.metrics.distance import edit_distance
import re,collections
import math
import fuzzy
import operator
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()

from editdistance import EditDistance
ed =EditDistance()

class WordLevel:

  def __init__(self,tx=None):
    self.tx =tx

## taking trigram of input word
  def getTrigram(self,w):
    if len(w) <3 :
      return [w] # returning null list if word length is < 3
    trigram =[]
    i=0
    for j in range(2,len(w)): 
      trigram.append(w[i:j+1]) # storing trigrams
      i=i+1
    trigram =set(trigram) #taking unique trigrams
    return trigram


  ## generating inverted index from the file where we stored inverted index for dictionary
  def getInvertedIndex(self):
    tri_inv_indx = open('trigram_inverted_indx_dict_big.txt').readlines() # open inverted index file and reading by lines
    inverted_index ={} # intializing dictionary to store the file data
    for line in tri_inv_indx: # reading line by line
      line =line.split("\t") # spliting the line contents into words
      key = line[0] # taking trigram as key(hashmap key) to store in the inverted index
      data = line[1:len(line)] # taking indices of words from file data 
    
      inverted_index[key]=data # assigning to inverted index
    return inverted_index


## getting candidate set based on trigram by looking into inverted index
  def getCandidateSetTrigram(self,trigram,inv_indx):
  #  dict_words =words.words() # taking words from dictionary
    candidateset =[] # intializing candidate set
    for t in trigram :
      if t in inv_indx :
        c_words = [dict_words[int(i)].strip() for i in inv_indx[t]] #
        for cw in c_words :
          candidateset.append(cw)
    return list(set(candidateset))


   ##pruning the candidate list based on edit distance (taking candidate if its edit distance <4)
  def getCandidatePrunEditDistance(self,word,candidateset):
    prunned_cs =[]
    edit_cs ={}
    k=5
    for cs in candidateset:
      edit = ed.edit_distance(cs,word) # nltk edit distance function
      edit_cs[cs] =edit
      if len(word)<3:
        if edit <=1 :
          prunned_cs.append(cs)
      elif edit <=3 :
        prunned_cs.append(cs)
    if len(prunned_cs)<k :
      addcs =[cs for cs,e in edit_cs.iteritems() if e ==4]
      for c in addcs :
        prunned_cs.append(c)
  #  sorted_p =sorted(edit_cs.iteritems(),key=operator.itemgetter(1))
  #  j=min(k,len(sorted_p))
#  for i in range(0,j):
#    prunned_cs.append(sorted_p[i][0])
#  for l in range(j,len(sorted_p)):
#    if sorted_p[l][1]==sorted_p[j][1]:
#      prunned_cs.append(sorted_p[l][0])
#  print prunned_cs 
#    if edit <=3 :
#     prunned_cs.append(cs)
    return prunned_cs

  def prior(self,word):
  #  corpus_words =[w.lower() for w in brown.words()]
    w_count = corpus_words.count(word)
    N = len(corpus_words)
    p = float(w_count+1)/float(N+len(set(corpus_words)))
    return p

  def getVal(self,x,y,filenm):
    del_data =open('ConfusionTables/deletiontable.csv').readlines()
    Y = del_data[0].strip().split(',')
    y_loc =Y.index(y) 
    for line in del_data:
      line =line.split(',')
      if line[0] == x:
        val =int(line[y_loc])
        return val
    return 0
  
  def getCount(self,x):
    n=0
    for w in corpus_words:
      n += w.count(x)
    if n==0:
      n=1
    return n

  def getProb(self,correct,typo,t):
    if t[0] == 'D':
      char_xy = self.getVal(correct[t[1]],correct[t[2]],'ConfusionTables/deletiontable.csv')
      char_x = self.getCount(correct[t[1]]+correct[t[2]])
    if t[0] == 'I':
      char_xy = self.getVal(typo[t[1]],typo[t[2]],'ConfusionTables/insertionstable.csv')
      char_x = self.getCount(typo[t[1]])
    if t[0] == 'S':
      char_xy = self.getVal(correct[t[1]],typo[t[2]],'ConfusionTables/substitutionstable.csv')
      char_x = self.getCount(correct[t[1]])
    if t[0] == 'T':
      char_xy = self.getVal(correct[t[1]],correct[t[2]],'ConfusionTables/transpositionstable.csv')
      char_x = self.getCount(correct[t[1]]+correct[t[2]])
    #if char_x ==0:
    #  char_x =0.1
    p = float(int(char_xy)+(float(1)/float(26)))/float(int(char_x)+1)
    return p

  def getLikelihood(self,correct,typo):
    trans =ed.edit_distance_trans(correct,typo)
    p=1
    for t in trans:
    
      p *= self.getProb(correct,typo,t)
    return p

  def getSoundex(self,word):
    soundex = fuzzy.Soundex(4)
    return soundex(word)

  def getSoundexCandidates(self,word):
    cs =[]
    w_sound = self.getSoundex(word)
    for i in range (0,len(dict_words)):
      dw =dict_words[i]
      if w_sound == self.getSoundex(dw) and ed.edit_distance(word.lower(),dw.lower())<=3:
      #if w_sound == self.getSoundex(dw) :
        cs.append(dw.lower())  
      dict_words[i] =dw.lower() 
    return cs

  def getCandidate(self,word,inv_indx):
    
    if(len(word.strip())<=2):
      re=open('word_1_2_dict.list').readlines()
      candidate_trigram=[]
      for bi_word in re:
        candidate_trigram.append(bi_word.lower().strip())
        
    else:
      trigram_input = self.getTrigram(word.strip()) ## taking trigram of input word
      candidate_trigram =self.getCandidateSetTrigram(trigram_input,inv_indx) ## getting candidate set based on trigram by looking into inverted index
    cs =self.getCandidatePrunEditDistance(word, candidate_trigram) ##pruning the candidate list based on edit distance (taking candidate if its edit distance <4)
    sound_cs = self.getSoundexCandidates(word)
#    print sound_cs
    for ws  in sound_cs:
      cs.append(ws.lower())
    p_post ={}
    word_sound =self.getSoundex(word.strip())
    word =word.lower().strip()
#    print cs
    for c in cs:
      l =self.getLikelihood(c.strip().lower(),word.strip().lower())
      pr = self.prior(c.strip())
#      editsim = float(1)/float(math.pow(1+ed.edit_distance(word.strip().lower(),c.strip().lower()),2))
      edit =ed.edit_distance(word.strip().lower(),c.strip().lower())
      editsim ={1:0.9,2:0.5,3:0.00001,4:0.001}  
      if edit not in editsim:
        editsim[edit]=0
      if len(c)<2:
        s_score =1
      else:
        c_sound = self.getSoundex(c)
        c =c.lower()
        if word_sound == c_sound:
          s_score =0.99
        else :
          s_score=0.0001
#      print word.strip().lower(),c.strip().lower()
      p = (0.3*l*pr)+(0.4*editsim[edit]*pr)+(0.3*s_score*pr)
#      p = (float(1)/float(3)*l*pr)+(float(1)/float(3)*editsim[edit]*pr)+(float(1)/float(3)*s_score*pr)
#      print word,c,p ,l*pr
#      p = pr*editsim[edit]
      p_post[c] =1-p
    sorted_p =sorted(p_post.iteritems(),key=operator.itemgetter(1))
    p_cs =[c[0] for c in sorted_p][0:5]
#    print word.strip(),': ',p_cs
    return p_cs

  def checkDictionary(self,w):

    if w in dict_words :
      return 1
    return 0

  def words(self,text): 
    return re.findall('[a-z]+', text.lower())

  def unigram_word(self,words):
    u_words ={}
    for l in words:
        lw = l.strip().split('\t')
        w = lw[0].lower()
        u_words[w] = lw[1]
    return u_words

wl =WordLevel()
#dict_words =open('word.list').readlines()
#dict_words =list(set(brown.words()))
#dw =open('count_big.txt').readlines()
#unigram =wl.unigram_word(dw)
#dict_words =[w for w in unigram]
#print dict_words[1:100]
dw =open('count_big.txt').read()
dict_words =wl.words(dw)

dict_words = [d.strip().lower() for d in dict_words]
corpus_words =[w.lower() for w in brown.words()]

if __name__ == "__main__":
  inv_indx = wl.getInvertedIndex() ## generating inverted index from the file where we stored inverted index for dictionary
  #word ='acress' ## input word trying one word now
  inputfile =open('testdata/words2.txt')
  inputdata =inputfile.readlines()
  mrr =0
  q=0
  for line in inputdata:
    line =line.strip().split('\t')
    mispelt_w = line[0]
    correct_w =line[1]
    if mispelt_w in dict_words:
      print mispelt_w.strip(), ' : CORRECT WORD'
      r_rank =1
    else:
      r_rank=0
      cs =wl.getCandidate(mispelt_w,inv_indx)
      print mispelt_w.lower() +':'+ str(cs)
      for i in range(0,len(cs)):
        if cs[i]==correct_w:
          print  mispelt_w, i+1
          r_rank = float(1)/float(i+1)
          break
    mrr += r_rank
    q +=1
  mrr =float(mrr)/float(q)
  print mrr
#  cs1 =getCandidatePrunEditDistance(word, list(set(words.words()))) ##pruning the candidate list based on edit distance (taking candidate if its edit distance <4)



