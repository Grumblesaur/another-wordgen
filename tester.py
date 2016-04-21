from source.phonetic import *
from random import randrange
from random import randint

path = "./rules/"

cons = path + "consonants.txt"
vows = path + "vowels.txt"
cons_freqs = path + "cons_freqs.txt"
vows_freqs = path + "vowel_freqs.txt"
onsets = path + "onsets.txt"
nuclei = path + "nuclei.txt"
codas = path + "codas.txt"

files = [cons, vows, cons_freqs, vows_freqs, onsets, nuclei, codas]

for s in files:
	s = path + s


p = Phonology(files[0], files[1], files[2], files[3], files[4], files[5],
files[6])

p.parse_phonemes(1)
p.parse_phonemes(0)
p.parse_frequencies(1)
p.parse_frequencies(0)
p.parse_onsets_codas(0)
p.parse_onsets_codas(1)
p.parse_nuclei()

dummy = [Phoneme("a"),Phoneme("e"),Phoneme("i"),Phoneme("o"),Phoneme("u")]
w = Word([])
for i in range(randrange(3) + 1):
	nuc = dummy[randint(0,4)]
	w.append(Syllable(p.generate_onset_coda(0), \
	nuc, p.generate_onset_coda(1)))

print(w.as_string())
