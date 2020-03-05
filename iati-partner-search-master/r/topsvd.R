#Author: Saliha Minhas, First Version Date: 29th September 2019

#Description
# read in df that has contains embeddings of the most frequently occuring unigrams 
# obtained from topfrequencies_and_their_embeddings_saved_todf pgm. Then flatten usind
#svd and plot




library(irlba)


train2 <-x3
#train2 <- word_vectors[500:550,]
#train2 <- word_vectors


temp = as.matrix(train2[1:nrow(train2),-1])
temp = apply(temp, 2, as.numeric)
pmi_svd <- irlba(temp, 2, maxit = 500)

#next we output the word vectors:
word_vectors2 <- pmi_svd$u
rownames(word_vectors2) <- x3[1:nrow(train2),1]
#rownames(word_vectors2) <- rownames(word_vectors)



#grab 100 words
forplot<-as.data.frame(word_vectors2)
forplot$word<-rownames(forplot)

#now plot
library(ggplot2)
ggplot(forplot, aes(x=V1, y=V2, label=word))+
  geom_text(aes(label=word),hjust=0, vjust=0, color="blue")+
  theme_minimal()+
  xlab("First Dimension Created by SVD")+
  ylab("Second Dimension Created by SVD")












