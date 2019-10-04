#Author: Saliha Minhas, First Version Date: 29th September 2019

#Description
# read in df that has contains embeddings of the most frequently occuring unigrams 
# obtained from topfrequencies_and_their_embeddings_saved_todf pgm. Then flatten using
#tsne and plot


train<- read.csv("C:/Users/s-minhas/Downloads/train.csv") ## Choose the train.csv file downloaded from the link above  

library(Rtsne)
train2 <-x3
#train2 <- word_vectors


## Curating the database for analysis with both t-SNE and PCA
Labels<-train2[,1]
Labels<-rownames(train2)

#train2$label<-as.factor(train2$list_of_names)

## for plotting
#colors = rainbow(length(unique(train2[,1])))
colors = rainbow(length(unique(rownames(train2))))

## Executing the algorithm on curated data


#train2 = train2[1:nrow(train2),-1]
train2 = train2[1:nrow(train2),]
train2 <- as.data.frame(train2[,-1])
train2 = apply(train2, 2, as.numeric)


tsne <- Rtsne(train2, dims = 2, perplexity=5, verbose=TRUE, max_iter = 500)

## Plotting
plot(tsne$Y, t='n', main="tsne")
text(tsne$Y, labels=x3[,1], col=colors[x3[,1]])




