#Author: Saliha Minhas, Date: 29th September 2019

#Description
#This program reads in data constructed from
#read_kmeansfile_toextract_correspondinginfo_ fromrawdata file
# a number of csv files are constructed as a result of this pg 
#this program then attempts to plot results



library(ggplot2)
library (readxl)
library (tidyverse)


make_bargraph <- function(pdata1, cfile) {
  
  dat <- data.frame(pdata1, other_col='foo')
  dat <-as.data.frame((table(dat$dfall.recipient.country)))
  

  x<- ggplot(data=dat, aes(x=dat$Var1, y=dat$Freq)) +
    geom_bar(stat="identity", fill="steelblue", width=0.5)+
    theme(text = element_text(size=4),
          axis.text.y = element_text())
  
  x<- x + ggtitle(cfile) +
    xlab("recipient.country") + ylab("Frequency of mentions in cluster")
  
  x<- x + theme(
    plot.title = element_text(color="red", size=14, face="bold.italic"),
    axis.title.x = element_text(color="blue", size=9, face="bold"),
    axis.title.y = element_text(color="#993333", size=9, face="bold")
  )
  
  x<-x + coord_flip()
  
  return(x)
}

#set the working directory from which the files will be read from
setwd("C:/corpus4/Country")

#create a list of the files from your target directory
file_list <- list.files(path="C:/corpus4/Country")

#had to specify columns to get rid of the total column
for (i in 1:length(file_list)){
  cfile<- file_list[i]
  pdata1 <- read.csv(cfile, header=TRUE, sep=",")
 
  graph1 <- make_bargraph(pdata1, cfile)
  #png(file = paste (cfile, ".png"))
  
  tiff(file = paste (cfile, ".tiff"), units="in", width=5, height=5, res=300)
  
  plot (graph1)
  dev.off()
 }


library(data.table)
library(formattable)


pdata1 <- read.csv("cluster27.csv", header=TRUE, sep=",")
dat <-as.data.frame((table(pdata1$dfall.recipient.country)))
dat2 <- dat[with(dat, order(-Freq)), ]


formattable(dat2)




