// Trusted verifier probe: print behavior, never a hard-coded success string.
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const load = (name) => import(pathToFileURL(resolve('dist/src', name)).href);
const task = process.argv[2];
let result;
if (task === 'task-001') {
  const { ContentService } = await load('content-service.js');
  let calls = 0;
  const service = new ContentService(async (key) => { calls += 1; await Promise.resolve(); return key; });
  result = { values: await Promise.all(['a', 'a', 'b'].map((key) => service.process(key))), calls };
} else if (task === 'task-002') {
  const { DeliveryService } = await load('delivery.js');
  const events = []; let callback; let finish;
  const done = new Promise((resolveDone) => { finish = resolveDone; });
  const service = new DeliveryService({ deliver: async () => {} });
  const clock = { now: () => 0, schedule: (_at, fn) => { callback = fn; return { cancel: () => { callback = undefined; } }; } };
  service.schedule({ id: 'probe', body: 'synthetic' }, 10, clock, { maxAttempts: 1 }, (event) => {
    events.push(event); if (event.type === 'completed' || event.type === 'failed') finish();
  });
  callback(); await done; result = events;
} else if (task === 'task-003') {
  const { saveContent } = await load('domain.js');
  const { MemoryRepository } = await load('persistence.js');
  const repository = new MemoryRepository();
  await saveContent(repository, { id: 'probe', body: 'synthetic' });
  result = await repository.find('probe');
} else if (task === 'task-004') {
  const { validate } = await load('validator.js');
  result = validate(['{"id":"x","title":"","body":"synthetic"}', 'null', 'broken']);
} else {
  throw new Error(`Unknown task: ${task}`);
}
console.log(JSON.stringify(result));
