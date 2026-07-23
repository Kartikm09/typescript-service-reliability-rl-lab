import type { Content } from "./domain.js";
export class MemoryRepository { readonly #items=new Map<string,Content>();async save(content:Content):Promise<void>{this.#items.set(content.id,structuredClone(content));}async find(id:string):Promise<Content|undefined>{return this.#items.get(id);} }
