const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const { spawn } = require("node:child_process");
const readline = require("node:readline");
const path = require("node:path");

let backend;
let windowRef;
let requestId = 0;
const pending = new Map();

function startBackend() {
  const python = process.env.PLTEDIT_PYTHON || "python";
  backend = spawn(python, [path.join(__dirname, "backend.py")], {
    cwd: path.resolve(__dirname, ".."), windowsHide: true, stdio: ["pipe", "pipe", "ignore"],
  });
  const output = readline.createInterface({ input: backend.stdout });
  output.on("line", (line) => {
    try {
      const response = JSON.parse(line);
      const request = pending.values().next().value;
      if (request) {
        pending.delete(request.id);
        response.ok ? request.resolve(response) : request.reject(new Error(response.error));
      }
    } catch (error) { console.error("Invalid backend response:", error); }
  });
  backend.on("error", (error) => windowRef?.webContents.send("backend-error", error.message));
}

function callBackend(payload) {
  return new Promise((resolve, reject) => {
    const id = ++requestId;
    pending.set(id, { id, resolve, reject });
    backend.stdin.write(`${JSON.stringify(payload)}\n`);
  });
}

function createWindow() {
  windowRef = new BrowserWindow({
    width: 1500, height: 980, minWidth: 1100, minHeight: 720,
    backgroundColor: "#f8f9ff", title: "PltEdit",
    webPreferences: { contextIsolation: true, preload: path.join(__dirname, "preload.js") },
  });
  windowRef.loadFile(path.join(__dirname, "renderer", "index.html"));
  windowRef.on("closed", () => { windowRef = undefined; });
}

ipcMain.handle("backend-call", (_event, payload) => callBackend(payload));
ipcMain.handle("open-file", async () => {
  const result = await dialog.showOpenDialog(windowRef, { title: "Open a PltEdit figure", properties: ["openFile"], filters: [{ name: "PltEdit figures", extensions: ["plt"] }] });
  return result.canceled ? null : result.filePaths[0];
});
ipcMain.handle("save-file", async (_event, suggestedPath) => {
  const result = await dialog.showSaveDialog(windowRef, { title: "Save PltEdit figure", defaultPath: suggestedPath || "figure.plt", filters: [{ name: "PltEdit figures", extensions: ["plt"] }] });
  return result.canceled ? null : result.filePath;
});
ipcMain.handle("export-png", async (_event, suggestedPath) => {
  const result = await dialog.showSaveDialog(windowRef, { title: "Export PNG", defaultPath: suggestedPath || "figure.png", filters: [{ name: "PNG image", extensions: ["png"] }] });
  return result.canceled ? null : result.filePath;
});

app.whenReady().then(() => {
  startBackend();
  createWindow();
  const initialFile = process.argv.find((argument) => argument.toLowerCase().endsWith(".plt"));
  if (initialFile) windowRef.webContents.once("did-finish-load", () => windowRef.webContents.send("initial-file", initialFile));
  app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});
app.on("before-quit", () => backend?.kill());
app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });