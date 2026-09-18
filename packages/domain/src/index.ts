export interface ContentJob {
  readonly id: string;
  readonly idempotencyKey: string;
  readonly payload: string;
}

export type DeliveryEvent =
  | {
      readonly type: "delivery.failed";
      readonly jobId: string;
      readonly attempts: number;
    }
  | {
      readonly type: "delivery.scheduled";
      readonly jobId: string;
      readonly at: number;
    }
  | { readonly type: "delivery.cancelled"; readonly jobId: string }
  | {
      readonly type: "delivery.completed";
      readonly jobId: string;
      readonly attempts: number;
    };

export interface ContentRepository {
  save(job: ContentJob): Promise<void>;
  find(id: string): Promise<ContentJob | undefined>;
}

export class ValidationError extends Error {
  public override readonly name = "ValidationError";
}

export function parseContentJob(value: unknown): ContentJob {
  if (typeof value !== "object" || value === null)
    throw new ValidationError("job must be an object");
  const record = value as Record<string, unknown>;
  for (const field of ["id", "idempotencyKey", "payload"] as const) {
    if (typeof record[field] !== "string" || record[field].length === 0)
      throw new ValidationError(`${field} must be a non-empty string`);
  }
  return {
    id: record["id"] as string,
    idempotencyKey: record["idempotencyKey"] as string,
    payload: record["payload"] as string,
  };
}
