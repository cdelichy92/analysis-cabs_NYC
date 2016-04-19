library(reshape2)
library(ggplot2)
library(dplyr)

setwd("/Users/cyprien/Desktop/Stanford/MS&E231/hw2")

# Work environment and data loading
data <- read.table("resultR.tsv",sep='\t',fill = TRUE,header=TRUE)
data <- filter(data, earnings>0)

#here we set a threshold value for the rain/no rain states
data$has_rained <- ifelse(is.na(data$precip) | data$precip<8, 0, 1)
data$has_rained <- factor(data$has_rained)

#group by rain/no rain and hour of the day
data_grouped <- group_by(data, has_rained, hour)

x<-summarise(data_grouped,
          total_earnings=sum(earnings), 
          total_drivers_onduty=sum(drivers_onduty),
          total_drivers_occupied=sum(drivers_occupied),
          total_t_onduty=sum(t_onduty),
          average_wage=total_earnings/total_t_onduty,
          average_precip=mean(precip),
          average_drivers_onduty=mean(drivers_onduty),
          average_drivers_occupied=mean(drivers_occupied),
          average_pass=sum(n_pass)/total_t_onduty,
          average_mile=sum(n_mile)/total_t_onduty,
          average_trip=sum(n_trip)/total_t_onduty)

theme_set(theme_bw())

p1 <- ggplot(x, aes(x=hour,y=average_wage, group = has_rained, colour = has_rained)) + 
  geom_path(alpha = 0.5) + ggtitle("Average wage")+ labs(x = "Hour") + labs(y = "Average wage")
ggsave(plot=p1, file='wage.png', width=20, height=8)

p1

p2 <- ggplot(x, aes(x=hour,y=average_drivers_onduty, group = has_rained, colour = has_rained)) + 
  geom_path(alpha = 0.5) + ggtitle("Average number of drivers on duty per hour")+ labs(x = "Hour") + labs(y = "Average number of drivers on duty")
ggsave(plot=p2, file='drivers-onduty.png', width=20, height=8)

p2

p3 <- ggplot(x, aes(x=hour,y=average_drivers_occupied, group = has_rained, colour = has_rained)) + 
  geom_path(alpha = 0.5) + ggtitle("Average number of drivers occupied per hour")+ labs(x = "Hour") + labs(y = "Average number of drivers occupied")
ggsave(plot=p3, file='drivers-occupied.png', width=20, height=8)

p3

p6 <- ggplot(x, aes(x=hour,y=average_trip, group = has_rained, colour = has_rained)) + 
  geom_path(alpha = 0.5) + ggtitle("Average number of trips")+ labs(x = "Hour") + labs(y = "Average number of trips")
ggsave(plot=p6, file='trip.png', width=20, height=8)

p6

#group by rain/no rain
data_grouped_rain <- group_by(data, has_rained)

y <- summarise(data_grouped_rain,
               total_earnings=sum(earnings),
               total_t_onduty=sum(t_onduty),
               total_t_occupied=sum(t_occupied),
               total_drivers_onduty=sum(drivers_onduty),
               drivers_onduty_h=sum(drivers_onduty)/n(),
               total_drivers_occupied=sum(drivers_occupied),
               average_wage=total_earnings/total_t_onduty,
               average_mile=sum(n_mile)/total_t_onduty,
               average_trip=sum(n_trip)/total_t_onduty,
               ratio=total_t_occupied/total_t_onduty,
               average_t_onduty=mean(drivers_onduty))