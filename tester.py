import phonetic

p = phonetic.Phonology("cons.txt", "vowels.txt", "phono.txt", "freq.txt")

p.parse_phonemes(1)
p.parse_phonemes(0)

print(p.consonants)
print()
print(p.vowels)
