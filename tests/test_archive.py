from __future__ import annotations

from datetime import datetime, timezone

import yaml

from LRFutils import archive


def test_new_creates_dated_archive_and_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(archive, "_git_metadata", lambda: {"commit": "abcdef123456", "branch": "main"})

    created = archive.new(
        "calibration",
        root=tmp_path,
        metadata={"operator": "V. Foriel", "instrument": "bench-A"},
        exposure=2.5,
        dark=True,
    )

    expected_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    assert created.path.parent.name == f"{expected_date}_abcdef1"
    metadata_path = created.path / "metadata.yml"
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    assert metadata_path.exists()
    assert metadata["git_commit"] == "abcdef123456"
    assert metadata["parameters"] == {"exposure": 2.5, "dark": True}
    assert metadata["operator"] == "V. Foriel"
    assert created.path.name.endswith("-calibration-exposure=2.5-dark=True")


def test_new_increments_archive_number(tmp_path, monkeypatch):
    monkeypatch.setattr(archive, "_git_metadata", lambda: {"commit": None, "branch": None})

    first = archive.new(root=tmp_path)
    second = archive.new(root=tmp_path)

    assert first.path.name == "0001"
    assert second.path.name == "0002"
    assert archive.latest(tmp_path).path == second.path

def test_name_and_parameters_are_made_filesystem_safe(tmp_path, monkeypatch):
    monkeypatch.setattr(archive, "_git_metadata", lambda: {"commit": None, "branch": None})

    created = archive.new("first light/test", root=tmp_path, path="a b")

    assert created.path.name == "0001-first-light-test-path=a-b"
    assert archive.description(x=1, flag=False) == "x=1-flag=False"
