import os

try:
    term_size = os.get_terminal_size()
    term_size = term_size.columns
except: term_size = 80

def hline(motif):
    return motif * int(term_size / len(motif))