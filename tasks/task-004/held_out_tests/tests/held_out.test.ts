import assert from "node:assert/strict";import test from "node:test";import {validate} from "../src/validator.js";
test("held-out: malformed JSON and work metric",()=>{const result=validate(["not-json",JSON.stringify({id:"1",title:"t",body:"b"})]);assert.deepEqual(result.errors,["json"]);assert.equal(result.parsePasses,2);});
