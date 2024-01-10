const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
    openFileExplorer: () => ipcRenderer.send('open-file-explorer'),
    onDirectorySelected: (callback) => ipcRenderer.on('selected-directory', callback)
});
