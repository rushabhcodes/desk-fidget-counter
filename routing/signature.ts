function canonical(value: any): any {
  if (Array.isArray(value)) return value.map(canonical)
  if (value && typeof value === "object") return Object.fromEntries(
    Object.keys(value).sort().map(key => [key, canonical(value[key])]))
  return value
}

export function routingSignature(input: any) {
  const data = JSON.stringify(canonical(input))
  let hash = 0xcbf29ce484222325n
  for (let i = 0; i < data.length; i++) {
    hash ^= BigInt(data.charCodeAt(i))
    hash = BigInt.asUintN(64, hash * 0x100000001b3n)
  }
  return hash.toString(16).padStart(16, "0")
}
