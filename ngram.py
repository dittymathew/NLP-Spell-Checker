class NGram:
  def __init__(self,tx=None):
    self.tx =tx

  def unigram(self,fn):
    text =open(fn).readlines()
    #text =open('wordfrequency.txt').readlines()
    unigramf ={}
    for line in text:
      line =line.strip()
      u_details =line.split('\t')
      #print u_details[0],u_details[1]
      unigramf[u_details[0]] =int(u_details[1])
    return unigramf

  def bigram(self,fn):
    text =open(fn).readlines()
    #text =open('w2_.txt').readlines()
    bigramf ={}
    for line in text:
      line =line.strip()
      b_details =line.split('\t')
      #print b_details
      bigramf[(b_details[1],b_details[2])] =int(b_details[0])
    return bigramf

  def trigram(self,fn):
    text =open(fn).readlines()
    #text =open('w3_.txt').readlines()
    trigramf ={}
    for line in text:
      line =line.strip()
      t_details =line.split('\t')
      trigramf[(t_details[1],t_details[2],t_details[3])] =int(t_details[0])
    return trigramf

  def pentagram(self,fn):
    text =open(fn).readlines()
    #text =open('w3_.txt').readlines()
    pentagramf ={}
    for line in text:
      line =line.strip()
      p_details =line.split('\t')
      pentagramf[(p_details[1],p_details[2],p_details[3],p_details[4],p_details[5])] =int(p_details[0])
    return pentagramf
if __name__ == "__main__":
  n =NGram()
  print n.unigram()
  print n.bigram()
  print n.trigram()
