"""Local figure service used by the standalone PltEdit desktop application."""

from __future__ import annotations

import base64
import io
import json
import os
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from LRFutils.pltedit._io import get_metadata, load, save
from LRFutils.pltedit._style import set_style


figure: Figure | None = None
current_path: Path | None = None


def _artists(axis: Axes) -> list[tuple[str, int, Any]]:
    """Return the artist types currently supported by the desktop editor."""
    items: list[tuple[str, int, Any]] = []
    items.extend(("Line", index, artist) for index, artist in enumerate(axis.lines))
    items.extend(("Collection", index, artist) for index, artist in enumerate(axis.collections))
    items.extend(("Patch", index, artist) for index, artist in enumerate(axis.patches))
    items.extend(("Text", index, artist) for index, artist in enumerate(axis.texts))
    return items


def _color(value: Any) -> str:
    try:
        from matplotlib.colors import to_hex

        return to_hex(value, keep_alpha=False)
    except Exception:
        return "#000000"


def _artist_model(kind: str, index: int, artist: Any) -> dict[str, Any]:
    label = str(artist.get_label()) if hasattr(artist, "get_label") else ""
    if not label or label.startswith("_"):
        label = f"{kind} {index + 1}"
    result: dict[str, Any] = {"kind": kind, "index": index, "label": label}
    if kind == "Line":
        result.update({
            "color": _color(artist.get_color()),
            "linewidth": float(artist.get_linewidth()),
            "linestyle": str(artist.get_linestyle()),
            "marker": str(artist.get_marker()),
            "markersize": float(artist.get_markersize()),
        })
    elif kind in {"Collection", "Patch"}:
        face = artist.get_facecolors() if kind == "Collection" else [artist.get_facecolor()]
        edge = artist.get_edgecolors() if kind == "Collection" else [artist.get_edgecolor()]
        result.update({
            "facecolor": _color(face[0] if len(face) else "#000000"),
            "edgecolor": _color(edge[0] if len(edge) else "#000000"),
            "alpha": float(artist.get_alpha() if artist.get_alpha() is not None else 1),
        })
        if kind == "Patch":
            result["linewidth"] = float(artist.get_linewidth())
    elif kind == "Text":
        result.update({
            "text": artist.get_text(),
            "color": _color(artist.get_color()),
            "fontsize": float(artist.get_fontsize()),
            "rotation": float(artist.get_rotation()),
        })
    return result


def _model() -> dict[str, Any]:
    if figure is None:
        raise RuntimeError("No figure is open")
    suptitle = figure._suptitle
    axes: list[dict[str, Any]] = []
    for axis_index, axis in enumerate(figure.axes):
        legend = axis.get_legend()
        location = legend._loc if legend else "best"
        if isinstance(location, int):
            location = ["best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center"][min(location, 10)]
        axes.append({
            "index": axis_index,
            "title": axis.get_title(),
            "title_size": float(axis.title.get_fontsize()),
            "xlabel": axis.get_xlabel(),
            "xlabel_size": float(axis.xaxis.label.get_fontsize()),
            "ylabel": axis.get_ylabel(),
            "ylabel_size": float(axis.yaxis.label.get_fontsize()),
            "xscale": axis.get_xscale(),
            "yscale": axis.get_yscale(),
            "xlim": list(axis.get_xlim()),
            "ylim": list(axis.get_ylim()),
            "grid": any(line.get_visible() for line in axis.xaxis.get_gridlines()),
            "legend": legend is not None,
            "legend_location": location,
            "legend_size": float(legend.get_texts()[0].get_fontsize()) if legend and legend.get_texts() else 10,
            "xticks": [float(value) for value in axis.get_xticks()],
            "yticks": [float(value) for value in axis.get_yticks()],
            "xticklabels": [tick.get_text() for tick in axis.get_xticklabels()],
            "yticklabels": [tick.get_text() for tick in axis.get_yticklabels()],
            "xtick_size": float(axis.get_xticklabels()[0].get_fontsize()) if axis.get_xticklabels() else 10,
            "ytick_size": float(axis.get_yticklabels()[0].get_fontsize()) if axis.get_yticklabels() else 10,
            "artists": [_artist_model(kind, index, artist) for kind, index, artist in _artists(axis)],
        })
    return {
        "path": str(current_path) if current_path else None,
        "metadata": get_metadata(current_path) if current_path else {},
        "width": float(figure.get_figwidth()),
        "height": float(figure.get_figheight()),
        "dpi": float(figure.dpi),
        "title": suptitle.get_text() if suptitle else "",
        "title_size": float(suptitle.get_fontsize()) if suptitle else 14,
        "axes": axes,
        "styles": ["default"] + list(plt.style.available),
    }


def _find_artist(axis: Axes, kind: str, index: int) -> Any:
    groups = {"Line": axis.lines, "Collection": axis.collections, "Patch": axis.patches, "Text": axis.texts}
    return groups[kind][index]


def _apply_axis(axis: Axes, changes: dict[str, Any]) -> None:
    if "title" in changes: axis.set_title(changes["title"], fontsize=changes.get("title_size", axis.title.get_fontsize()))
    if "title_size" in changes: axis.set_title(axis.get_title(), fontsize=float(changes["title_size"]))
    if "xlabel" in changes: axis.set_xlabel(changes["xlabel"], fontsize=changes.get("xlabel_size", axis.xaxis.label.get_fontsize()))
    if "xlabel_size" in changes: axis.set_xlabel(axis.get_xlabel(), fontsize=float(changes["xlabel_size"]))
    if "ylabel" in changes: axis.set_ylabel(changes["ylabel"], fontsize=changes.get("ylabel_size", axis.yaxis.label.get_fontsize()))
    if "ylabel_size" in changes: axis.set_ylabel(axis.get_ylabel(), fontsize=float(changes["ylabel_size"]))
    if "xscale" in changes: axis.set_xscale(changes["xscale"])
    if "yscale" in changes: axis.set_yscale(changes["yscale"])
    if "xlim" in changes: axis.set_xlim(*changes["xlim"])
    if "ylim" in changes: axis.set_ylim(*changes["ylim"])
    if "grid" in changes: axis.grid(bool(changes["grid"]))
    if "legend" in changes:
        if changes["legend"]:
            axis.legend(loc=changes.get("legend_location", "best"), fontsize=changes.get("legend_size", 10))
        elif axis.get_legend(): axis.get_legend().remove()
    if "legend_location" in changes and axis.get_legend(): axis.legend(loc=changes["legend_location"], fontsize=changes.get("legend_size", 10))
    if "legend_size" in changes and axis.get_legend(): axis.legend(loc=changes.get("legend_location", "best"), fontsize=changes["legend_size"])
    for direction in ("x", "y"):
        if f"{direction}ticks" in changes: getattr(axis, f"set_{direction}ticks")(changes[f"{direction}ticks"])
        if f"{direction}ticklabels" in changes: getattr(axis, f"set_{direction}ticklabels")(changes[f"{direction}ticklabels"])
        if f"{direction}tick_size" in changes: axis.tick_params(axis=direction, labelsize=changes[f"{direction}tick_size"])


def _apply_artist(axis: Axes, changes: dict[str, Any]) -> None:
    artist = _find_artist(axis, changes["kind"], int(changes["index"]))
    if "label" in changes: artist.set_label(changes["label"] or "_nolegend_")
    if changes["kind"] == "Line":
        for key, setter in (("color", "set_color"), ("linewidth", "set_linewidth"), ("linestyle", "set_linestyle"), ("marker", "set_marker"), ("markersize", "set_markersize")):
            if key in changes: getattr(artist, setter)(changes[key])
    elif changes["kind"] in {"Collection", "Patch"}:
        for key, setter in (("facecolor", "set_facecolor"), ("edgecolor", "set_edgecolor"), ("alpha", "set_alpha"), ("linewidth", "set_linewidth")):
            if key in changes and hasattr(artist, setter): getattr(artist, setter)(changes[key])
    elif changes["kind"] == "Text":
        for key, setter in (("text", "set_text"), ("color", "set_color"), ("fontsize", "set_fontsize"), ("rotation", "set_rotation")):
            if key in changes: getattr(artist, setter)(changes[key])


def _render() -> str:
    if figure is None: raise RuntimeError("No figure is open")
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", bbox_inches="tight")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def handle(request: dict[str, Any]) -> dict[str, Any]:
    global figure, current_path
    command = request.get("command")
    if command == "open":
        current_path = Path(request["path"]).expanduser().resolve()
        figure = load(current_path)
        return {"model": _model(), "image": _render()}
    if command == "list":
        directory = Path(request.get("path") or Path.cwd()).expanduser().resolve()
        return {"directory": str(directory), "directories": sorted([item.name for item in directory.iterdir() if item.is_dir() and not item.name.startswith(".")]), "files": sorted([item.name for item in directory.glob("*.plt")])}
    if command == "update":
        if figure is None: raise RuntimeError("No figure is open")
        changes = request.get("changes", {})
        if "figure" in changes:
            settings = changes["figure"]
            if "style" in settings and settings["style"] != "default": figure = set_style(figure, settings["style"])
            if "width" in settings or "height" in settings: figure.set_size_inches(settings.get("width", figure.get_figwidth()), settings.get("height", figure.get_figheight()))
            if "title" in settings or "title_size" in settings: figure.suptitle(settings.get("title", figure._suptitle.get_text() if figure._suptitle else ""), fontsize=settings.get("title_size", 14))
        for axis_change in changes.get("axes", []): _apply_axis(figure.axes[int(axis_change["index"])], axis_change)
        for artist_change in changes.get("artists", []): _apply_artist(figure.axes[int(artist_change["axis"])], artist_change)
        return {"model": _model(), "image": _render()}
    if command == "save":
        if figure is None: raise RuntimeError("No figure is open")
        target = Path(request.get("path") or current_path)
        save(figure, target)
        current_path = target
        return {"model": _model()}
    if command == "export_png":
        if figure is None: raise RuntimeError("No figure is open")
        figure.savefig(request["path"], format="png", bbox_inches="tight")
        return {"path": request["path"]}
    raise ValueError(f"Unknown command: {command}")


def main() -> None:
    """Process JSON-lines requests from the Electron main process."""
    for line in sys.stdin:
        try:
            result = handle(json.loads(line))
            print(json.dumps({"ok": True, **result}, default=str), flush=True)
        except Exception as error:
            print(json.dumps({"ok": False, "error": str(error)}), flush=True)


if __name__ == "__main__":
    main()