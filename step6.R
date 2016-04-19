setwd("/Users/cyprien/Desktop/Stanford/MS&E231/hw2")

#take the output of step5 as the input data in the "taxi" dataframe
taxi <- read.table("stats.csv",sep=',',fill = TRUE,header=TRUE)

#data manipulation prior to do the join because the format of the keys for the join are not the same
taxi$hour2 <- ifelse(nchar(paste(taxi$hour, "00", sep=":"))<5,paste("0",paste(taxi$hour, "00", sep=":"),sep=""),paste(taxi$hour, "00", sep=":")) 

precip <-read.table("nyc_precipitation.csv",sep=',',fill = TRUE,header=TRUE)
precip<- precip[,(names(precip) %in% c("DATE","HPCP"))]

taxi$date2 <- gsub('-','',taxi$date)
taxi$datehour <- do.call(paste, c(taxi[c("date2","hour2")], sep = " "))
taxi<- taxi[,!(names(taxi) %in% c("date2"))]

#Left join
result<-merge(taxi, precip, by.x="datehour", by.y="DATE",all.x=TRUE)

colnames(result)[ncol(result)] <- "precip"

#select the right columns to ouput
result <- result[c("date", "hour", "precip", "drivers_onduty", "drivers_occupied", "t_onduty", "t_occupied", "n_pass", "n_trip", "n_mile", "earnings")]

#write the result of the join in a tsv file
write.table(result, file = "resultR.tsv",row.names=FALSE, na="NA", quote=FALSE,col.names=TRUE, sep="\t")
