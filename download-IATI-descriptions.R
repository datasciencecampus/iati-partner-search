# This code makes an API request to the IATI data. It downloads the data in chunks, then saves them as .RData objects on the computer (which seems to be more efficient than .csv)
# It then loads the .RData objects and stitches them togeather. 
library(RCurl) # edit with http://www.rpubs.com/Mentors_Ubiqum/list_packages
library(XML)

### Note, this code will not work in DFID or via vpn into DFID. It will work on gov wifi. This is due to DFID security protocols. 
## this first section downloads the data. you may beed to change filepath.   

filepath <- "C:/Users/k-carolan/OneDrive - DFID/Documents/IATI API call data 2/"

options("scipen"=100, "digits"=4) # R will want to use 1e+05 for 100000 which messes up the URL below. This fixes that. 

Start_time <- Sys.time()

record_to_start_from <- 0 # 0 is first record. # 10200000 to 10300000 is not working.Server issue on 20.08.2019. Will look for solution.  
# will put in a thing to check which files have been done. 

record_to_run_to <- 1103148 # you can check the total count of records at https://www.oipa.nl/api/activities/?format=json under the "count" field.  

offset_size <- 1 # the rows of data to download at a time. This is the size of the request passed in getURL() and xmlParse() 

for(offset in seq(record_to_start_from,record_to_run_to,offset_size)){
 
  Loop_start_time <- Sys.time()

  location_to_store_downloaded_data <- paste0(filepath,"IATI_download_from_",offset,"_to_",offset+offset_size,".RData")
  
  # XML download. 
  URL_xml <- paste0("http://datastore.iatistandard.org/api/1/access/activity.xml?limit=",offset_size,"&","offset=",offset)
  
  downloaded_records_xml <- xmlParse(URL_xml,useInternalNodes = TRUE,trim=TRUE,replaceEntities=FALSE)
  
  downloaded_records_xml <-  paste(unlist(xmlToList(downloaded_records_xml)),collapse= " ") 
  
  # CSV download 
  # we need the IATI ID etc. 

  URL_csv <- paste0("http://datastore.iatistandard.org/api/1/access/activity.csv?limit=",offset_size,"&","offset=",offset)
  
  downloaded_records_csv <- read.csv(textConnection(getURL(URL_csv)))
   # Arrange the two downloads to sit side by side. 
  recorded_downloads <- cbind(downloaded_records_csv,downloaded_records_xml)
  
  Loop_end_time <- Sys.time()
  
  # Each saved file will be one IATI ID. 
  save(recorded_downloads,file=location_to_store_downloaded_data)
  
  # unimportant, just for tracking. 
  print(paste0("loop run time = ",round(difftime(Loop_end_time, Loop_start_time,units="secs"),2)," sec for loop ",offset,
               " of ",record_to_run_to,", total runtime = " ,round(difftime(Loop_end_time, Start_time,units="mins"),2),
               " min ")
  )
  
} # end the offset loop




## load into one object for analysis. 
record_to_start_from <- 0
record_to_run_to <-1010000 # (this + offset_size) is the final record brought in.  
offset_size <- 10000

options("scipen"=100, "digits"=4) # R will want to use 1e+05 for 100000 which messes up the URL. This fixes that. 

all_downloaded_records <- "first entry is a blank, delete this.(From Kevin at DSH)"

for(offset in seq(record_to_start_from,record_to_run_to,offset_size)){
  
  location_to_load_downloaded_data <- paste0(filepath,"IATI_download_from_",offset,"_to_",offset+offset_size,".RData")
  
  load(file=location_to_load_downloaded_data)
  
  all_downloaded_records <- rbind(all_downloaded_records,downloaded_records)
  print(paste0("finished ",offset," of ",record_to_run_to," (",(offset/record_to_run_to)*100,"%)"
  ))
  
} # end the offset loop

# cut of the decleration for "all_downloaded_records" if it exists. 
if(all_downloaded_records[1,56] == "first entry is a blank, delete this.(From Kevin at DSH)") {
  all_downloaded_records <- all_downloaded_records[2:length(all_downloaded_records[,1]),]
}

# set up this on multiple instances (different run-tos)



