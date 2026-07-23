export interface Message { readonly id: string; readonly body: string; }
export interface Transport { deliver(message: Message): Promise<void>; }
export class DeliveryService { constructor(private readonly transport: Transport) {} async deliverNow(message: Message): Promise<void> { await this.transport.deliver(message); } }
