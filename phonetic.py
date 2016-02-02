class LingException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


class Syllable:
    onset = ""
    nucleus = ""
    coda = ""
    
    def __init__(self, o, n, c):
        if n == "":
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
        return self.onset != ""
    
    def has_coda(self):
        return self.coda != ""
        
    
