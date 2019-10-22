# open the already downloaded .xml files. 
# how do we associate them with eg IATI ID and coutnry and all? 



require(XML)
data <- xmlParse("C://Users//k-carolan//DFID//EXTERNAL - ONS-DFID Data Science Hub - iatikitcache//registry//data//_admin//asfpakistan-activities.xml")

xml_data <- xmlToList(data)

xml_data$`iati-activity`$`iati-identifier` # will give the IATI ID
paste(unlist(xml_data$`iati-activity`$description),collapse=" ") # Will give description; TO TEST; how does this interact with cases with multiple descriptions?
paste(xml_data,collapse=" ") # Gives all the text in the entry. 

# Open all files in the shared space 
filepath <- "C://Users//k-carolan//DFID//EXTERNAL - ONS-DFID Data Science Hub - iatikitcache//registry//data"
list_of_folders <- list.files(filepath) # just to note, output is a vector not a list (odd function name)

# Storage objects (just declare they exist)
IATI_ID=0
DESCRIPTION=0
FULL_TEXT=0
FILEPATH=0
# Loop through the files and open them. 
for(this_folder in 1:length(list_of_folders)){
  
  filepath2 <- paste(filepath,"//",list_of_folders[this_folder],sep="")
  list_of_xml_files <- list.files(filepath2) # list of xml files in the folder in the shared space.
  
  for(this_xml_file in 1:length(list_of_xml_files)){
    error_catch <- 0 # declare exists and is numeric
    
    filepath3 <- paste(filepath2,"//",list_of_xml_files[this_xml_file],sep="")
    FILEPATH <- append(FILEPATH,filepath3)
    #data <- xmlParse(filepath3) # to do; put in a try catch for cases where there is an empty file. What does an empty file mean? Ask Sara 
    
    error_catch <- try(xmlParse(filepath3),silent = TRUE)
    if(is(error_catch)[1]=="XMLInternalDocument"){ # if it is not xml or does not exist, move to the error_catch else. 
    data <- xmlParse(filepath3)
    xml_data <- xmlToList(data)
    
    iati_id <- try(xml_data$`iati-activity`$`iati-identifier`)
    if(is(iati_id)=="try-error"){IATI_ID <- append(IATI_ID,"Error 1")}
    else{
      IATI_ID <- append(IATI_ID,xml_data$`iati-activity`$`iati-identifier`) 
    }
    
    description <- try(xml_data$`iati-activity`$description)
    if(is(description)=="try-error"){DESCRIPTION <- append(DESCRIPTION,"Error 2") }
    else{
      DESCRIPTION <- append(DESCRIPTION,paste(unlist(xml_data$`iati-activity`$description),collapse=" ")) 
    }
    
    full_text <- try(paste(xml_data,collapse=" "))
    if(is(description)=="try-error"){FULL_TEXT <- append(FULL_TEXT,"Error 3") }
    else{
      FULL_TEXT <- append(FULL_TEXT,paste(xml_data,collapse=" ")) 
    }
    

    }else{ # else statement of the error_catch try() above. 
    
    IATI_ID <- append(IATI_ID,paste("file empty, ",filepath3)) # to test; some of the files are not empty, eg C://Users//k-carolan//DFID//EXTERNAL - ONS-DFID Data Science Hub - iatikitcache//registry//data//3ie//3ie-dpw.xml  see Results[9,]
    DESCRIPTION <- append(DESCRIPTION,"file empty")
    FULL_TEXT <- append(FULL_TEXT,"file empty") 
    }
    
} # Close the this_xml_file loop
print(paste("folder",this_folder,"of",length(list_of_folders),"done"))  
} # Close the this_folder loop

#remove the "0" from the original declare, cbind and store the output. 
Results <- cbind(IATI_ID,DESCRIPTION,FULL_TEXT,FILEPATH)

length(unlist(Results[,1])) # 282 folders contained 1182 IDs. Need to figure out the variation in the data structures. 
  
### There are too many files to store in memory, it becomes too big to have open as a project at once. 
# try opening and closing a csv instead > Next R code. 

# dont do CSV do .RData 