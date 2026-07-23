import assert from "node:assert/strict";import test from "node:test";import {readFile} from "node:fs/promises";
test("held-out: domain has no persistence import",async()=>{const source=await readFile("src/domain.ts","utf8");assert.equal(source.includes("persistence"),false);});
