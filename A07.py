import pandas as pd
from math import log2
from collections import defaultdict

# ----------------------------
# 1. Read FASTA File
# ----------------------------
def read_fasta(filename):
    sequences = {}
    header = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                header = line[1:]  # Remove '>'
                sequences[header] = ''
            else:
                sequences[header] += line.upper()
    return sequences

# ----------------------------
# 2. Estimate Single Probabilities p_a
# ----------------------------
def estimate_single_probabilities(sequences):
    total = 0
    counts = defaultdict(int)
    for seq in sequences.values():
        for aa in seq:
            if aa != '-':  # Ignore gaps
                counts[aa] += 1
                total += 1
    probs = {aa: count / total for aa, count in counts.items()}
    return probs

# ----------------------------
# 3. Estimate Joint Probabilities p_ab
# ----------------------------
def estimate_joint_probabilities(sequences):
    headers = list(sequences.keys())
    n = len(headers)
    length = len(next(iter(sequences.values())))

    counts = defaultdict(int)
    total_pairs = 0

    for pos in range(length):
        column = [sequences[hdr][pos] for hdr in headers]
        for i in range(n):
            for j in range(i+1, n):
                a, b = column[i], column[j]
                if a != '-' and b != '-':
                    pair = tuple(sorted((a, b)))
                    counts[pair] += 1
                    total_pairs += 1

    probs = {pair: count / total_pairs for pair, count in counts.items()}
    return probs

# ----------------------------
# 4. Compute Substitution Matrix
# ----------------------------
def compute_substitution_matrix(p_single, p_joint):
    aa_set = sorted(p_single.keys())
    subst_matrix = {}

    for a in aa_set:
        for b in aa_set:
            pair = tuple(sorted((a, b)))
            if pair in p_joint:
                p_ab = p_joint[pair]
                s = log2(p_ab / (p_single[a] * p_single[b]))
                subst_matrix[(a, b)] = s
            else:
                subst_matrix[(a, b)] = float('-inf')  # or None if preferred
    return subst_matrix, aa_set

# ----------------------------
# 5. Convert to DataFrame and Save
# ----------------------------
def matrix_to_csv(subst_matrix, aa_list, filename='substitution_matrix.csv'):
    df = pd.DataFrame(index=aa_list, columns=aa_list)
    for a in aa_list:
        for b in aa_list:
            pair = tuple(sorted((a, b)))
            score = subst_matrix[pair]
            df.loc[a, b] = score
            df.loc[b, a] = score  # Symmetric
    df.to_csv(filename)
    return df

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    fasta_file = "msa-scoring-matrix.fasta"  # Replace with your filename
    sequences = read_fasta(fasta_file)

    p_single = estimate_single_probabilities(sequences)
    p_joint = estimate_joint_probabilities(sequences)
    subst_matrix, aa_list = compute_substitution_matrix(p_single, p_joint)
    df = matrix_to_csv(subst_matrix, aa_list)
    print("Substitution matrix saved to 'substitution_matrix.csv'")
