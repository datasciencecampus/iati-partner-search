library(xml2)

root_folder <- "C:/data/iati_data/data"

files <- list.files(path=root_folder, pattern="*.xml", full.names=TRUE, recursive=TRUE)

get_from_xml<- function (xmlfile){
  tryCatch({
    fcontents <- read_xml(xmlfile)
    extract_xml <- lapply(xml_children(fcontents), function(inputxml) {
      id <- xml_text(xml_find_first(inputxml, './/iati-identifier'))
      desc <- paste(xml_text(xml_find_all(inputxml, './/description')), collapse=' ')
      data.frame(id, desc, stringsAsFactors = FALSE)
    })
    return (do.call(rbind, extract_xml))
  },
  error=function(error_message){
    #message(xmlfile)
    #message(error_message)
    return (NULL)}
  )
}

results_df<- data.frame(iati_identifier=character(), description=character(), file = character())

errors_df<- data.frame(errors=character())

for (this_file in 1:length(files)){
    f <- files[this_file]
  
    out_df <- get_from_xml(f)
  
    out_df<- na.omit(out_df)
  
    if (!is.null(out_df)) { if (nrow(out_df) > 0){
    out_df$file <- basename(f)
    results_df<- rbind(results_df, out_df)
  }}
  else {
    error_f <- data.frame(xml_file=f)
    errors_df<- rbind(errors_df, error_f)}

  if(object.size(results_df)>100000){ # if larger than 100 kb, save the .csv and reset the results_df and errors_df objects. I assume errors_df will always be smaller than results_df.  
    
    results_file <- paste0("C:\\data\\results",this_file,".csv")
    errors_file <-  paste0("C:\\data\\errors",this_file,".csv")
    
    write.csv(results_df, results_file, row.names=FALSE)
    write.csv(errors_df, errors_file, row.names=FALSE)
    
    results_df<- data.frame(iati_identifier=character(), description=character())
    errors_df<- data.frame(errors=character())
  } # close the if object size statement 

  } # close the this_file loop

results_file <- paste0("C:\\data\\results",this_file,".csv")
errors_file <-  paste0("C:\\data\\errors",this_file,".csv")

write.csv(results_df, results_file, row.names=FALSE, fileEncoding = 'UTF-8')
write.csv(errors_df, errors_file, row.names=FALSE, fileEncoding = 'UTF-8')


#Get all result csvs, append and write out
csvs <- list.files(path='C:/data', pattern="results.*\\.csv", full.names=TRUE)

append_df <- do.call(rbind, lapply(csvs, FUN = function(file) {
  read.csv(file, stringsAsFactors = FALSE)
}))

colnames(append_df) <- c('iati_identifier', 'description', 'file')

write.csv(append_df, "C:\\data\\iati_full_desc.csv", fileEncoding='UTF-8', row.names=FALSE)
