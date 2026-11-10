import { readFileSync } from "node:fs"
import { routingSignature } from "./signature"

console.log(routingSignature(JSON.parse(readFileSync(process.argv[2], "utf8"))))
