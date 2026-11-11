#!/usr/bin/env python3
"""Independently check hidden trace spans using complete Shapely pour geometry.

Optional --baseline proves that every other nonmetadata circuit record remains
identical. This command does not modify circuit JSON.
"""
import argparse
import hashlib
import json
from pathlib import Path
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("circuit", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("--baseline", type=Path)
args = parser.parse_args()
circuit = json.loads(args.circuit.read_text())

def geometry(pour):
    if pour["shape"] == "brep":
        shape = pour["brep_shape"]
        points = lambda ring: [(p["x"], p["y"]) for p in ring["vertices"]]
        return Polygon(points(shape["outer_ring"]), [points(h) for h in shape["inner_rings"]])
    assert pour["shape"] == "rect", "Add coverage for this pour shape"
    w, h = pour["width"] / 2, pour["height"] / 2
    return translate(rotate(box(-w, -h, w, h), pour.get("rotation", 0), origin=(0, 0)), pour["center"]["x"], pour["center"]["y"])

sources = {t["source_trace_id"]: t for t in circuit if t["type"] == "source_trace"}
pours = {}
for pour in (p for p in circuit if p["type"] == "pcb_copper_pour"):
    shape = geometry(pour)
    assert shape.is_valid, f"Invalid pour: {pour['pcb_copper_pour_id']}"
    pours.setdefault((pour["source_net_id"], pour["layer"]), []).append(shape)
pours = {key: unary_union(shapes).buffer(1e-8) for key, shapes in pours.items()}
failures = []
hidden_count = 0
for trace in (t for t in circuit if t["type"] == "pcb_trace"):
    source_id = trace.get("source_trace_id")
    nets = sources.get(source_id, {}).get("connected_source_net_ids", [source_id])
    for start, end in zip(trace["route"], trace["route"][1:]):
        if not (start.get("is_inside_copper_pour") and end.get("is_inside_copper_pour")):
            continue
        hidden_count += 1
        same_layer_wires = start["route_type"] == end["route_type"] == "wire" and start["layer"] == end["layer"]
        line = LineString([(start["x"], start["y"]), (end["x"], end["y"])])
        shapes = [pours[(net, start.get("layer"))] for net in nets if (net, start.get("layer")) in pours]
        if not same_layer_wires or not shapes or not unary_union(shapes).covers(line):
            failures.append({"trace": trace["pcb_trace_id"], "start": start, "end": end})

report = {
    "source_circuit_sha256": hashlib.sha256(args.circuit.read_bytes()).hexdigest(),
    "hidden_segments_checked": hidden_count,
    "invalid_hidden_segments": failures,
    "coverage_basis": "Complete same-net, same-layer polygons with all holes; no point sampling",
}
if args.baseline:
    baseline = json.loads(args.baseline.read_text())
    def without_visibility(value):
        if isinstance(value, dict):
            return {k: without_visibility(v) for k, v in value.items() if k not in ("is_inside_copper_pour", "copper_pour_id")}
        if isinstance(value, list):
            return [without_visibility(v) for v in value]
        return value
    normalized = lambda data: without_visibility([r for r in data if r["type"] != "source_project_metadata"])
    unchanged = normalized(circuit) == normalized(baseline)
    report.update(
        baseline_circuit_sha256=hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
        all_nonmetadata_records_unchanged_except_visibility=unchanged,
        physical_pcb_records_sha256=hashlib.sha256(json.dumps(without_visibility([r for r in circuit if r["type"].startswith("pcb_")]), sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
    )
    assert unchanged, "A visibility fix must preserve copper, nets, footprints, placement and CAD"
args.output.parent.mkdir(exist_ok=True, parents=True)
args.output.write_text(json.dumps(report, indent=2) + "\n")
assert not failures, f"{len(failures)} uncovered trace sections are incorrectly hidden"
print(f"Checked {hidden_count} hidden trace spans: zero false hidden sections.")
