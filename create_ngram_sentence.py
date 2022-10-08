from nltk.corpus import brown,gutenberg,webtext
from nltk.corpus import reuters
from nltk.corpus import stopwords
import re
ww =open('tmpword.txt','w')
word_alpha =re.compile('(\w)|(<s>)|(</s>)')
def getNgram(wList,n):
  if len(wList) <n :
    return [] # returning null list if word length is < 3
  ngram =[]
  i=0
  for j in range(0,len(wList)-n+1): 
    w ='('
    flg =0
    for k in range(0,n):

      w += wList[j+k].lower()+','
#     if wList[j+k].lower() not in dict_words and  wList[j+k] not in ['<s>','</s>']:
      if re.match(word_alpha,wList[j+k].lower()) is None or len(wList[j+k])==0:
      #  print 'non alpha ' +wList[j+k]
        flg =1
#      else:
#        ww.write(wList[j+k]+' , '+str(len(wList[j+k]))+'\n')
    if flg ==0 :
      w = w[0:len(w)-1]+')'
    ngram.append(w) # storing bigrams
    i=i+1
  return ngram

corpus_sents =[s for s in reuters.sents()]
corpus_words =[w.lower() for w in reuters.words()]
for s in brown.sents():
  corpus_sents.append(s)
for w in brown.words():
  corpus_words.append(w)
for s in gutenberg.sents():
  corpus_sents.append(s)
for w in gutenberg.words():
  corpus_words.append(w)
for s in webtext.sents():
  corpus_sents.append(s)
for w in webtext.words():
  corpus_words.append(w)
dict_words =open('word.list').readlines()
dict_words = [d.strip().lower() for d in dict_words]

unigram_freq ={}
bigram_freq ={}
trigram_freq ={}
qgram_freq ={}
fivegram_freq ={}
punt =['.','!',',',';',':','"','-','.-',",",'(',')','<','>','!','@','#','$','%','^','&','*','=','+','_',' ']
for s in corpus_sents:
  for w in s:
    if w in punt:
      s.remove(w)  
           
  s =['<s>'] +s+['</s>']
  
  u_gram = getNgram(s,1)
  for u in u_gram:
    if u not in unigram_freq:
      unigram_freq[u] = 0
    unigram_freq[u] += 1
  b_gram = getNgram(s,2)
  for b in b_gram:
    if b not in bigram_freq:
      bigram_freq[b] = 0
    bigram_freq[b] += 1
  t_gram = getNgram(s,3)
  for t in t_gram:
    if t not in trigram_freq:
      trigram_freq[t] = 0
    trigram_freq[t] += 1
  q_gram = getNgram(s,4)
  for q in q_gram:
    if q not in qgram_freq:
      qgram_freq[q] = 0
    qgram_freq[q] += 1
  f_gram = getNgram(s,5)
  for f in f_gram:
    if f not in fivegram_freq:
      fivegram_freq[f] = 0
    fivegram_freq[f] += 1
    

      
uni =open('Data/sen_1gram_brgw.txt','w')
bi =open('Data/sen_2gram_brgw.txt','w')
tri =open('Data/sen_3gram_brgw.txt','w')
qg =open('Data/sen_4gram_brgw.txt','w')
fiveg =open('Data/sen_5gram_brgw.txt','w')
for u in unigram_freq:
  uf = u.strip('(').strip(')')
  if re.match(word_alpha,uf.lower()) :

    uni.writelines(uf+'\t'+str(unigram_freq[u])+'\n')
for b in bigram_freq:
  bf = b.strip('(').strip(')').split(',')
  
  if re.match(word_alpha,bf[0].lower()) and re.match(word_alpha,bf[1].lower()) :
    bi.writelines(str(bigram_freq[b])+'\t'+bf[0]+'\t'+bf[1]+'\n')
for t in trigram_freq:
  tf = t.strip('(').strip(')').split(',')
  if re.match(word_alpha,tf[0].lower()) and re.match(word_alpha,tf[1].lower()) and re.match(word_alpha,tf[2].lower()) :
    tri.writelines(str(trigram_freq[t])+'\t'+tf[0]+'\t'+tf[1]+'\t'+tf[2]+'\n')
for q in qgram_freq:
  qf = q.strip('(').strip(')').split(',')
  if re.match(word_alpha,qf[0].lower()) and re.match(word_alpha,qf[1].lower()) and re.match(word_alpha,qf[2].lower()) and re.match(word_alpha,qf[3].lower()):
    qg.writelines(str(qgram_freq[q])+'\t'+qf[0]+'\t'+qf[1]+'\t'+qf[2]+'\t'+qf[3]+'\n')
for f in fivegram_freq:
  ff = f.strip('(').strip(')').split(',')
  if re.match(word_alpha,ff[0].lower()) and re.match(word_alpha,ff[1].lower()) and re.match(word_alpha,ff[2].lower()) and re.match(word_alpha,ff[3].lower())and re.match(word_alpha,ff[4].lower()):
    fiveg.writelines(str(fivegram_freq[f])+'\t'+ff[0]+'\t'+ff[1]+'\t'+ff[2]+'\t'+ff[3]+'\t'+ff[4]+'\n')

        
