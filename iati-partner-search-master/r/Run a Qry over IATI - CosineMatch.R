#Author: Saliha Minhas, Date: 29th September 2019

#Description
#This program reads in raw IATI data to df 
#then sets  up a query, does some preprocessing, 
# then sets up a TDM and then for every 
# row in TDM compares query vector with 
# the the row descriotion of iati vector
# using cosine similarity,
#return thoise vectors in description
#by rank that has greatest similarity score


library(tm)
library(tidyverse)

## load in data
DataOrig <- read.csv(file="C:/corpus3/test10k.csv", header=TRUE, sep=",")


## pick up data of interest the iati identifier and description
my_list= as.vector(DataOrig$description) 
my_list= unlist(my_list) 
b= as.vector(DataOrig$iati.identifier) 
b= unlist(b) 
names(my_list) <- c(b)


start_time <- Sys.time()

## set up a query - put in here what you want to search
query="The general objective of TRESMED IV is to continue to strengthen the consultative role of social and economic partners in the Mediterranean beneficiary countries under the European Neighbourhood policy instrument"  
qry = unlist(strsplit(query,"\n"))


## get data ready for term doc matrix
docs <- VectorSource(c(my_list, qry))
docs$Names <- c(names(my_list), "query")
corpus1 <- VCorpus(docs)
corpus1

### do a bit of preprocessin on text

#remove punctuation
corpus1 <- tm_map(corpus1, removePunctuation)
#remove numbers, uppercase, additional spaces
corpus1 <- tm_map(corpus1, removeNumbers)
corpus1 <- tm_map(corpus1, content_transformer(tolower))
corpus1 <- tm_map(corpus1, stripWhitespace)
corpus1 <- tm_map(corpus1, removeWords, stopwords("english"))
#create document matrix in a format that is efficient and ensure scoring is tf idf

term.doc.matrix <- TermDocumentMatrix(corpus1,control = list(weighting = function(x) weightTfIdf(x, normalize =TRUE)))

#switch on if required
#term.doc.matrix <- removeSparseTerms(term.doc.matrix, 0.7)


# ensure correct labelling is in place for TDM
colnames(term.doc.matrix) <- c(names(my_list), "query")

# have a look at it
inspect(term.doc.matrix[155:214, ])


## get data ready for cosine calc and comparison
##set up an empty df - x1 which will contain results of cosine

tdm_mat = as.matrix(term.doc.matrix)
s.df <- t(as.data.frame(tdm_mat, stringsASFactors = TRUE))
x1=data.frame(Cosine=rep(as.double(NA),nrow(s.df)))


##pick out qry from dataframe (last row)
qv = s.df[nrow(s.df),] 

#go through every row in main data DF - s.df  extracted and compare with qry and put results in x1
rownames(x1) <- rownames(s.df)
for (r in 1:(nrow(s.df)-1)) {
      
     a=s.df[r,]
     x1[r,1]= coop::cosine(a,qv)
}


## sort and display
head(x1[order(-x1$Cosine), , drop = FALSE],20)
end_time <- Sys.time()
print (end_time - start_time)