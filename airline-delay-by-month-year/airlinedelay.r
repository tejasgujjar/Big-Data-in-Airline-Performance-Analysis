library(ggplot2)

airline <- read.table("airline.csv", header=T, fill=T, sep=",")
ggplot(airline,aes(x=airline$year,y=airline$arr_delay, color=3)) + geom_point() + geom_smooth(color="grey")
ggplot(airline,aes(x=airline$month,y=airline$arr_delay, color=3)) + geom_point() + geom_smooth(color="grey")
