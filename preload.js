const { contextBridge, ipcRenderer } = require("electron/renderer");

contextBridge.exposeInMainWorld("electronAPI", {
  decrypt: () => ipcRenderer.invoke("decrypt"),
});
