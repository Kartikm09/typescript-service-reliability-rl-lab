import assert from "node:assert/strict";import test from "node:test";import {DeliveryService} from "../src/delivery.js";
test("regression: immediate delivery remains",async()=>{let calls=0;const service=new DeliveryService({deliver:async()=>{calls+=1;}});await service.deliverNow({id:"m",body:"x"});assert.equal(calls,1);});
