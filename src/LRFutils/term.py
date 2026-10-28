import os

try:
    term_size = os.get_terminal_size()
    term_size = term_size.columns
except: term_size = 80

def hline(motif):
    """Return a horizontal line as wide as the terminal.

    Parameters
    ----------
    motif : str
        Characters repeated along the line.

    Returns
    -------
    str
        ``motif`` repeated to fill :data:`term_size` columns.

    Examples
    --------
    >>> from LRFutils import term
    >>> print(term.hline("─"))
    ────────────────────────────────────────────────────────────────────────────────
    >>> print(term.hline("=-"))
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    """
    return motif * int(term_size / len(motif))