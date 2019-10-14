#Author: Saliha Minhas, First Version Date: 29th September 2019

#Description
#This program reads in raw IATI data to df, IATI dat must only have the 
#recipient-country,	description columns. The purpose of this
#program is to clean out the recipient-country column so that every row only
#has one country and one description




library(stringr)
# read in recipient-country,	description columns
newdataframe <- read.csv(file="C:/corpus3/data4.csv", row.names = NULL, header=TRUE, stringsAsFactors = FALSE, sep=",")

# set up an empty df where clean out entrues wil be  put

df2 <- data.frame(Country=character(),
                  Description = character(), 
                  stringsAsFactors=FALSE)

newrow = 1

clean_list <- function(chrlist) {
  list2 = list()
  ct =1
  for(i in chrlist){
    for(j in i){
      a<-tolower(j)
      a<-gsub("[\r\n]", "", j)
      list2[ct] = str_replace_all(a," ","")
      list2[ct] = str_replace_all(gsub(" ","",tolower(j)) , "[\r\n]" , "")
      list2[ct] = j
      ct = ct +1}
  }
  list2=list2[!duplicated(list2)]
  return (list2)
}


##########################

for (i in 1:nrow (newdataframe)){
  # clean out description
  split2 = strsplit(newdataframe[i,2], " ")
  retlist2 = clean_list(split2)
  temp = ""
  
  # put the descripton back together 
  for(i3 in 1:length(retlist2)){
    
    temp = paste(temp, retlist2[i3])
    
  }
 
  # clean out recipient-country
  if (newdataframe[i,1] != ""){
    split1 = strsplit(newdataframe[i,1], ";")
    retlist = clean_list(split1)
  }else{
    retlist[1] = ""
  }
 
  # update df2
  for(i2 in 1:length(retlist)){
    
    
    if (retlist[i2] == ""|retlist[i2] == " "){
      df2[newrow,1] = "EMPTY"
    } else {
      df2[newrow,1] = retlist[i2]
    }
    
    df2[newrow,2] = temp
    newrow = newrow +1 
  }
}  



