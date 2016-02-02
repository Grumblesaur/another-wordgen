from phonetic import *

p = Phonology("cons.txt", "vowels.txt", "", "cons_freqs.txt", "vowel_freqs.txt")

p.parse_phonemes(1)
p.parse_phonemes(0)
p.parse_frequencies(1)
p.parse_frequencies(0)

print(p.consonants, "\n")
print(p.cons_freqs, "\n")

print(p.vowels, "\n")
print(p.vowl_freqs, "\n")

