const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("plteditDesktop", {
  callBackend: (payload) => ipcRenderer.invoke("backend-call", payload),
  openFile: () => ipcRenderer.invoke("open-file"),
  saveFile: (suggestedPath) => ipcRenderer.invoke("save-file", suggestedPath),
  exportPng: (suggestedPath) => ipcRenderer.invoke("export-png", suggestedPath),
  onInitialFile: (callback) => ipcRenderer.on("initial-file", (_event, filePath) => callback(filePath)),
  onBackendError: (callback) => ipcRenderer.on("backend-error", (_event, message) => callback(message)),
});