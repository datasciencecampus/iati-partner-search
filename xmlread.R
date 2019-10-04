#Author: Saliha Minhas,  Date firstUpdated: 29th September 2019

#Description
#This program was the initial program that attempted to read in XML
#but it has been superseded


library(XML)

a<- c(list.files (path = "C:/corpus3", recursive = TRUE))

path = "C:/corpus3"
for(f in a){
  dir.x <- sprintf("%s/%s", path, f)
  
  result <- xmlParse(file = dir.x)
  b<-xmlToDataFrame(nodes = getNodeSet(result, "//*/description/narrative"))
  write.table(x = b,
              file = "C:/temp/first.txt",col.names = FALSE, row.names = FALSE, append = TRUE,
              sep = "\t")        
}
