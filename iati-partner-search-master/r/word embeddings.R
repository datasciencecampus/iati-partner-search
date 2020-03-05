#Author: Saliha Minhas, First Version Date: 29th September 2019

#Description
#This program reads in raw IATI data to df 
#and then uses text2vec functions to create word embeddings

library(text2vec)
library(tm)
library(tidyverse)

## load in data

# switch on if you want to read in data from a file
#DataOrig <- read.csv(file="C:/corpus3/test10k.csv", header=TRUE, sep=",")

#otherwise use variable where records are stored
df100 <-all_downloaded_records

DataOrig <- df100

# some quick preprocosssing
preprocess <- function(x) {
  
  x <- (as.character(x))
  x <- removeNumbers(x)
  x <- removePunctuation(x)
  x <- tolower(x)
  x <- removeWords(x,stopwords("english"))
  x <- stripWhitespace(x)
  
  return (x)
  
}

## pick up data of interst the iati identifier and description
a = as.vector(DataOrig$description) 
a = preprocess(a)

# Create iterator over tokens
tokens <- space_tokenizer(a)
# Create vocabulary. Terms will be unigrams (simple words).
it = itoken(tokens, preprocess_function = tolower, 
            tokenizer = word_tokenizer, chunks_number = 10, progressbar = FALSE)

corpus <- create_vocabulary(it)

# a token must appear at least 5 times
vocab <- prune_vocabulary(corpus, term_count_min = 5L)


# Use our filtered vocabulary
vectorizer <- vocab_vectorizer(vocab)

# use window of 5 for context words
tcm <- create_tcm(it, vectorizer, skip_grams_window = 5L)



glove = GlobalVectors$new(word_vectors_size = 50, vocabulary = vocab, x_max = 10)

word_vectors_main  = glove$fit_transform(tcm,n_iter=20)

#And now we get the word vectors:
word_vectors_context <- glove$components
word_vectors = word_vectors_main + t(word_vectors_context)



### Examples - get similarity scores for healthcare and rates based on vector capture
##of semantics

rom = word_vectors["healthcare", , drop = F]
cos_sim_rom = sim2(x = word_vectors, y = rom, method = "cosine", norm = "l2")

head(sort(cos_sim_rom[,1], decreasing = T), 10)

word2 = word_vectors["reproductive", , drop = F]
cos_sim_rom = sim2(x = word_vectors, y = word2, method = "cosine", norm = "l2")

head(sort(cos_sim_rom[,1], decreasing = T), 10)

















