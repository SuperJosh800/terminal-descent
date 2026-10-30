// Runs the Python game in Pyodide. The game's input() calls block on a shared buffer
// until the page writes the player's answer into it.
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs";

let control; // [answer ready flag, answer length]
let bytes;

self.write = (text) => postMessage({ type: "text", text });

self.ask = (prompt, choices) => {
  postMessage({ type: "ask", prompt, choices: JSON.parse(choices) });
  Atomics.wait(control, 0, 0);
  const answer = new TextDecoder().decode(bytes.slice(0, control[1]));
  Atomics.store(control, 0, 0);
  return answer;
};

self.onmessage = async ({ data }) => {
  control = new Int32Array(data.buffer, 0, 2);
  bytes = new Uint8Array(data.buffer, 8);
  try {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    await pyodide.pyimport("micropip").install("colorama");
    const files = await (await fetch("files.json")).json();
    for (const name of files) {
      pyodide.FS.writeFile(name, await (await fetch(name)).text());
    }
    postMessage({ type: "ready" });
    pyodide.runPython(`
import json, js, ui_bridge
ui_bridge.run_game(js.write, lambda prompt, choices: js.ask(prompt, json.dumps(choices)))
`);
    postMessage({ type: "done" });
  } catch (error) {
    postMessage({ type: "error", text: String(error) });
  }
};
