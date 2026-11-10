import stored from "./verified.json"
import { routingSignature } from "./signature"
export { routingSignature } from "./signature"

// A conservative guard: any routing input change requires regenerating and
// independently checking the stored copper. This also runs in the web viewer.
export async function verifiedRouting(input: any) {
  const signature = routingSignature(input)
  if (signature !== stored.input_signature) throw new Error(
    `Stored PCB routing is stale: expected ${stored.input_signature}, received ${signature}. Regenerate routing and repeat copper checks.`)
  const handlers: Record<string, (event: any) => void> = {}
  const traces = stored.traces
  return {
    on(event: string, handler: (event: any) => void) { handlers[event] = handler; return this },
    start() { handlers.complete?.({ traces }) },
    stop() {},
    getOutputSimpleRouteJson() { return { ...input, traces } },
  }
}
