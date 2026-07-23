export interface LogRecord {
  readonly event: string;
  readonly fields: Readonly<Record<string, string | number>>;
}
export interface Logger {
  write(record: LogRecord): void;
}
export class MemoryLogger implements Logger {
  readonly #records: LogRecord[] = [];
  write(record: LogRecord): void {
    this.#records.push(structuredClone(record));
  }
  records(): readonly LogRecord[] {
    return structuredClone(this.#records);
  }
}
