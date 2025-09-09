rm(list = ls()) # clean environment
cat("\014") # clean console

#####################################
## IMPORTING DATA
library(data.table)
data <- fread("https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv")


#####################################
# DATA FRAMES

#Creating a Data Frame
AnnaBenInfo <- data.frame(
  "Name" = c("Anna", "Ben"),
  "Age" = c(20, 21),
  "ExamResult" = c(82, 90),
  stringsAsFactors = FALSE
)

# Inspecting a Data Frame
class(AnnaBenInfo)

str(AnnaBenInfo)

ncol(AnnaBenInfo)

nrow(AnnaBenInfo)

dim(AnnaBenInfo)

# ACCESSING AND MODIFYING DATA FRAME ELEMENTS
# By name
AnnaBenInfo$Name

AnnaBenInfo[["Name"]]

AnnaBenInfo["Name"]

# By position
AnnaBenInfo[1, ]

AnnaBenInfo[ , 3]

AnnaBenInfo[2, 3]

# Filter rows using conditions
AnnaBenInfo[AnnaBenInfo$ExamResult > 85, ]

# Modify an element
AnnaBenInfo[2, "Age"] <- 23
AnnaBenInfo

# ADDING ROWS AND COLUMNS
# Adding a row
AnnaBenInfo <- rbind(AnnaBenInfo, list("Kate", 19, 85))

# Adding a column
cbind(AnnaBenInfo, Country=c("US","UK", "DE"))

# DELETING ROWS AND COLUMNS
# Remove a column
AnnaBenInfo$ExamResult <- NULL
AnnaBenInfo

# Remove a row
AnnaBenInfo[-2,]



#####################################
# WORKING WITH DIAMONDS10
rm(list = ls()) # clean environment
cat("\014") # clean console

#install.packages("ggplot2")
library(ggplot2)
?diamonds
Diamonds10 <- diamonds[1:10,]
str(Diamonds10)
print(Diamonds10)

Diamonds10$CitySold <- c("NY", "NY", "LA", "LV", "NY", "NY", "LV", "SF", "LA", "SF")
Diamonds10$DaysInStore <- c(5, 100, 3, 15, 93, 65, 22, 46, 43, 12)

Diamonds10$Type <- c(1, 3, 2, 2, 1, 2, 3, 3, 3, 3)
Diamonds10$Type <- factor(Diamonds10$Type, levels = c(1:3), labels = c("earring", "necklace", "ring"))

Diamonds10$DateSold <- as.Date(rep(c("2016-12-01", "2016-06-15"), 5))
Diamonds10$DiamondReturned <- c(TRUE, FALSE, FALSE, TRUE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE)
str(Diamonds10)


#####################################
# DATA CLEANING
rm(list = ls()) # clean environment
cat("\014") # clean console

library(dplyr)
?starwars

## SELECTING VARIABLES
# keep the variables name, height, and gender
newdata <- select(starwars, name, height, gender)

# keep the variable name and all variables between mass and species inclusive
newdata <- select(starwars, name, mass:species)

# keep all variables except birth_year and gender
newdata <- select(starwars, -birth_year, -gender)


## SELECTING OBSERVATIONS
# select females
newdata <- filter(starwars, sex == "female")

# select females with brown hair
newdata <- filter(starwars, sex == "female" & hair_color == "brown")


# select individuals that are from Alderaan or Endor
newdata <- filter(starwars, homeworld == "Alderaan" | homeworld == "Endor")

# this can be written more succinctly as
newdata <- filter(starwars, 
                  homeworld %in% 
                    c("Alderaan", "Endor"))

# convert height in centimeters to inches and mass in kilograms to pounds
newdata <- mutate(starwars, 
                  height_in = height * 0.394,
                  mass_p   = mass   * 2.205)

# if height is greater than 180 then heightcat = "tall", 
# otherwise heightcat = "short"
newdata <- mutate(starwars, 
                  heightcat = ifelse(height > 180, 
                                     "tall", 
                                     "short"))

# convert any eye color that is not black, blue or brown, to other.
newdata <- mutate(starwars, 
                  eye_color = ifelse(eye_color %in% 
                                       c("black", "blue", "brown"),
                                     eye_color,
                                     "other"))

# set heights greater than 200 or less than 75 to missing
newdata <- mutate(starwars, 
                  height = ifelse(height < 75 | height > 200,
                                  NA,
                                  height))

# calculate mean height and mass
newdata <- summarize(starwars, 
                     mean_ht = mean(height, na.rm=TRUE), 
                     mean_mass = mean(mass, na.rm=TRUE))
newdata

# calculate mean height and weight by gender
newdata <- group_by(starwars, gender)
newdata <- summarize(newdata, 
                     mean_ht = mean(height, na.rm=TRUE), 
                     mean_wt = mean(mass, na.rm=TRUE))
newdata


## USING PIPES
# calculate the mean height for females by species
newdata <- filter(starwars, 
                  sex == "female")
newdata <- group_by(newdata, species)
newdata <- summarize(newdata, 
                     mean_ht = mean(height, na.rm = TRUE))
newdata

# this can be written more concisely as
newdata <- starwars %>%
  filter(sex == "female") %>%
  group_by(species) %>%
  summarize(mean_ht = mean(height, na.rm = TRUE))
newdata


###################################
## PROCESSING DATES
rm(list = ls()) # clean environment
cat("\014") # clean console

df <- data.frame(
  dob = c("06/07/1952", "Dec-13-89", "2:26:2003")
  )
# view structure of data frame
str(df) 


# Processing data with lubridate
library(lubridate)
# Convert dob from character to date
df$dob <- mdy(df$dob)
str(df)

# Extract year/month/day of birth
df$birth_year <- year(df$dob)
df$birth_month <- month(df$dob)
df$birth_day <- day(df$dob)
# Calculate age in years
df$age <- time_length(interval(df$dob, today()), unit = "days")
df


#######################################
## RESHAPING DATA
rm(list = ls()) # clean environment
cat("\014") # clean console

# Create wide data
df <- data.frame(
  id = c("01", "02", "03"),
  name = c("Bill", "Bob", "Mary"),
  sex = c("Male", "Male", "Female"),
  height = c(70, 72, 62),
  weight = c(180, 195, 130)
)

# Reshape to long format
library(tidyr)
df_long <- pivot_longer(df, cols = c(height, weight), 
                        names_to = "variable", values_to = "value")


########################################
## MISSING VALUES
rm(list = ls()) # clean environment
cat("\014") # clean console

# Feature Selection

# load mammal sleep data
data(msleep, package="ggplot2")
?msleep

# What is the proportion of missing data for each variable?
pctmiss <- colSums(is.na(msleep))/nrow(msleep)
round(pctmiss, 2)

# Delete variable sleep_cycle
msleep <- select(msleep, -sleep_cycle)


# Create a dataset containing genus, vore, and conservation.
newdata <- select(msleep, name, genus, vore, conservation)
# Delete any rows containing missing data.
newdata <- na.omit(newdata)


# Impute missing values using the 5 nearest neighbors
library(VIM) # installed!?
newdata <- kNN(msleep, k=5)

# Check again proportion of missing data
pctmiss <- colSums(is.na(newdata))/nrow(newdata)
round(pctmiss, 2)







