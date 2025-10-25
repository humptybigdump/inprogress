import pandas as pd

# read in csv file as pandas dataframe
df = pd.read_csv('files/customers.csv')

# show first lines  of dataframe, you can hand over the number 
# of lines to the function .head() as a argument in the brackets
print('df.head()')
print('---------')
print(df.head())
print()

# information on column names, non-na values per coluimn and datatype
print('df.info()')
print('---------')
print(df.info())
print()

# summary statistics of numerical columns
print('df.describe()')
print('-------------')
print(df.describe())
print()

# extract column names of dataframe
print('df.columns')
print('----------')
print(df.columns)
print()

# filter dataframe
print("Filter dataframe by 'Country' == 'Chile'")
print('----------------------------------------')
print(df[df['Country'] == 'Chile'])
print()

print("Filter dataframe by 'Subscription Data' > '2021-01-21")
print('-----------------------------------------------------')
print(df[df['Subscription Date'] > '2021-01-21'])

# save dataframe as csv file
df.to_csv('new_csv.csv', index=False)