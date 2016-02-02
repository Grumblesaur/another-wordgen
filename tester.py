import phonetic

p = phonetic.Phonology("consonants.txt", "vowels.txt", "phonotactics.txt")

p.parse_phonemes(1)
p.parse_phonemes(0)

print(p.consonants)
print()
print(p.vowels)
