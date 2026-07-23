import assert from "node:assert/strict";
import test from "node:test";
import { ContentService } from "../src/content-service.js";
test("regression: completed result is cached",async()=>{let calls=0;const service=new ContentService(async()=>{calls+=1;return "ok";});assert.equal(await service.process("x"),"ok");assert.equal(await service.process("x"),"ok");assert.equal(calls,1);});
