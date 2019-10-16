#Author: Saliha Minhas, First Version Date: 29th September 2019

#Summary, this program reads in raw IATI data to df 
#and then takes sections of it by column and writes to CSV files


##read in all records to df
dfall <- as.data.frame(all_downloaded_records)


#all report org columns
dfreport <- data.frame(dfall$iati.identifier, dfall$reporting.org,
                       dfall$reporting.org.ref, dfall$reporting.org.type,
                       dfall$reporting.org.type.code) 

write.csv(dfreport,"C:/corpus3/dfreport.csv", row.names = FALSE)


# main data 
dfmain <-data.frame(dfall$iati.identifier, dfall$title, dfall$description)
write.csv(dfmain,"C:/corpus3/dfmain.csv", row.names = FALSE)



#all participating org columns
dfpart <- data.frame (dfall$iati.identifier, dfall$participating.org..Accountable., dfall$participating.org.ref..Accountable., dfall$participating.org.type..Accountable.,
                      dfall$participating.org..Funding., dfall$participating.org.ref..Funding.,
                      dfall$participating.org.type..Funding., dfall$participating.org.type.code..Funding.)

write.csv(dfpart,"C:/corpus3/dfpart.csv", row.names = FALSE)


dfsector <- data.frame (dfall$iati.identifier, dfall$sector,
                        dfall$sector.code, dfall$sector.percentage,
                        dfall$sector.vocabulary, dfall$sector.vocabulary.code)

#sector columns
write.csv(dfsector,"C:/corpus3/dfsector.csv", row.names = FALSE)

#country columns
dfcountry <- data.frame (dfall$iati.identifier, dfall$recipient.country.code,
                         dfall$recipient.country)

write.csv(dfcountry,"C:/corpus3/dfcountry.csv", row.names = FALSE)


























                      