# Native Messaging & local HTTP Bridge Specifications

This reference provides the boilerplate templates and binary implementations required to build a zero-dependency Chrome Extension Native Messaging bridge and local HTTP port listener in Node.js.

## 1. Chrome Native Messaging Protocol (The Binary Header)
Chrome communicates with the native host using standard input/output. Each message is serialized as JSON, UTF-8 encoded, and preceded by a 32-bit message length in system native byte order (Little Endian on macOS/Intel/ARM).

### Node.js Binary Parser Implementation (`index.cjs`):
```javascript
#!/usr/local/bin/node
const fs = require('fs');
const http = require('http');

let messageBuffer = Buffer.alloc(0);
const pendingRequests = new Map();
let reqId = 0;

// Read binary data from Chrome stdin
process.stdin.on('data', (chunk) => {
    messageBuffer = Buffer.concat([messageBuffer, chunk]);

    while (messageBuffer.length >= 4) {
        // Read 32-bit length prefix
        const msgLen = messageBuffer.readUInt32LE(0);
        if (messageBuffer.length >= 4 + msgLen) {
            const msgBody = messageBuffer.slice(4, 4 + msgLen).toString('utf8');
            messageBuffer = messageBuffer.slice(4 + msgLen);
            handleChromeMessage(JSON.parse(msgBody));
        } else {
            break; // Wait for more data
        }
    }
});

// Self-terminate cleanly when Chrome disconnects
process.stdin.on('end', () => {
    process.exit(0);
});

// Write binary data to Chrome stdout
function sendToChrome(msg) {
    const msgStr = JSON.stringify(msg);
    const msgLen = Buffer.byteLength(msgStr, 'utf8');
    const header = Buffer.alloc(4);
    header.writeUInt32LE(msgLen, 0);
    process.stdout.write(header);
    process.stdout.write(msgStr);
}
```

---

## 2. Host Manifest Template (`com.thirdsignal.orbitalcontext.json`)
This file must be placed in `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/` on macOS.

```json
{
  "name": "com.thirdsignal.orbitalcontext",
  "description": "Orbital Context Native Messaging Host and MCP Server",
  "path": "/Users/lenoxparis/conductor/repos/orbital-context/mcp-host/index.cjs",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://dpehgfpjpjlfihhppllphgoacgffedpg/"
  ]
}
```

---

## 3. Background Service Worker Template (`background.js`)
Handles the browser-side connection to the native host, executing API queries on request.

```javascript
let nativePort = null;

function connectNativeHost() {
  nativePort = chrome.runtime.connectNative('com.thirdsignal.orbitalcontext');

  nativePort.onMessage.addListener((msg) => {
    if (msg.type === 'get_active_tabs') {
      chrome.tabs.query({}, (tabs) => {
        nativePort?.postMessage({ id: msg.id, result: tabs });
      });
    } else if (msg.type === 'close_tabs') {
      chrome.tabs.remove(msg.tabIds, () => {
        nativePort?.postMessage({ id: msg.id, result: { success: true } });
      });
    }
  });

  nativePort.onDisconnect.addListener(() => {
    console.error("Native port disconnected:", chrome.runtime.lastError?.message);
    nativePort = null;
  });
}

// Connect immediately
connectNativeHost();
```
