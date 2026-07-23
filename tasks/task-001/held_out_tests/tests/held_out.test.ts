import assert from "node:assert/strict";
import test from "node:test";
import { ContentService } from "../src/content-service.js";
test("held-out: distinct keys remain concurrent",async()=>{const pending=new Set<string>();let maximum=0;const service=new ContentService(async(key)=>{pending.add(key);maximum=Math.max(maximum,pending.size);await Promise.resolve();pending.delete(key);return key;});await Promise.all([service.process("a"),service.process("b")]);assert.equal(maximum,2);});
test("held-out: failure clears in-flight state",async()=>{let calls=0;const service=new ContentService(async()=>{calls+=1;if(calls===1)throw new Error("temporary");return "ok";});await assert.rejects(service.process("x"));assert.equal(await service.process("x"),"ok");});
