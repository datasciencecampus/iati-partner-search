#Author: Kevin Carolan, Saliha Minhas,  First Version Date: 29th September 2019

#Description
#This program reads in file that has cleaned up country and description columns
#preprocessing is done on the description column, frequencies are obtained for every unigram
# for the highest 50 frequencies, the corresponding vector embeddings are saved for plotting
#wordcloud is used to plot the highest frequency words and a table is also constructed.

library(tm)
library(tidyverse)
library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")


## load in data

DataOrig <- read.csv(file="C:/corpus1/df2.csv", header=TRUE, sep=",")

#DataOrig <- read.csv(file="C:/corpus3/test10k.csv", header=TRUE, sep=",")

#DataOrig <- df100
#a <- as.vector(DataOrig$description) 

e = filter(df2, df2$Country == "EMPTY")
a <- as.vector(e$Description)

#x <- (as.character(DataOrig$description))

x <- (as.character(e$Description))
x <- removePunctuation(x)
x <- tolower(x)
x <- removeWords(x,stopwords("english"))
x <- stripWhitespace(x)


x1 <- tail(sort(table(unlist(strsplit(x," ")))),50) # top ten most frequent words (still need to remove spare blankspace)

selected_word_vector_rows=array(NA,dim=c(50,50))
list_of_names=0
for(this_row_to_extract in 1:50){
  list_of_names[this_row_to_extract]= as.character(unlist(dimnames(x1))[this_row_to_extract])
  if(length(word_vectors[which(rownames(word_vectors) == as.character(unlist(dimnames(x1))[this_row_to_extract]))])==0){next}  
  selected_word_vector_rows[this_row_to_extract,]=word_vectors[which(rownames(word_vectors) == as.character(unlist(dimnames(x1))[this_row_to_extract]))]
  }

x3= cbind(list_of_names,selected_word_vector_rows)
x3 <- na.omit(x3)


xd<- data.frame(x1, stringsAsFactors = FALSE)


set.seed(1234)
wordcloud(words = xd$Var1, freq = xd$Freq, min.freq = 1,
          max.words=50, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))



xd <- xd[order(-xd$Freq),] 


kable(xd, caption = "Top 50 Unigrams by Raw Frequency")

library(kableExtra)
kable(ad) %>%
  kable_styling("striped", full_width = F) %>%
  column_spec(1:2, bold = T) %>%
  row_spec(1:50, bold = T, color = "white", background = "#D7261E")
  
  
 
