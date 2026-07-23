import type { ContentJob, ContentRepository } from "@rl-lab/domain";
export class MemoryContentRepository implements ContentRepository {
  readonly #jobs = new Map<string, ContentJob>();
  save(job: ContentJob): Promise<void> {
    this.#jobs.set(job.id, structuredClone(job));
    return Promise.resolve();
  }
  find(id: string): Promise<ContentJob | undefined> {
    const job = this.#jobs.get(id);
    return Promise.resolve(
      job === undefined ? undefined : structuredClone(job),
    );
  }
}
