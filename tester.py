from phonetic import *

path = "./rules/"

cons = "consonants.txt"
vows = "vowels.txt"
cons_freqs = "cons_freqs.txt"
vows_freqs = "vowel_freqs.txt"
onsets = "onsets.txt"
nuclei = "nuclei.txt"
codas = "codas.txt"

files = [cons, vows, cons_freqs, vows_freqs, onsets, nuclei, codas]

for s in files:
	s = path + s


p = Phonology(files[0], files[1], files[2], files[3], files[4], files[5],
files[6])

print("Begin parsing.\n")
p.parse_phonemes(1)
p.parse_phonemes(0)
p.parse_frequencies(1)
p.parse_frequencies(0)
p.parse_onsets_codas(0)
p.parse_onsets_codas(1)
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

print("Begin syllable generation.")
dummy = [Phoneme("a")]
s = Syllable(p.generate_onset_coda(0), dummy, p.generate_onset_coda(1))


print('\n')
print(s.onset)
print(s.nucleus)
print(s.coda)
print(s)

word_string = ""

for ph in s.onset:
	word_string += ph.ipa
for ph in s.nucleus:
	word_string += ph.ipa
for ph in s.coda:
	word_string += ph.ipa

print(word_string)
