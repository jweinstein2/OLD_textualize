const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const { dialog } = electron

const path = require('path')
const url = require('url')

let mainWindow

const { ipcMain } = electron
ipcMain.on('async-file-select', (event, arg) => {
    console.log(arg) // prints "ping"

    dialog.showOpenDialog(mainWindow, {
        buttonLabel: "Select",
        properties: ['openFile', 'openDirectory']
    }).then(result => {
        console.log(result.canceled)
        console.log(result.filePaths)
        event.reply('async-file-reply', result)
    }).catch(err => {
        console.log(err)
        event.reply('async-file-reply', err)
    })
})

function createWindow() {
    mainWindow = new BrowserWindow({
        show: false,
        title: "Textualize",
        webPreferences: {
            nodeIntegration: true, // SECURITY RISK: used to access ipcRenderer
        },
    })
    mainWindow.maximize()
    mainWindow.show()

    mainWindow.loadURL(
        process.env.ELECTRON_START_URL ||
        url.format({
            pathname: path.join(__dirname, '/../public/index.html'),
            protocol: 'file:',
            slashes: true
        })
    )

    mainWindow.on('closed', () => {
        mainWindow = null
    })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow()
    }
})
