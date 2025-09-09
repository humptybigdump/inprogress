rm(list = ls()) # clean environment
cat("\014") # clean console


#####################################
## if STATEMENTS IN R
# if statement
is_raining <- TRUE
if (is_raining) {
  print("Take an umbrella!")
}

# if ... else
temperature <- 18
if (temperature < 20) {
  print("Wear a jacket.")
} else {
  print("No jacket needed.")
}

# Nested if ... else
temperature <- 18
if (temperature < 10) {
  print("Wear a jacket and a
scarf.")
} else if (temperature < 20) {
  print("Wear a jacket.")
} else if (temperature < 30) {
  print("Wear a t-shirt.")
} else {
  print("It's time to go to the simming pool.")
}

#####################################
## LOOPS 
# for loop
fam_members <- c("Alex", "Jamie", "Sam", "Taylor")

for (member in fam_members) {
  print(paste(member,"your coffee is ready!"))
}

# while loop
seconds <- 10
while (seconds > 0){
  print(paste("The party starts in", seconds))
  Sys.sleep(1)
  seconds <- seconds -1
}
print("The party has started!")

#####################################
## FUNCTIONS
calculateTriangleArea <- function(base, height) {
  area <- (base * height) / 2
  return(area)
}
calculateTriangleArea(3,2)


