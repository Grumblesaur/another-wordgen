#!/usr/bin/python
# -*- coding: utf-8 -*-

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
		
	def build_word():
		pass
		
class Syllable:
	def __init__(self, o, n, c):
		if n == []:
			raise LingException("Syllable must contain nucleus!")
		self.onset = o
		self.nucleus = n
		self.coda = c
	
	def onset_is_cluster(self):
		return len(self.onset) > 1
	
	def nucleus_is_dipthong(self):
		return len(self.nucleus) > 1
	
	def coda_is_cluster(self):
		return len(self.coda) > 1
		
	def has_onset(self):
		return self.onset != []
	
	def has_coda(self):
		return self.coda != []

class Phoneme:
	ipa = ""
	
	def __init__(self, ipa_string):
		self.ipa = ipa_string
	

class Phonology:
	
	def __init__(self, consonants, vowels, phonotactics):
		self.consonant_file = consonants
		self.vowel_file = vowels
		self.phonotactics_file = phonotactics
		self.consonants = {}
		self.vowels = {}
		self.phonotactics = []
	
	def parse_phonemes(self, vow):
		inventory = open((self.consonant_file, self.vowel_file)[vow], "r")
		curr_category = ""
		switch = [self.consonants, self.vowels]
		for line in inventory:
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

	def is_whitespace(s):
		for c in s:
			if c not in "\t\n \r":
				return False
		return True
	
	def is_comment(s):
		return "!!" in s
	
	def is_category(s):
		temp = not Helper.is_whitespace(s) and not Helper.is_comment(s)
		temp2 = temp and ":" not in s and "," not in s
		return temp2
