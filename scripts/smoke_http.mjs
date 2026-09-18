import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';

const child = spawn(process.execPath, ['packages/api/dist/main.js'], {
  env: { PATH: process.env.PATH, APP_HOST: '127.0.0.1', APP_PORT: '0' },
  stdio: ['ignore', 'pipe', 'pipe'],
});
try {
  const port = await new Promise((resolve, reject) => {
    let output = '';
    const deadline = setTimeout(() => { reject(new Error('HTTP server startup timed out')); }, 10000);
    child.once('error', (error) => { clearTimeout(deadline); reject(error); });
    child.once('exit', (code) => { clearTimeout(deadline); reject(new Error(`Server exited before readiness: ${code}`)); });
    child.stdout.on('data', (chunk) => {
      output += String(chunk);
      const match = /listening on (\d+)/.exec(output);
      if (match) { clearTimeout(deadline); resolve(Number(match[1])); }
    });
  });
  assert.ok(port > 0, 'server must report its actual ephemeral port');
  const health = await fetch(`http://127.0.0.1:${port}/health`, { signal: AbortSignal.timeout(5000) });
  assert.equal(health.status, 200);
  assert.deepEqual(await health.json(), { status: 'ok' });
  const missing = await fetch(`http://127.0.0.1:${port}/missing`, { signal: AbortSignal.timeout(5000) });
  assert.equal(missing.status, 404);
  assert.equal(await missing.text(), '');
  console.log('HTTP smoke passed: health 200, missing route 404');
} finally {
  if (child.exitCode === null && child.signalCode === null) {
    const exited = once(child, 'exit'); child.kill('SIGTERM'); await exited;
  }
}
