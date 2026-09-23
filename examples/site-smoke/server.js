const http = require("node:http");
const fs = require("node:fs/promises");
const path = require("node:path");

const root = path.resolve(__dirname, "../..");
const contentTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
};

http.createServer(async (request, response) => {
  if (!["GET", "HEAD"].includes(request.method)) {
    response.writeHead(405).end();
    return;
  }
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  } catch {
    response.writeHead(400).end();
    return;
  }
  let filename = path.resolve(root, "." + pathname);
  if (filename !== root && !filename.startsWith(root + path.sep)) {
    response.writeHead(403).end();
    return;
  }
  try {
    const stat = await fs.stat(filename);
    if (stat.isDirectory()) filename = path.join(filename, "index.html");
    if (!contentTypes[path.extname(filename)]) {
      response.writeHead(404).end();
      return;
    }
    const body = await fs.readFile(filename);
    response.writeHead(200, { "Content-Type": contentTypes[path.extname(filename)] });
    response.end(request.method === "HEAD" ? undefined : body);
  } catch {
    response.writeHead(404).end();
  }
}).listen(8766, "127.0.0.1");
