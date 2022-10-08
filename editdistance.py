class EditDistance:
  def __init__(self,tx=None):
    self.tx =tx

  def edit_dist_step(self,lev,lev_path, i, j, c1, c2,s1,s2):
    if c1 != c2:
      s = lev[i-1][j-1] + 2
      p='S'# Substitution
    else:
      s = lev[i-1][j-1]
      p ='N' # no operation
    if i > 1 and j > 1:
      if s1[i - 2] == c2 and s2[j - 2] == c1:
        t = lev[i - 2][j - 2] + 1
        if t < s :
          p ='T'
          s = t
    d = lev[i-1][j ] + 1 
    if d< s:
      p ='D'
  
    i = lev[i ][j-1] + 1 
    if i < min(d,s) :
      p ='I'
#    print d,s,i
    l = min(d,s,i)
    return (l,p)

  def edit_dist_init(self,len1, len2): 
    lev = []

    for i in range(len1): 
      lev.append([0] * len2)  # initialize 2-D array to zero 
   
    for i in range(len1): 
      lev[i][0] = i           # column 0: 0,1,2,3,4,... 
      for j in range(len2): 
        lev[0][j] = j           # row 0: 0,1,2,3,4,... 
    return lev   

  def findTransformations(self,lev_path,i,j,trans):

    if lev_path[i][j] == 'O':
      if  j==1:
        trans.append(['I',j-2,j-1])
      if i ==1:
        trans.append(['D',i-2,i-1])
      return trans
    if lev_path[i][j] == 'N' or lev_path[i][j] == 'S':
      if lev_path[i][j] == 'S':
       
        trans.append(['S',i-1,j-1])
      return self.findTransformations(lev_path,i-1,j-1,trans)
    if lev_path[i][j] == 'D':
      trans.append(['D',i-2,i-1])
      return self.findTransformations(lev_path,i-1,j,trans)
    if lev_path[i][j] == 'I':
      trans.append(['I',j-2,j-1])
      return self.findTransformations(lev_path,i,j-1,trans)
    if lev_path[i][j] == 'T':
      trans.append(['T',i-2,i-1])
      return self.findTransformations(lev_path,i-2,j-2,trans)

  def edit_distance_transformation(self,s1, s2):
    len1 = len(s1)
    len2 = len(s2)

    lev = self.edit_dist_init(len1+1, len2+1)

    lev_path =[]
    for i in range((len1+1)): 
      lev_path.append(['O'] * (len2+1))  # initialize 2-D array to zero 

    for i in range(len1):
      lev_path.append([])
      for j in range (len2): 

        (l,p)=self.edit_dist_step(lev,lev_path, i+1, j+1, s1[i], s2[j],s1,s2) 
        lev[i+1][j+1] =l
        lev_path[i+1][j+1]=p

    t= self.findTransformations(lev_path,len1,len2,[])

    return (lev[len1][len2],t)

  def edit_distance(self,s1,s2):
    (l,t) = self.edit_distance_transformation(s1, s2)
    return l
  def edit_distance_trans(self,s1,s2):
    (l,t) = self.edit_distance_transformation(s1, s2)
    return t
if __name__ == "__main__":
  ed=EditDistance()
  s1= 'of'
  s2 ='fo'
  print ed.edit_distance(s1,s2)
  print ed.edit_distance_trans(s1,s2)
