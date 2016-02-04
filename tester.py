from phonetic import *

p = Phonology("consonants.txt", "vowels.txt", "cons_freqs.txt",
"vowel_freqs.txt", "onsets.txt", "nuclei.txt", "codas.txt")

print("Begin parsing.\n")
p.parse_phonemes(1)
p.parse_phonemes(0)
p.parse_frequencies(1)
p.parse_frequencies(0)
p.parse_onsets_codas(0)
p.parse_nuclei()

print("Parsing complete. Display consonant information.\n")
print(p.consonants, "\n")
print(p.consonant_frequencies, "\n")

print("Display vowel information.\n")
print(p.vowels, "\n")
print(p.vowel_frequencies, "\n")

print("Display phonotactic information.\n")
print(p.onsets, "\n")
print(p.nuclei, "\n")
