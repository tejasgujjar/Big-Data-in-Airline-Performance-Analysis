library(RSentiment)
library(twitteR)
library(stringr)

#get following details from apps.twitter.com
API_Key='lCMb5ZG30JuswZFSWWw4bmPlL'
API_Secret='IrO9yEJR5OgY8vhIUdSfh455hBNsO5sS2rmFYgDeUja7v1cq1E'
Access_Token='363638093-2EtBiQOcIpKYmoYRN4XOjxQyWBmTfLU8D8x21xuL'
Access_Token_Secret='9MrpFRvKYyVZQRLKCHG4GIeMoYyJfT2h78htGwUEr9XOz'
setup_twitter_oauth(API_Key,API_Secret,Access_Token,Access_Token_Secret)

##searching for 50 recent tweets
got<-searchTwitter("jetblue",n=800,lang = 'en',resultType = "recent")

##format tweets
got1 <- sapply(got, function(x) x$getText())
got2 <- gsub("[\r\n]", "", got1)
got3 <- str_replace_all(got2, "[[:punct:]]", "")

##write csv
data <- calculate_sentiment(got3[1:600])
write.csv(data, file = "jetblue.csv")
