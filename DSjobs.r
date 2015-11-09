df<-read.csv("DSJobsUKTools.csv",stringsAsFactors=FALSE)
colnames(df)=c("Skill","Percentage")

library(ggplot2)

skillPlotDS<-ggplot(data=df,aes(Skill,Percentage,order=Percentage))+
  geom_bar(stat="identity")+
skillPlotDS
