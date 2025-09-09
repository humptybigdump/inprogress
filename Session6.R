rm(list = ls()) # clean environment
cat("\014") # clean console

##############################
# SQL

library(DBI)

con <- dbConnect(
  RMariaDB::MariaDB(),
  host = "relational.fel.cvut.cz",
  port = 3306,
  username = "guest",
  password = "ctu-relational",
  dbname = "sakila"
)

dbListTables(con)

query <- "SELECT f.title, 
COUNT(*) AS rental_count
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY f.title
ORDER BY rental_count DESC
LIMIT 3; "

df <- dbGetQuery(con, query)


print(df)

dbDisconnect(con)



##############################
# API
##############################
rm(list = ls()) # clean environment
cat("\014") # clean console


library(httr)
library(dplyr)

# Access the key
source("OMDb_API_Key.R")

# Send request
response <- GET("http://www.omdbapi.com/?",
                query = list(apikey = omdb_key,
                             s = "despicable me",
                             type = "movie",
                             page = 1)) %>% content()

# Print titles of movies

# length(response[["Search"]])
for (i in 1:4) {
  print(response[["Search"]][[i]][["Title"]])
}




##############################
# Web Scraping
##############################

rm(list = ls()) # clean environment
cat("\014") # clean console

library(rvest)
html <- read_html("https://www.tagesschau.de/inland/regional/badenwuerttemberg")
article_titles <- html %>%
  html_nodes(css = ".teaser__headline") %>%
  html_text()
head(article_titles, 5)



##############################
# Programmatic Access
##############################
rm(list = ls()) # clean environment
cat("\014") # clean console


library(rdwd)

# select a dataset (e.g. recent daily climate data from Metzingen)
link <- selectDWD("Metzingen", res="daily", var="kl", per="recent")

# Download that dataset
file <- dataDWD(link, read=FALSE)

# Read the file from the zip folder
clim <- readDWD(file, varnames=TRUE) # can happen directly in dataDWD

# Inspect the data.frame
str(clim)
# Quick time series graphic of temperature
plotDWD(clim, "TMK.Lufttemperatur")


unlink("/cloud/lib/x86_64-pc-linux-gnu-library/4.4/00LOCK-rdwd", recursive = TRUE)
install.packages("rdwd")

