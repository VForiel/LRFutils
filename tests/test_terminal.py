from LRFutils import color, progress, term


def test_clear_removes_color_codes():
    assert color.clear(color.red("error") + " " + color.on_green("ok")) == "error ok"


def test_hline_fills_the_terminal_width():
    assert len(term.hline("-")) == term.term_size


def test_progress_bar_prints_its_state(capsys):
    bar = progress.Bar(max=4, width=60, prefix="run")
    for i in range(5):
        bar(i)
    out = color.clear(capsys.readouterr().out)
    assert "run" in out
    assert "100%" in out
    assert "4/4" in out
