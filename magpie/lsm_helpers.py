import random

DNA_BASES = ('A', 'T', 'G', 'C')
DNA_COMPLEMENTS = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
RNA_BASES = ('A', 'U', 'G', 'C')
RNA_COMPLEMENTS = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}

def get_random_dsDNA(length):
    seq = get_random_ssDNA(length)
    return (seq, get_complementary_ssDNA(seq))

def get_random_dsRNA(length):
    seq = get_random_ssRNA(length)
    return (seq, get_complementary_ssRNA(seq))

def get_complementary_ssDNA(dna_seq):
    return tuple(DNA_COMPLEMENTS[base] for base in dna_seq)

def get_complementary_ssRNA(rna_seq):
    return tuple(RNA_COMPLEMENTS[base] for base in rna_seq)

def get_random_ssDNA(length):
    seq = get_random_seq(length)
    return tuple(DNA_BASES[base] for base in seq)

def get_random_ssRNA(length):
    seq = get_random_seq(length)
    return tuple(RNA_BASES[base] for base in seq)

def get_random_seq(length):
    return tuple(random.randint(0, 3) for _ in range(length))
