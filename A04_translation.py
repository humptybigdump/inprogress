# to run the script: python A04_translation.py "path to fasta file"
import sys

# read single fasta file
def read_fasta(f):
    with open(f, 'r') as f:
        seq = ''
        for line in f:
            # skip header line
            if not line.startswith('>'):
                seq += line.strip()

    return seq

# transcribe DNA to RNA sequence
def transcribe(dna):
    rna = ''
    for n in dna:
        # replace T by U
        if n == 'T':
            rna += 'U'
        else:
            rna += n

    return rna

# translate RNA sequence to amino acid sequence
def translate(s, dictionary):
    i = 0
    aa_seq = ''
    while i < len(s):
        codon = s[i:i + 3]
        aa_seq += dictionary[codon]
        i += 3

    return aa_seq

# define codon - amino acid dictionary
codons = {'UAA': '*', 'UAG': '*', 'UGA': '*',
'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
'UGU': 'C', 'UGC': 'C',
'GAU': 'D', 'GAC': 'D',
'GAA': 'E', 'GAG': 'E',
'UUU': 'F', 'UUC': 'F',
'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
'CAU': 'H', 'CAC': 'H',
'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
'AAA': 'K', 'AAG': 'K',
'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
'AUG': 'M',
'AAU': 'N', 'AAC': 'N',
'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
'CAA': 'Q', 'CAG': 'Q',
'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'AGU': 'S', 'AGC': 'S',
'ACU': 'U', 'ACC': 'U', 'ACA': 'U', 'ACG': 'U',
'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
'UGG': 'W',
'UAU': 'Y', 'UAC': 'Y'}

# get input file path
input_file = sys.argv[1]

# read fasta file
dna_seq = read_fasta(input_file)
print('DNA sequence:')
print(dna_seq)
print()

# transcribe DNA sequence
rna_seq = transcribe(dna_seq)
print('RNA sequence:')
print(rna_seq)
print()

# translate RNA sequence
aa_seq = translate(rna_seq, codons)
print('Amino acid sequence:')
print(aa_seq)