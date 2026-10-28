"""Tests for pltedit save/load functionality."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

from LRFutils import pltedit
from LRFutils.pltedit._io import save, load, get_metadata


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def simple_figure():
    """Return a simple matplotlib figure with one line plot."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6], label="test")
    ax.set_title("Test figure")
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    yield fig
    plt.close(fig)


@pytest.fixture()
def plt_file(tmp_path, simple_figure):
    """Save the simple figure to a temp .plt file and return the path."""
    out = tmp_path / "test.plt"
    save(simple_figure, out)
    return out


# ---------------------------------------------------------------------------
# save() tests
# ---------------------------------------------------------------------------

class TestSave:
    def test_creates_file(self, tmp_path, simple_figure):
        out = tmp_path / "fig.plt"
        save(simple_figure, out)
        assert out.exists()

    def test_auto_adds_plt_extension(self, tmp_path, simple_figure):
        out = tmp_path / "fig"  # no extension
        save(simple_figure, out)
        assert (tmp_path / "fig.plt").exists()

    def test_accepts_axes(self, tmp_path, simple_figure):
        ax = simple_figure.get_axes()[0]
        out = tmp_path / "from_axes.plt"
        save(ax, out)
        assert out.exists()

    def test_rejects_non_figure(self, tmp_path):
        with pytest.raises(TypeError):
            save("not a figure", tmp_path / "bad.plt")

    def test_file_is_valid_npz(self, plt_file):
        archive = np.load(plt_file, allow_pickle=False)
        assert "figure" in archive
        assert "metadata" in archive

    def test_string_path(self, tmp_path, simple_figure):
        out = str(tmp_path / "str_path.plt")
        save(simple_figure, out)
        assert Path(out).exists()


# ---------------------------------------------------------------------------
# load() tests
# ---------------------------------------------------------------------------

class TestLoad:
    def test_returns_figure(self, plt_file):
        fig = load(plt_file)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_data_preserved(self, plt_file):
        fig = load(plt_file)
        ax = fig.get_axes()[0]
        line = ax.get_lines()[0]
        np.testing.assert_array_equal(line.get_xdata(), [1, 2, 3])
        np.testing.assert_array_equal(line.get_ydata(), [4, 5, 6])
        plt.close(fig)

    def test_labels_preserved(self, plt_file):
        fig = load(plt_file)
        ax = fig.get_axes()[0]
        assert ax.get_title() == "Test figure"
        assert ax.get_xlabel() == "X axis"
        assert ax.get_ylabel() == "Y axis"
        plt.close(fig)

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load(tmp_path / "nonexistent.plt")

    def test_invalid_file(self, tmp_path):
        bad = tmp_path / "bad.plt"
        bad.write_bytes(b"this is not a numpy archive")
        with pytest.raises(ValueError):
            load(bad)

    def test_string_path(self, plt_file):
        fig = load(str(plt_file))
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


# ---------------------------------------------------------------------------
# get_metadata() tests
# ---------------------------------------------------------------------------

class TestGetMetadata:
    def test_returns_dict(self, plt_file):
        meta = get_metadata(plt_file)
        assert isinstance(meta, dict)

    def test_required_keys(self, plt_file):
        meta = get_metadata(plt_file)
        for key in ("created_at", "python_version", "matplotlib_version", "pltedit_version"):
            assert key in meta, f"Missing key: {key}"

    def test_python_version(self, plt_file):
        meta = get_metadata(plt_file)
        assert sys.version in meta["python_version"]

    def test_matplotlib_version(self, plt_file):
        meta = get_metadata(plt_file)
        assert meta["matplotlib_version"] == matplotlib.__version__

    def test_pltedit_version(self, plt_file):
        meta = get_metadata(plt_file)
        assert meta["pltedit_version"] == pltedit.__version__

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            get_metadata(tmp_path / "nonexistent.plt")


# ---------------------------------------------------------------------------
# Round-trip tests
# ---------------------------------------------------------------------------

class TestRoundTrip:
    def test_multi_axes(self, tmp_path):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot([0, 1], [0, 1])
        ax2.scatter([0, 1, 2], [2, 1, 0])
        out = tmp_path / "multi.plt"
        save(fig, out)
        plt.close(fig)

        loaded = load(out)
        assert len(loaded.get_axes()) == 2
        plt.close(loaded)

    def test_image_figure(self, tmp_path):
        fig, ax = plt.subplots()
        data = np.random.default_rng(0).random((10, 10))
        ax.imshow(data)
        out = tmp_path / "image.plt"
        save(fig, out)
        plt.close(fig)

        loaded = load(out)
        assert len(loaded.get_axes()) == 1
        plt.close(loaded)

    def test_overwrite(self, tmp_path, simple_figure):
        out = tmp_path / "overwrite.plt"
        save(simple_figure, out)
        # Save again — should overwrite without error
        save(simple_figure, out)
        fig = load(out)
        plt.close(fig)


def test_get_metadata_is_public(tmp_path):
    fig, ax = plt.subplots()
    ax.plot([0, 1])
    pltedit.save(fig, tmp_path / "f.plt")
    assert pltedit.get_metadata(tmp_path / "f.plt")["matplotlib_version"] == matplotlib.__version__
    plt.close(fig)
