rm(list = ls()) # clean environment
cat("\014") # clean console

################################
# Load packages
library(datarium)
library(ggplot2)

# Load data
data("marketing")

# Fit OLS model
model <- lm(sales ~ youtube, data = marketing)

print(model)



# Plot the regression line
ggplot(marketing, aes(x = youtube, y = sales)) +
  geom_point(color = "blue", size = 2) +
  geom_abline(intercept = 8.43911, slope = 0.04754, color = "red", linewidth = 1.5) +
  labs(x = "YouTube Advertising Budget",
       y = "Sales") +
  theme_classic(base_size = 14)



# Multiple Regression Model
model_multiple <- lm(sales ~ youtube + facebook + newspaper, data = marketing)
print(model_multiple)

summary(model_multiple)


model_nonlinear <- lm(log(sales) ~ log(youtube) + facebook + newspaper, data = marketing)
summary(model_nonlinear)



##############################################
# Logistic Regression
rm(list = ls()) # clean environment
cat("\014") # clean console

library(titanic)

data("titanic_train")

# Prepare data
df <- titanic_train
df <- na.omit(df[, c("Survived", "Pclass", "Sex", "Age")])  # drop NAs
df$Sex <- factor(df$Sex)
df$Pclass <- factor(df$Pclass)

# Estimate logistic regression model
model_logit <- glm(Survived ~ Pclass + Sex + Age, data = df, family = binomial)
summary(model_logit)







##############################################
# Other figures from the lecture slides

# Scatter plot
p1 <- ggplot(marketing, aes(x = youtube, y = sales)) +
  geom_point(color = "blue", size=1.5) +
  labs(x = "YouTube Advertising Budget",
       y = "Sales") +
  theme_classic(base_size = 12)
#ggsave("Marketing-SalesYoutube-Data.pdf", plot = p1, width = 12, height = 9, units = "cm")
print(p1)



# Add fitted values
model <- lm(sales ~ youtube, data = marketing)

marketing$fitted <- fitted(model)

# Create plot with residual lines
p2 <- ggplot(marketing, aes(x = youtube, y = sales)) +
  geom_segment(aes(xend = youtube, yend = fitted), color = "gray") +
  geom_point(color = "blue", size = 1.5) +
  geom_line(aes(y = fitted), color = "red", linewidth = 1.5) +
  labs(x = "YouTube Advertising Budget",
       y = "Sales") +
  theme_classic(base_size = 12)

print(p2)

#ggsave("Marketing-SalesYoutube-OLS.pdf", plot = p2, width = 12, height = 9, units = "cm")

# Create plot
p3 <- ggplot(marketing, aes(x = youtube, y = sales)) +
  #geom_segment(aes(xend = youtube, yend = fitted), color = "gray") +
  geom_point(color = "blue", size = 1.5) +
  geom_line(aes(y = fitted), color = "red", linewidth = 1.5) +
  labs(x = "YouTube Advertising Budget",
       y = "Sales") +
  theme_classic(base_size = 12)

print(p3)

#ggsave("Marketing-SalesYoutube-OLS2.pdf", plot = p3, width = 12, height = 9, units = "cm")


# Plot the regression line
p4 <- ggplot(marketing, aes(x = youtube, y = sales)) +
  geom_point(color = "blue", size = 2) +
  geom_abline(intercept = 8.43911, slope = 0.04754, color = "red", linewidth = 1.5) +
  labs(x = "YouTube Advertising Budget",
       y = "Sales") +
  theme_classic(base_size = 14)

print(p4)
#ggsave("Marketing-SalesYoutube-OLS3.pdf", plot = p4, width = 12, height = 9, units = "cm")


