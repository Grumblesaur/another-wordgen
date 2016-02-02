#!/usr/bin/python
# -*- coding: utf-8 -*-

# James Murphy
# word generator package
# module functions

class LingException(Exception):
	"""Exceptions related to Linguistic classes."""
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

class Word:
	"""Container class for Syllable"""
	def __init__(self, syllables, max_length):
		self.syllables = None
		if type(syllables) is Syllable:
			self.syllables[0] = syllables
		elif type(syllables) is List:
			self.syllables[:] = syllables
		else:
			raise Exception("No syllables passed in!")
		self.max_length = max_length
	
	#@TODO: this
	def build_word():
		pass
		
class Syllable:
	"""Container class for phonemes; stores phonemes in lists called
	'onset', 'nucleus', and 'coda', after the parts of a syllable."""
	def __init__(self, o, n, c):
		if n == []:
			raise LingException("Syllable must contain nucleus!")
		self.onset = o
		self.nucleus = n
		self.coda = c
	
	def onset_is_cluster(self):
		return len(self.onset) > 1
	
	def nucleus_is_polyphthong(self):
		return len(self.nucleus) > 1
	
	def coda_is_cluster(self):
		return len(self.coda) > 1
		
	def has_onset(self):
		return self.onset != []
	
	def has_coda(self):
		return self.coda != []

class Phoneme:
	"""Container class for raw IPA strings, to be generated for insertion
	into a Syllable object."""
	
	def __init__(self, ipa_string):
		self.ipa = ipa_string
	

class Phonology:
	"""Class for organizing/categorizing IPA symbols for random
	phoneme generation and Phoneme and Syllable object construction."""
	
	# constructed with files containing information about a language's
	# phonology; will need phoneme frequency file later
	def __init__(self, consonants, vowels, phonotactics, frequencies):
		self.consonant_file = consonants
		self.vowel_file = vowels
		self.phonotactics_file = phonotactics
		self.frequencies_file = frequencies
		self.consonants = {}
		self.vowels = {}
		self.phonotactics = []
	
	# when arg 'vow' is 1 or True, parses the vowel file
	# when arg 'vow' is 0 or False, parses the consonant file
	def parse_phonemes(self, vow):
		inventory = open((self.consonant_file, self.vowel_file)[vow], "r")
		curr_category = ""
		
		# effectively a multiplexor switched by 'vow' arg later
		switch = [self.consonants, self.vowels]
		
		
		for line in inventory:
			# leading/trailing whitespace is a bitch, kill it.
			line = line.strip()
			if Helper.is_comment(line):
				continue
			if Helper.is_whitespace(line):
				continue
			if Helper.is_category(line):
				curr_category = line
				switch[vow][curr_category] = {}
			else:
				pair = line.split(":")
				switch[vow][curr_category][pair[0]] = pair[1].split(",")
		inventory.close()

class Helper:
	# figure this one out for yourself, nerd
	def is_whitespace(s):
		for c in s:
			if c not in "\t\n \r":
				return False
		return True
	
	# if a line contains "!!" ANYWHERE it is ignored. Not your typical
	# comment paradigm, but honestly, you don't need inline comments in
	# what is just a plaintext list of things
	def is_comment(s):
		return "!!" in s

	# determines whether a line bears categorical or phonetic information	
	def is_category(s):
		temp = not Helper.is_whitespace(s) and not Helper.is_comment(s)
		temp2 = temp and ":" not in s and "," not in s
		return temp2
