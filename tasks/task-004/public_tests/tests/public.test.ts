import assert from "node:assert/strict";import test from "node:test";import {validate} from "../src/validator.js";
test("public: outputs remain compatible",()=>{const result=validate([JSON.stringify({id:"1",title:"t",body:"b"}),JSON.stringify({id:"2",title:4,body:"b"})]);assert.deepEqual(result.values,[{id:"1",title:"t",body:"b"}]);assert.deepEqual(result.errors,["title"]);});
