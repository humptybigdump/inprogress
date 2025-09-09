rm(list = ls()) # clean environment
cat("\014") # clean console

################################
library(tidyverse)
library(wbstats)

wb_data_cs <- wb_data(c("SP.DYN.LE00.IN", "NY.GDP.PCAP.CD"), start_date = 2023, end_date = 2023) %>%
  rename(life_exp = SP.DYN.LE00.IN,
         gdppc = NY.GDP.PCAP.CD
  ) %>%
  filter(!is.na(life_exp), !is.na(gdppc))

# Create a simple plot
ggplot(wb_data_cs, aes(x=gdppc, y=life_exp)) + geom_point()




################################
library(tidyverse)
library(wbstats)

# Define countries and years
countries <- c("DE", "FR", "US", "CN", "IN")
start_year <- 2000
end_year <- 2023

# Download Life expectancy
wb_data_pd <- wb_data(indicator = "SP.DYN.LE00.IN",
                   country = countries,
                   start_date = start_year, end_date = end_year)

# Create plot
ggplot(wb_data_pd, aes(x = date, y = SP.DYN.LE00.IN, color = country)) +
  geom_line(linewidth = 1) +    # First geometric layer: line
  geom_point(size = 2) +   # Second geometric layer: points
  labs(title = "Life Expectancy at Birth (2000–2023)",
       x = "Year", y = "Life expectancy (years)",
       color = "Country") +
  theme_classic()



####################################
# Line chart

# Filter to Germany only
wb_data_germany <- wb_data_pd %>% filter(country == "Germany")

# Create plot
ggplot(wb_data_germany, aes(x = date, y = SP.DYN.LE00.IN)) +
  geom_line(color="blue", linewidth = 1) +    # Line
  labs(title = "Life Expectancy at Birth in Germany (2000–2023)",
       x = "Year", y = "Life expectancy (years)") +
  theme_classic()

####################################
# Bar chart
# Prepare data: filter for 2023
wb_data_bar <- wb_data_pd %>%
  filter(date == 2023)

# Create bar chart
ggplot(wb_data_bar, aes(x = country, y = SP.DYN.LE00.IN, fill = country)) +
  geom_bar(stat = "identity") +
  labs(title = "Life Expectancy at Birth (2023)",
       x = "Country", 
       y = "Life expectancy (years)") +
  theme_classic() +
  theme(legend.position = "none")  # no legend

####################################
# Histogram

ggplot(wb_data_cs, aes(x = life_exp)) +
  geom_histogram(binwidth = 1, fill = "skyblue", color = "black") +
  labs(title = "Life Expectancy (2023)",
       x = "Life expectancy (years)",
       y = "Count") +
  theme_classic()

####################################
# Density Plot

ggplot(wb_data_cs, aes(x = life_exp)) +
  geom_density(fill = "skyblue", alpha = 0.6, bw = 1) +
  labs(title = "Life Expectancy (2023)",
       x = "Life expectancy (years)",
       y = "Density") +
  theme_classic()



####################################
# Boxplot
ggplot(wb_data_cs, aes(y = gdppc)) +
  geom_boxplot(fill = "skyblue", alpha = 0.6) +
  labs(title = "GDP per Capita (2023)",
       y = "GDP per capita (US$)") +
  theme_classic()


####################################
# Violin plot
ggplot(wb_data_cs, aes(x = "", y = gdppc)) +
  geom_violin(fill = "skyblue", 
              alpha = 0.6) +
  geom_boxplot(width = 0.1, fill = "white", outlier.color = "red") +
  labs(title = "GDP per Capita (2023)",
       x = "",
       y = "GDP per capita (US$)") +
  theme_classic()


####################################
# Maps

library(tidyverse)
library(wbstats)

# Download Life Expectancy for all countries in 2023
wb_data_map <- wb_data(c("SP.DYN.LE00.IN"), country = "all", start_date = 2023, end_date = 2023) %>%
  rename(life_exp = SP.DYN.LE00.IN) %>%
  filter(!is.na(life_exp))

# Get world map (with country shapes)
library(rnaturalearth)
library(rnaturalearthdata)
library(sf)

world <- ne_countries(scale = "medium", returnclass = "sf")

# Prepare for join
world_life_exp <- world %>%
  left_join(wb_data_map, by = c("iso_a3" = "iso3c"))


# Choropleth Map
ggplot(world_life_exp) +
  geom_sf(aes(fill = life_exp), color = "white") +
  scale_fill_viridis_c(option = "plasma",
                       na.value = "gray90") +
  labs(title = "Life Expectancy at Birth (2023)",
       fill = "Life Expectancy (years)") +
  theme_classic()


####################################
# Point map

# Load libraries
library(tidyverse)
library(rnaturalearth)
library(rnaturalearthdata)

# World and cities data
world <- ne_countries(scale = "medium", returnclass = "sf")
cities <- ne_download(scale = "medium", type = "populated_places", returnclass = "sf")

# Filter Europe countries and capitals
europe_countries <- world %>% filter(continent == "Europe") %>% pull(name)

world_europe <- world %>% filter(name %in% europe_countries)

capitals_europe <- cities %>%
  filter(FEATURECLA %in% c("Admin-0 capital", "Admin-0 capital alt"),
         ADM0NAME %in% europe_countries)

# Plot the point map
ggplot() +
  geom_sf(data = world_europe, fill = "gray90", color = "white") +
  geom_sf(data = capitals_europe, color = "blue", size = 2) +
  coord_sf(xlim = c(-25, 45), ylim = c(34, 72), expand = FALSE) +
  labs(title = "National Capitals of Europe") +
  theme_classic()


####################################
# Bubble map: Capitals of Europe by population
ggplot() +
  geom_sf(data = world_europe, fill = "gray90", color = "white") +
  geom_sf(data = capitals_europe, aes(size = POP_MAX), color = "darkgreen", alpha = 0.6) +
  coord_sf(xlim = c(-25, 45), ylim = c(34, 72), expand = FALSE) +
  labs(title = "European Capitals by Population",
       size = "Population") +
  theme_classic()






############################
# Map of German federal states and selected cities
# Load libraries
library(tidyverse)
library(sf)
library(rnaturalearth)
library(rnaturalearthdata)
library(geodata)  # to download GADM data easily

# Polygon of Germany
germany <- ne_countries(scale = "medium", country = "Germany", returnclass = "sf")

# Bundesländer (admin level 1)
states_germany_raw <- geodata::gadm(country = "DE", level = 1, path = tempdir())

# Convert to sf object
states_germany <- sf::st_as_sf(states_germany_raw)

# Cities in Germany
cities <- ne_download(scale = "medium", type = "populated_places", returnclass = "sf")

cities_germany <- cities %>%
  filter(ADM0NAME == "Germany") %>%
  arrange(desc(POP_MAX)) %>%
  slice(1:10)  # 3 largest cities

# Plot: Germany polygon + Bundesländer boundaries + cities
ggplot() +
  geom_sf(data = germany, fill = "gray90", color = "black", size = 0.8) +
  geom_sf(data = states_germany, fill = NA, color = "gray", size = 0.5) +
  geom_sf(data = cities_germany, color = "red", size = 3) +
  theme_classic()


