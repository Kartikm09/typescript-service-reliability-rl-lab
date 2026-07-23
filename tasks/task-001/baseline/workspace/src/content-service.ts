export class ContentService {
  readonly #completed = new Map<string, string>();
  constructor(private readonly sideEffect: (key: string) => Promise<string>) {}
  async process(key: string): Promise<string> {
    const completed = this.#completed.get(key);
    if (completed !== undefined) return completed;
    const result = await this.sideEffect(key);
    this.#completed.set(key, result);
    return result;
  }
}
