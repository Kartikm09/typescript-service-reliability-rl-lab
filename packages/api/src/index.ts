import { parseContentJob, type ContentJob } from "@rl-lab/domain";
import type { DeliveryService } from "@rl-lab/jobs";
export interface ApiResponse {
  readonly status: number;
  readonly body: Readonly<Record<string, string>>;
}
export async function handleCreate(
  body: unknown,
  service: DeliveryService,
): Promise<ApiResponse> {
  const job: ContentJob = parseContentJob(body);
  const id = await service.process(job);
  return { status: 202, body: { id } };
}
