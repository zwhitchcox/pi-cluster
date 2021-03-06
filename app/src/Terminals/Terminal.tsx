import React, { useRef, useEffect, useState } from 'react'
import "xterm/css/xterm.css"
import { Terminal } from 'xterm'
import { WebLinksAddon } from 'xterm-addon-web-links'
import { AttachAddon } from 'xterm-addon-attach'
import { dialog } from 'electron'
import {v4 as uuid} from 'uuid'

declare var ipcRenderer;

const Term = () => {
  const [id, setId] = useState()
  const ref:any = useRef(null)
  useEffect(() => {
    const _id = uuid()
    setId(_id)
    const key = ipcRenderer.sendSync("get-key")
    if (key === undefined) {
      dialog.showErrorBox("No Key", "could not find a key at $HOME/.ssh/id_rsa")
    }
    ipcRenderer.send("run-cmd", {
      id,
      cmd: "ls",
      host: "192.168.1.85",
      key,
    })
  }, [])
  useEffect(() => {
    if (ref && ref.current !== null) {
      const term = new Terminal({ cols: 80, rows: 24})
      term.open(ref.current)

      // const ws = new WebSocket("ws://localhost:8080")
      // const attachAddon = new AttachAddon(ws)
      // term.loadAddon(attachAddon)
      // ws.onerror = console.error
    }
  }, [ref])
  return (
    <div id="terminal" ref={ref}>
    </div>
  )
}

export default Term