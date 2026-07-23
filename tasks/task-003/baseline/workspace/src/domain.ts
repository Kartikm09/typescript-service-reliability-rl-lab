import type { MemoryRepository } from "./persistence.js";
export interface Content { readonly id: string; readonly body: string; }
export async function saveContent(repository: MemoryRepository, content: Content): Promise<void> { await repository.save(content); }
