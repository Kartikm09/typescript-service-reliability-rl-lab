import assert from "node:assert/strict";
import test from "node:test";
import { saveContent, type Content } from "../src/domain.js";
test("regression: alternate ports preserve public behavior", async () => {
  let saved = "";
  const repository = { save: async (content: Content) => { saved = content.id; }, find: async () => undefined };
  // Exercise public behavior without requiring the reference patch's particular port filename.
  await Reflect.apply(saveContent, undefined, [repository, { id: "x", body: "y" }]);
  assert.equal(saved, "x");
});
