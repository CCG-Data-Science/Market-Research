## Ways to webscrape

## http://scholar.google.com/citations?user=HI-I6C0AAAAJ&hl=en
library(RCurl)
#library(RTidyHTML)
library(XML)

urls<-unlist(read.csv('JobURLS.txt',stringsAsFactors=FALSE))
url <- "https://careers.peopleclick.eu.com/careerscp/client_qinetiq/qinetiqexternal/gateway.do?functionName=viewFromLink&jobPostId=15632&localeCode=en-us&source=Indeed.com&sourceType=PREMIUM_POST_SITE"

for (i in 1:length(urls)){

url<-urls[i]
print(i)
doc.raw <- getURL(url)
#doc <- tidyHTML(doc.raw)
html <- htmlTreeParse(doc.raw, useInternal = TRUE)
txt <- xpathApply(html, "//body//text()[not(ancestor::script)][not(ancestor::style)][not(ancestor::noscript)]", xmlValue)
txt<-unlist(txt)
}
#print(txt)


library(tm)
corpus = Corpus(VectorSource(txt))
# Pre-process data
corpus = tm_map(corpus, tolower)
# IMPORTANT NOTE: If you are using the latest version of the tm package, you will need to run the following line before continuing (it converts corpus to a Plain Text Document). This is a recent change having to do with the tolower function that occurred after this video was recorded.
corpus = tm_map(corpus, PlainTextDocument)
corpus = tm_map(corpus, removePunctuation)
corpus = tm_map(corpus, removeWords, stopwords("english"))
corpus = tm_map(corpus, stemDocument)
length(stopwords("english"))
#create a matrix
dtm = DocumentTermMatrix(corpus)
dtm
ncol(dtm)

#2.2 Remove sparse terms
spdtm= removeSparseTerms(dtm, .99)
ncol(spdtm)

# 2.3 Create data frame
txtSparse = as.data.frame(as.matrix(spdtm))
names(txtSparse)<-make.names(names(txtSparse))

# which word occurs most frequently
library(dplyr)
sums<-as.numeric(colSums(txtSparse))
names<-names(txtSparse)
Absums<-data.frame(names,sums)
arrange(Absums,-sums)[1:50,]

# achieves the same in one line of code!
which.max(colSums(txtSparse))