import assert from "node:assert/strict";import test from "node:test";import {validate} from "../src/validator.js";
test("regression: error ordering",()=>assert.deepEqual(validate([JSON.stringify({id:1,title:2,body:3})]).errors,["id"]));
