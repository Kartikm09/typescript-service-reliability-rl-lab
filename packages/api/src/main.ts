import { createServer } from "node:http";
const port = Number.parseInt(process.env["APP_PORT"] ?? "8084", 10);
const server = createServer((request, response) => {
  if (request.url === "/health") {
    response.writeHead(200, { "content-type": "application/json" });
    response.end('{"status":"ok"}\n');
    return;
  }
  response.writeHead(404);
  response.end();
});
server.listen(port, "0.0.0.0", () => {
  console.log(`TypeScript service listening on ${String(port)}`);
});
