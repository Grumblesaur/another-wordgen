#!/usr/bin/python
# -*- coding: utf-8 -*-

# James Murphy
# word generator package
# module functions

import random as rand
import sys

class LingException(Exception):
	"""Exceptions related to Linguistic classes."""
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

class Word(object):
	"""Container class for Syllable"""
	def __init__(self, syllables, max_length = 5):
		self.syllables = []
		if type(syllables) is Syllable:
			self.syllables[0] = syllables
		elif type(syllables) is list:
			self.syllables[:] = syllables
		else:
			raise LingException("No syllables passed in!")
		self.max_length = max_length
	
	def append(self, syllable):
		self.syllables += [syllable]
		return len(self.syllables) - 1
	
	def as_string(self):
		return''.join([s.as_string()for s in self.syllables])
	
	# TODO:
	# create methods for applying rewrite rules
		
class Syllable(object):
	"""Container class for phonemes; stores phonemes in lists called
	'onset', 'nucleus', and 'coda', after the parts of a syllable."""
	def __init__(self, o, n, c):
		if type(n) is not list: # this is a kludge until I fix how nuclei
			self.nucleus = [n]  # phonemes are passed around
		else:
			self.nucleus = n
		self.onset = o
		self.coda = c
	
	def as_string(self):
		r = ""
		for p in self.onset:
			r += p.as_string()
		for p in self.nucleus:
			r += p.as_string()
		for p in self.coda:
			r += p.as_string()
		return r
		
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

class Phoneme(object):
	"""Container class for raw IPA strings, to be generated for insertion
	into a Syllable object."""
	
	def __init__(self, ipa_string):
		self.ipa = str(ipa_string)
	
	def __iter__(self):
		return iter(self)
	
	def as_string(self):
		return self.ipa
	

class Phonology:
	"""Class for organizing/categorizing IPA symbols for random
	phoneme generation and Phoneme and Syllable object construction."""
	# constructed with files containing information about a language's
	# phonology; will need phoneme frequency file later
	def __init__(self, cs, vs, fc, fv, on, nu, cd):
		"""Obtains filenames needed for later setup method calls and
		instantiates container members for phonemic and phonotactic
		information."""
		self.consonant_file = cs
		self.vowel_file = vs
		self.consonant_frequency_file = fc
		self.vowel_frequency_file = fv
		self.onset_rule_file = on
		self.nucleus_rule_file = nu
		self.coda_rule_file = cd
		
		self.consonants = {}
		self.consonant_frequencies = {}
		self.vowels = {}
		self.vowel_frequencies = {}
		self.onsets = []
		self.nuclei = []
		self.codas = []

	# if argument 'coda' is 1, parse coda rules, else parse onset rules	
	def parse_onsets_codas(self, coda):
		"""Creates a list of lists of tuples from a consonant rules file,
		either onsets or codas. Each tuple contains descriptors for a
		potential phoneme to be selected later. Each list of tuples contains
		tuples which, in order, describe the rules for an onset or coda.
		Multiple tuples indicate that the rule will produce a cluster,
		while a single tuple will produce a single-consonant onset or coda.
		"""
		rule_list = []
		switch = [self.onset_rule_file, self.coda_rule_file]
		rules = open(switch[coda])
		for line in rules:
			rule = []
			line = line.strip()
			if Helper.is_comment(line):
				continue
			if Helper.is_whitespace(line):
				continue
			else:
				line = line.replace(" ", "").replace("\t", "")
				line = line.split("+")
				for phone in line:
					phone = phone.split(",")
					phone = tuple(phone)
					rule.append(phone)
					rule_list.append(rule)
		if coda == 1:
			self.codas = rule_list[:]
		else:
			self.onsets = rule_list[:]
	
	def parse_nuclei(self):
		"""Creates a list of lists of tuples, where each tuple contains
		descriptors for a potential vowel to be selected, and each list of
		tuples describes the rules for a possible syllable nucleus."""
		rules = open(self.nucleus_rule_file)
		for line in rules:
			rule = []
			line = line.strip()
			if Helper.is_comment(line):
				continue
			if Helper.is_whitespace(line):
				continue
			else:
				line = line.replace(" ", "").replace("\t","")
				line = line.split("+")
				for phone in line:
					phone = phone.split(",")
					phone = tuple(phone)
					rule.append(phone)
				self.nuclei.append(rule)
		
	# when arg 'vow' is 1 or True, parses the vowel file
	# when arg 'vow' is 0 or False, parses the consonant file
	def parse_phonemes(self, vow):
		"""Gathers phonemes according to their category and stores them in
		a dictionary."""
		inventory = open((self.consonant_file, self.vowel_file)[vow], "r")
		
		# effectively a multiplexor switched by 'vow' arg later
		switch = [self.consonants, self.vowels]
		for line in inventory:
			# leading/trailing whitespace is a bitch, kill it.
			line = line.strip()
			if Helper.is_comment(line):
				continue
			if Helper.is_whitespace(line):
				continue
			else:
				pair = line.replace(" ", "").replace("\t", "").split(":")
				switch[vow][pair[0]] = pair[1].split(",")
		inventory.close()
	
	# as before, vow == 1 means parse the vowels, 0 parse the consonants
	def parse_frequencies(self, vow):
		"""Gathers phoneme-frequency pairs and stores them in a dictionary.
		"""
		frequencies = open((self.consonant_frequency_file,
		self.vowel_frequency_file)[vow])
		
		switch = [self.consonant_frequencies, self.vowel_frequencies]
		curr_category = ""
		for line in frequencies:
			line = line.strip().replace(" ", "").replace("\t", "")
			if Helper.is_comment(line):
				continue
			if Helper.is_whitespace(line):
				continue
			else:
				pair = line.split(":")
				switch[vow][pair[0]] = float(pair[1])
		frequencies.close()
	
	def generate_onset_coda(self, coda): # does not yet account for freqs
		"""Returns a list of Phoneme objects of either onset or coda
		structure. Generates a coda if coda arg is 1, else generates
		an onset."""
		rand.seed(None)
		possible = []
		phonemes = []
		rule = None
		if coda == 1:
			try:
				rule = self.codas[rand.randrange(0, len(self.codas)-1)]
			except:
				sys.stderr.write("Coda rule file is empty!")
				sys.exit()
		else:
			try:
				rule = self.onsets[rand.randrange(0,len(self.onsets)-1)]
			except:
				sys.stderr.write("Onset rule file is empty!")
				sys.exit()

		for t in rule:
			consonants = []
			for descriptor in t:
				consonants.append(self.consonants[descriptor])
			possible.append(consonants)
		for group in possible:
			matched = False
			phoneme_string = ""
			if len(group) == 1:
				phonemes.append(Phoneme(group[0][rand.randrange(0,
				len(group[0]))-1]))
			else:
				while not matched:
					incount = 0
					s = group[0][rand.randrange(0,len(group[0]))-1]
					phoneme_string = s
					for g in group[1:]:
						if s in g:
							incount += 1
					if incount == len(group[1:]):
						matched = True
				phonemes.append(Phoneme(phoneme_string))
		return phonemes

class Helper():
	"""Module to assist with file parsing."""
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
	def is_category(s): # turns out not to be necessary at the moment
		temp = not Helper.is_whitespace(s) and not Helper.is_comment(s)
		temp2 = temp and ":" not in s and "," not in s
		return temp2
