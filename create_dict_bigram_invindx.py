from nltk.corpus import brown
from nltk.corpus import words

def getTrigram(w):
  i=0
  if len(w) <2 :
    return []
  trigram =[]
  for j in range(1,len(w)):
    if w[i:j+1] not in trigram:
      trigram.append(w[i:j+1])
    i=i+1
  trigram =set(trigram)
  return trigram

def writeTrigramInvIdxDict():
  trigram_dict =createInvertedIndex()
  w_trigram =open('bigram_inverted_indx_dict_big.txt','w')
  for t in trigram_dict:
    wstr =str(t)
    for index in trigram_dict[t]:
      wstr += '\t'+str(index)
    wstr += '\n'
    w_trigram.write(wstr)
  w_trigram.close()
   

###Creating Inverted index for dictionary 
def createInvertedIndex():
  #dictwords =open('word.list').readlines()
  dw =open('count_big.txt').readlines()
  dictwords =[l.split('\t')[0] for l in dw]
  #dictwords =words.words()
  tri_set ={}
  i=0
  for dw in dictwords:
    dw_trigram =getTrigram(dw.lower())
    for dw_t in dw_trigram:
      if dw_t not in tri_set:
        tri_set[dw_t] = []
      tri_set[dw_t].append(dictwords.index(dw))
      print dw_t, dw, dictwords.index(dw)
    i=i+1
  print tri_set
  return tri_set    
  
writeTrigramInvIdxDict()



