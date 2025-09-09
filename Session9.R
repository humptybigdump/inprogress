rm(list = ls()) # clean environment
cat("\014") # clean console

##################################
# Classification

# Import the required packages
library(psych)
library(tidyverse)
library(tidymodels)
library(kknn)
library(caret)

# Import the data
titanic <- read_csv("data/titanic_clean.csv")

# Summary statistics
stats <- describe(titanic)
desired_stats <- stats[c("mean", "sd", "median",
                         "min", "max")]
print(desired_stats)

# Ensuring replicability
set.seed(1234)

# Change outcome to factor
titanic$Survived <- as.factor(titanic$Survived)
# Randomly draw 80% of the observations
index <- sample(nrow(titanic),
                size = 0.8 * nrow(titanic),
                replace = FALSE)
# Split dataset
train_data <- titanic[index,]
test_data <- titanic[-index,]

# Define the recipe with scaling
rec <- recipe(Survived ~ ., data = train_data) %>%
  step_scale(all_predictors()) %>%
  step_center(all_predictors())

# Define the model
mod <- nearest_neighbor(neighbors = 10) %>%
  set_engine("kknn") %>%
  set_mode("classification")

# Combine both in a workflow
wf <- workflow() %>% add_recipe(rec) %>% add_model(mod)

# Train the model
clf <- wf %>% fit(data = train_data)

# Predict on unseen data
test_predictions <- predict(clf, new_data = test_data)$.pred_class

# Accuracy
caret::confusionMatrix(test_predictions,
                       test_data$Survived)[["overall"]][["Accuracy"]]

caret::confusionMatrix(test_predictions, test_data$Survived)


##################################
rm(list = ls()) # clean environment
cat("\014") # clean console
##################################
# Regression

# Import the required packages
library(psych)
library(tidyverse)
library(tidymodels)

# Import the data
mel <- read_csv("data/Mel_housing_clean.csv")

# Summary statistics
stats <- describe(mel)
desired_stats <- stats[c("mean", "sd", "median", "min", "max")]
print(desired_stats)

# Ensuring replicability
set.seed(1234)

# Remove 1st two character columns
mel <- mel[, -c(1, 2)]

# Randomly draw 80% of the observations
index <- sample(nrow(mel),
                size = 0.8 * nrow(mel),
                replace = FALSE)

# Split dataset
train_data <- mel[index,]
test_data <- mel[-index,]

# 1st way: Using same pipeline as in classification
# Define the recipe
rec <- recipe(Price ~ ., data = train_data)

# Define the model
mod <- linear_reg() %>% set_engine("lm") %>% set_mode("regression")

# Combine both in a workflow
wf <- workflow() %>% add_recipe(rec) %>% add_model(mod)

# Train the model
mod_fit <- wf %>% fit(data = train_data)

# Predict on the test data
predictions <- predict(mod_fit, test_data) %>%  bind_cols(test_data)

# Calculate RMSE and normalized RMSE
rmse_value <- sqrt(mean((predictions$Price - predictions$.pred)^2))
nrmse_percent <- (rmse_value / mean(predictions$Price)) * 100

print(paste("RMSE:", round(rmse_value, 2)))
print(paste("Normalized RMSE (% of mean):", round(nrmse_percent, 2), "%"))


# 2nd way: Using traditional linear regression
# Train the model
lm_model <- lm(Price ~ ., data = train_data)

# Examine model
summary(lm_model)

# Predict on the test data
pred <- predict(lm_model, test_data)

# Plot actual vs. predicted
d <- data.frame(actual = predictions$Price,
                predicted = predictions$.pred)
p <- ggplot(d, aes(x = actual, y = predicted)) +
  geom_point(alpha = 0.5, size = 2.5,
             color = "blue") +
  geom_abline(slope = 1, intercept = 0) +
    theme_minimal() +
  labs(title = "Actual vs. Predicted Prices",
       x = "Actual Prices",
       y = "Predicted Prices")
plot(p)

 ggsave("ActualvsPredicted.pdf", plot = p, width = 12, height = 9, units = "cm")
