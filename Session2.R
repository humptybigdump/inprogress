rm(list = ls()) # clean environment
cat("\014") # clean console

#####################################
## BASIC SYNTAX
Students <- c("Anna", "Ben", "Catherine", "Dennis")


#####################################
## VARIABLE TYPES
MovieNames <- c("Anora", "The Substance", "Emilia Perez", "The Brutalist")
Length <- c(139,141,132,215)
OscarWinner <- c(1, 0, 1, 1)
OscarWinner <- factor(OscarWinner,
                      levels = c(0:1),
                      labels = c("no winner", "winner"))
ReleaseDate <- as.Date(c("2024-10-31", "2024-09-19", "2024-11-28", "2025-01-30"))
MovieSeen <- c(TRUE, TRUE, TRUE, FALSE)


# Converting Data Types
OscarWinner <- factor(c(1, 0, 1))
as.numeric(OscarWinner)
as.numeric(as.character(OscarWinner))


#####################################
## VECTORS
# Vector Properties
MyVector <- c(3, 5, 7, 8, 10)
typeof(MyVector)
class(MyVector)
length(MyVector)

# Assessing Vector Elements
MyVector
MyVector[3]
MyVector[c(1,3)]
MyVector[-1]

#####################################
## BASIC MANIPULATIONS
# Modifying Elements
MyVector[3] <- 0 
MyVector
MyVector[MyVector < 6] <- 1 
MyVector
#Truncating
MyVector <- MyVector[3:5]
MyVector
#Emptying
MyVector <- NULL
MyVector[2]

#Consecutive Numbers
x <- 1:5
x

y <- 3:-3
y

# Sequences 
seq(2, 4, by = 0.25)
seq(2, 10, length.out = 4)

#####################################
## LISTS
# Creating a List
Name <- "Ben"
Male <- TRUE
Age <- 22
ExamResults <- c(80, 90, 76)
InfoBen <- list(Name, Male, Age, ExamResults)
typeof(InfoBen)
length(InfoBen)
str(InfoBen)

# Accessing Elements
InfoBen[c(3:4)]
InfoBen[[4]]

#####################################
# Logical Operators
c(FALSE, TRUE, TRUE) & c(TRUE, FALSE, TRUE)
c(FALSE, TRUE, TRUE) | c(TRUE, FALSE, TRUE)
!c(FALSE, TRUE, TRUE)


#####################################
# FUNCTIONS
args(sum)
?sum

sum(1, 2, NA)
sum(1, 2, NA, na.rm = TRUE)

#####################################
# COMMONLY USED FUNCTIONS I
a <- 4
b <- c(1,NA)
c <- "HI THERE"
d <- "hello"
x <- 2:4
z <- c(1.23, -3.456)
m <- matrix(1:6, nrow = 2)

sum(x)
mean(x)
sd(x)
min(x)
max(x)
signif(z, digits = 2)
round(z, digits = 2)
rowMeans(m)
rowSums(m)

# COMMONLY USED FUNCTIONS II
abs(z)
sqrt(a)
log(a)
exp(a)
seq(4,10,2)
rep(2,5)
is.na(b)
tolower(c)
toupper(d)

# RESERVED WORDS
?reserved
TRUE <- 1
True <- 1

#####################################
# if STATEMENTS
x <- -7
if (x > 0) {
  print("It's a positive number")
}

x <- 2
if (x < 2) {
  print("smaller than two")
} else if (x > 2) {
  print("greater than two")
} else {
  print("two")
}


#####################################
# for LOOPS
# count even numbers in a vector
x <- c(2,5,4,3,9,8,11,6)
count <- 0
for (val in x) {
  if (val %% 2 == 0) {  # modulus
    count <- count + 1
  }
}
print(count)

# assigning values to matrix based on position:
mymat <- matrix(nrow = 7, ncol = 7)
for (i in 1:nrow(mymat)) {
  for (j in 1:ncol(mymat)) {
    mymat[i,j] = i*j
  }}
mymat


#####################################
# WRITING FUNCTIONS
# defining function
myFirstFunction <- function(n) {
  return(n + n)
}
myFirstFunction(10)
b <- c(1, 5, 9)
outcomeB <- myFirstFunction(b)
outcomeB

# defining function with default
funWithDefaultArg <- function(x, y=3) {
  x*y
}
funWithDefaultArg(2,5) # 2*5=10
funWithDefaultArg(2) # 2*3=6


# defining function without return
Fun3 <- function(m) {
  l <- m + m
}
# using function
Fun3(8)

# defining function with return
Fun4 <- function(p) {
  q <- p + p
  return(q)
}
# Using function
Fun4(8)



#####################################
# PACKAGES
install.packages("tidyverse")
library(tidyverse)







