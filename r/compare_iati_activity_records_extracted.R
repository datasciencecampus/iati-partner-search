library(tidyverse)

api_records<-read.csv('C:/repos/iati-partner-search/data/all_downloaded_records.csv', stringsAsFactors=FALSE)
api_records <- api_records %>% select(iati.identifier, description)

xml_records<- read.csv('C:/data/iati_full_desc.csv', stringsAsFactors = FALSE)
xml_records<- xml_records %>% select(iati_identifier, description)
#There are a few duplicates
xml_records <- distinct(xml_records)

count_distinct_ids_api <- api_records %>% select(iati.identifier) %>% n_distinct()
count_distinct_ids_xml <- xml_records %>% select(iati_identifier) %>% n_distinct()

errors_check_distinct <- append_df_distinct %>% inner_join(count_df_distinct, by='iati_identifier') %>% filter(count >1)

xml_not_in_api <- xml_records %>% filter(! iati_identifier %in% api_records$iati.identifier)

api_not_in_xml <- api_records %>% filter(! iati.identifier %in% xml_records$iati_identifier)


#Wildcard search on similar ids
check_api <- api_records %>% filter(str_detect(iati.identifier, 'XM-OCHA'))

check_xml <- xml_records %>% filter(str_detect(iati_identifier, '30001-11SN01'))