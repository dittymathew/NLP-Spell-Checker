words =open('word.list').readlines()
wp=open('word_1_2_dict.list',"w")
for w in words:
  if len(w.strip())<=2:
    wp.write(w)
wp.close()

