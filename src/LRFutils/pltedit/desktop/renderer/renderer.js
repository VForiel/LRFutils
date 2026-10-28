const api = window.plteditDesktop;
const state = { model: null, path: null, directory: null, busy: false };
const $ = (id) => document.getElementById(id);

function status(message, error = false) { $("status").textContent = message; document.body.classList.toggle("error", error); }
function escapeHtml(value) { return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[char]); }
function input(label, value, key, type = "text", extra = "") { return `<label class="control"><span>${label}</span><input data-key="${key}" type="${type}" value="${escapeHtml(value)}" ${extra}></label>`; }
function select(label, value, key, options) { return `<label class="control"><span>${label}</span><select data-key="${key}">${options.map((option) => `<option ${option === value ? "selected" : ""}>${escapeHtml(option)}</option>`).join("")}</select></label>`; }
function checkbox(label, value, key) { return `<label class="check-control"><input data-key="${key}" type="checkbox" ${value ? "checked" : ""}><span>${label}</span></label>`; }
function numeric(value) { return Number(value); }
function renderInspector() {
  const model = state.model;
  if (!model) return;
  const metadata = model.metadata || {};
  $("inspector-content").innerHTML = `<details open><summary>Figure</summary><div class="form-grid">${input("Title", model.title, "figure.title")}${input("Title size", model.title_size, "figure.title_size", "number", "min=1")}${input("Width", model.width, "figure.width", "number", "min=1")}${input("Height", model.height, "figure.height", "number", "min=1")}${select("Matplotlib style", "default", "figure.style", model.styles)}</div></details>${model.axes.map(renderAxis).join("")}<details><summary>File metadata</summary><div class="metadata"><span>Created</span><strong>${escapeHtml(metadata.created_at || "N/A")}</strong><span>Python</span><strong>${escapeHtml(metadata.python_version || "N/A")}</strong><span>Matplotlib</span><strong>${escapeHtml(metadata.matplotlib_version || "N/A")}</strong><span>PltEdit</span><strong>${escapeHtml(metadata.pltedit_version || "N/A")}</strong></div></details>`;
  $("inspector-content").querySelectorAll("[data-key]").forEach((control) => control.addEventListener("change", applyControl));
}
function renderAxis(axis) {
  const scales = ["linear", "log", "symlog", "logit"];
  const locations = ["best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center"];
  return `<details ${axis.index === 0 ? "open" : ""}><summary>Axes ${axis.index + 1}<span class="summary-hint">${escapeHtml(axis.title || "Untitled")}</span></summary><div class="form-grid">${input("Title", axis.title, `axis.${axis.index}.title`)}${input("Title size", axis.title_size, `axis.${axis.index}.title_size`, "number", "min=1")}${input("X label", axis.xlabel, `axis.${axis.index}.xlabel`)}${input("X size", axis.xlabel_size, `axis.${axis.index}.xlabel_size`, "number", "min=1")}${input("Y label", axis.ylabel, `axis.${axis.index}.ylabel`)}${input("Y size", axis.ylabel_size, `axis.${axis.index}.ylabel_size`, "number", "min=1")}${select("X scale", axis.xscale, `axis.${axis.index}.xscale`, scales)}${select("Y scale", axis.yscale, `axis.${axis.index}.yscale`, scales)}${input("X minimum", axis.xlim[0], `axis.${axis.index}.xlim.0`, "number")}${input("X maximum", axis.xlim[1], `axis.${axis.index}.xlim.1`, "number")}${input("Y minimum", axis.ylim[0], `axis.${axis.index}.ylim.0`, "number")}${input("Y maximum", axis.ylim[1], `axis.${axis.index}.ylim.1`, "number")}${checkbox("Show grid", axis.grid, `axis.${axis.index}.grid`)}${checkbox("Show legend", axis.legend, `axis.${axis.index}.legend`)}${select("Legend position", axis.legend_location, `axis.${axis.index}.legend_location`, locations)}${input("Legend size", axis.legend_size, `axis.${axis.index}.legend_size`, "number", "min=1")}${input("X ticks (comma separated)", axis.xticks.join(", "), `axis.${axis.index}.xticks`)}${input("Y ticks (comma separated)", axis.yticks.join(", "), `axis.${axis.index}.yticks`)}${input("X tick labels", axis.xticklabels.join(", "), `axis.${axis.index}.xticklabels`)}${input("Y tick labels", axis.yticklabels.join(", "), `axis.${axis.index}.yticklabels`)}${input("X tick size", axis.xtick_size, `axis.${axis.index}.xtick_size`, "number", "min=1")}${input("Y tick size", axis.ytick_size, `axis.${axis.index}.ytick_size`, "number", "min=1")}</div>${axis.artists.map((artist) => renderArtist(axis.index, artist)).join("")}</details>`;
}
function renderArtist(axisIndex, artist) {
  const key = `artist.${axisIndex}.${artist.kind}.${artist.index}`;
  const controls = [input("Legend label", artist.label, `${key}.label`)];
  if (artist.kind === "Line") controls.push(input("Color", artist.color, `${key}.color`, "color"), input("Line width", artist.linewidth, `${key}.linewidth`, "number", "min=0"), select("Line style", artist.linestyle, `${key}.linestyle`, ["-", "--", "-.", ":", "None"]), select("Marker", artist.marker, `${key}.marker`, ["None", ".", "o", "v", "^", "s", "*", "+", "x"]), input("Marker size", artist.markersize, `${key}.markersize`, "number", "min=0"));
  if (artist.kind === "Collection" || artist.kind === "Patch") controls.push(input("Face color", artist.facecolor, `${key}.facecolor`, "color"), input("Edge color", artist.edgecolor, `${key}.edgecolor`, "color"), input("Alpha", artist.alpha, `${key}.alpha`, "number", "min=0 max=1 step=.05"));
  if (artist.kind === "Patch") controls.push(input("Line width", artist.linewidth, `${key}.linewidth`, "number", "min=0"));
  if (artist.kind === "Text") controls.push(input("Text", artist.text, `${key}.text`), input("Color", artist.color, `${key}.color`, "color"), input("Font size", artist.fontsize, `${key}.fontsize`, "number", "min=1"), input("Rotation", artist.rotation, `${key}.rotation`, "number"));
  return `<details class="artist"><summary>${artist.kind} ${artist.index + 1}<span class="summary-hint">${escapeHtml(artist.label)}</span></summary><div class="form-grid">${controls.join("")}</div></details>`;
}
function parseTicks(value) { return String(value).split(",").map((part) => Number(part.trim())).filter(Number.isFinite); }
function applyControl(event) {
  const parts = event.target.dataset.key.split(".");
  const value = event.target.type === "checkbox" ? event.target.checked : event.target.value;
  const changes = { figure: {}, axes: [], artists: [] };
  if (parts[0] === "figure") changes.figure[parts[1]] = ["width", "height", "title_size"].includes(parts[1]) ? numeric(value) : value;
  if (parts[0] === "axis") {
    const axis = { index: Number(parts[1]) };
    if (["xlim", "ylim"].includes(parts[2])) { const source = state.model.axes[axis.index][parts[2]].slice(); source[Number(parts[3])] = numeric(value); axis[parts[2]] = source; }
    else if (["xticks", "yticks"].includes(parts[2])) axis[parts[2]] = parseTicks(value);
    else if (["xticklabels", "yticklabels"].includes(parts[2])) axis[parts[2]] = String(value).split(",").map((part) => part.trim());
    else if (["title_size", "xlabel_size", "ylabel_size", "legend_size", "xtick_size", "ytick_size"].includes(parts[2])) axis[parts[2]] = numeric(value);
    else axis[parts[2]] = value;
    changes.axes.push(axis);
  }
  if (parts[0] === "artist") { const artist = { axis: Number(parts[1]), kind: parts[2], index: Number(parts[3]) }; artist[parts[4]] = ["linewidth", "markersize", "alpha", "fontsize", "rotation"].includes(parts[4]) ? numeric(value) : value; changes.artists.push(artist); }
  update(changes);
}
async function update(changes) {
  if (state.busy) return;
  state.busy = true; $("dirty-mark").hidden = false; status("Updating...");
  try { const result = await api.callBackend({ command: "update", changes }); state.model = result.model; setPreview(result.image); renderInspector(); status("Unsaved changes"); } catch (error) { status(error.message, true); } finally { state.busy = false; }
}
function setPreview(image) { $("preview").src = `data:image/png;base64,${image}`; $("preview").hidden = false; $("preview-wrap").querySelector(".empty-state")?.remove(); }
async function openPath(filePath) {
  try { const result = await api.callBackend({ command: "open", path: filePath }); state.model = result.model; state.path = filePath; state.directory = filePath.replace(/[\\/][^\\/]+$/, ""); $("file-name").textContent = filePath.split(/[\\/]/).pop(); $("figure-caption").textContent = $("file-name").textContent; $("canvas-size").textContent = `${result.model.width.toFixed(1)} × ${result.model.height.toFixed(1)} in`; $("save-button").disabled = false; $("export-button").disabled = false; setPreview(result.image); renderInspector(); await listFiles(state.directory); status("Ready"); } catch (error) { status(error.message, true); }
}
async function listFiles(directory) { state.directory = directory; $("directory-input").value = directory; const result = await api.callBackend({ command: "list", path: directory }); $("file-list").innerHTML = [...result.directories.map((name) => `<button class="file-row folder" data-directory="${escapeHtml(name)}">▸ ${escapeHtml(name)}</button>`), ...result.files.map((name) => `<button class="file-row" data-file="${escapeHtml(name)}">▤ ${escapeHtml(name)}</button>`)].join(""); $("file-list").querySelectorAll("[data-file]").forEach((item) => item.onclick = () => openPath(`${directory}\\${item.dataset.file}`)); $("file-list").querySelectorAll("[data-directory]").forEach((item) => item.onclick = () => listFiles(`${directory}\\${item.dataset.directory}`)); }
$("open-button").onclick = async () => { const path = await api.openFile(); if (path) openPath(path); };
$("empty-open").onclick = $("open-button").onclick;
$("browse-button").onclick = $("open-button").onclick;
$("directory-input").onchange = () => listFiles($("directory-input").value);
$("up-button").onclick = () => listFiles(state.directory?.replace(/[\\/][^\\/]+$/, "") || ".");
$("save-button").onclick = async () => { const target = await api.saveFile(state.path); if (target) { await api.callBackend({ command: "save", path: target }); state.path = target; $("dirty-mark").hidden = true; status("Saved"); } };
$("export-button").onclick = async () => { const target = await api.exportPng((state.path || "figure").replace(/\.plt$/i, ".png")); if (target) { await api.callBackend({ command: "export_png", path: target }); status("PNG exported"); } };
+api.onInitialFile(openPath); api.onBackendError((message) => status(message, true)); listFiles(".").catch((error) => status(error.message, true));
