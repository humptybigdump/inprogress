######################################
# AdvancedBILS tutorial - 17.07.2025 #
# Coding recap                       #
######################################

# Task 1a: Create a script which counts the occurrences of all letters in a string (not case sensitive).

# define a function to encapsulate the counting functionality
def count_occurrences(s):
    # intiialize dictionary to store count values
    occ = {}
    # Loop through each character in the string
    for char in s.upper():
        if char in occ:
            occ[char] += 1
        else:
            occ[char] = 1

    return occ

# run code on string s
s = 'sfSFgsefeWRgefvVfhwerthbdgsefvGRH'
occurrences = count_occurrences(s)
print(f'Occurrence count in {s}:\n{occurrences}')


# Task 1b: now consider the input to be a DNA sequence. Compute the GC content of this sequence
seq = 'ATGCGTACTGCATTCGGC'
occ_dna = count_occurrences(seq)

# compute GC content: (#G + #C) / sequence length
gc_content = (occ_dna['G'] + occ_dna['C']) / len(seq)

print(f'GC content of {seq}: {gc_content}')


print('\n\n')

######################################

# Task 2: Input: list of gene data, ["gene_number", "expression_level", "length", "name"]
gene_data = [
    ["gene_1", "high", 450, "abef"],
    ["gene_2", "medium", 300, "bcdf"],
    ["gene_3", "low", 150, "cdef"],
    ["gene_4", "high", 500, "defg"],
    ["gene_5", "medium", 350, "efgh"],
    ["gene_6", "low", 200, "fghi"],
]

# TASK (a): Return a list of the gene names sorted descendingly by 
# their expression levels.

# convert list to pandas DataFrame and add column names
import pandas as pd
df = pd.DataFrame(gene_data)
df.columns = ["gene_number", "expression_level", "length", "name"]
print(df)

# map expression levels to numerical values 0 = low, 1 = medium, 2 = high
mapping = {'low': 0,
           'medium': 1,
           'high': 2}
df['expression_level_numerical'] = df['expression_level'].map(mapping)

# sort dataframe
sorted_df = df.sort_values(by='expression_level_numerical', ascending=False)
print(sorted_df)

# extract names as a list
names = list(sorted_df['name'])
print(names)

# TASK (b): Print the average length of all genes.
# compute mean of the length column
print(f'Average gene length: {df['length'].mean()}')


# Task (c): Add a new gene to the list with the following data: 
# ["gene_7", "medium", 400, "ghij"].
# append new entry to list
gene_data.append(["gene_7", "medium", 400, "ghij"])
print(gene_data)