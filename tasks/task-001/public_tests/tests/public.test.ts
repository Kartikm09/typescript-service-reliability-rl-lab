import assert from "node:assert/strict";
import test from "node:test";
import { ContentService } from "../src/content-service.js";
test("public: concurrent same-key calls share one effect", async () => { let calls=0; const service=new ContentService(async(key)=>{calls+=1;await Promise.resolve();return `result-${key}`;}); const results=await Promise.all([service.process("same"),service.process("same"),service.process("same")]); assert.deepEqual(results,["result-same","result-same","result-same"]);assert.equal(calls,1); });
