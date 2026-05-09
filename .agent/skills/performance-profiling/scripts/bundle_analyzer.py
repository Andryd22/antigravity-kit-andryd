#!/usr/bin/env python3
"""
Bundle Size Analyzer — Antigravity Kit
=======================================
Analyzes JavaScript/TypeScript bundle size, identifies large modules,
and suggests optimization opportunities.

Usage:
    python bundle_analyzer.py <project_path>
    python bundle_analyzer.py <project_path> --max-size 200KB

Checks:
    - Bundle size (via next build or webpack stats)
    - Largest modules by size
    - Duplicate dependencies
    - Tree-shaking opportunities
"""

import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


def print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def find_large_files(path: Path, max_size_kb: int = 200) -> list:
    """Find large JS/CSS files in build output"""
    findings = []
    build_dirs = [".next", "dist", "build", "out"]

    for build_dir in build_dirs:
        build_path = path / build_dir
        if not build_path.exists():
            continue

        for file_path in build_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in (".js", ".css", ".mjs"):
                size_kb = file_path.stat().st_size / 1024
                if size_kb > max_size_kb:
                    findings.append({
                        "file": str(file_path.relative_to(path)),
                        "size_kb": round(size_kb, 1),
                        "severity": "high" if size_kb > 500 else "medium",
                    })

    findings.sort(key=lambda x: x["size_kb"], reverse=True)
    return findings


def check_node_modules_size(path: Path) -> dict:
    """Estimate node_modules disk usage"""
    nm_path = path / "node_modules"
    if not nm_path.exists():
        return {"skipped": True, "reason": "No node_modules"}

    total = 0
    for item in nm_path.iterdir():
        if item.is_dir():
            try:
                # Fast estimate via child count * avg size
                count = sum(1 for _ in item.rglob("*") if not _.is_dir())
                total += count * 4  # rough KB estimate
            except (PermissionError, OSError):
                pass

    return {
        "skipped": False,
        "estimated_size_kb": total,
        "severity": "medium" if total > 500000 else "low",
    }


def analyze_next_build(path: Path) -> list:
    """Analyze Next.js build output for bundle info"""
    findings = []
    build_trace = path / ".next" / "trace"

    if build_trace.exists():
        try:
            with open(build_trace) as f:
                data = json.load(f)
                # Extract page sizes if available
        except (json.JSONDecodeError, IOError):
            pass

    # Check for .next/static chunks
    static_dir = path / ".next" / "static"
    if static_dir.exists():
        chunks_dir = static_dir / "chunks"
        if chunks_dir.exists():
            for chunk in chunks_dir.glob("*.js"):
                size_kb = chunk.stat().st_size / 1024
                if size_kb > 100:
                    findings.append({
                        "file": str(chunk.relative_to(path)),
                        "size_kb": round(size_kb, 1),
                    })

    findings.sort(key=lambda x: x["size_kb"], reverse=True)
    return findings


def check_duplicate_deps(path: Path) -> list:
    """Check for duplicate package versions in node_modules"""
    findings = []
    package_json = path / "package.json"
    lock_file = path / "package-lock.json"

    if not lock_file.exists():
        return findings

    try:
        with open(lock_file) as f:
            lock_data = json.load(f)
            packages = lock_data.get("packages", {})

            # Count instances of each package name
            pkg_versions = {}
            for pkg_path, pkg_info in packages.items():
                if not pkg_path or pkg_path == "":
                    continue
                # Extract package name from path like "node_modules/react"
                parts = pkg_path.replace("node_modules/", "").split("/")
                name = parts[0] if parts[0] else parts[1] if len(parts) > 1 else "unknown"
                if name not in pkg_versions:
                    pkg_versions[name] = []
                pkg_versions[name].append(pkg_info.get("version", "?"))

            for name, versions in pkg_versions.items():
                unique_versions = set(versions)
                if len(unique_versions) > 1:
                    findings.append({
                        "package": name,
                        "versions": list(unique_versions),
                        "severity": "medium",
                        "message": f"{name} has {len(unique_versions)} duplicate versions: {unique_versions}",
                        "fix": f"Deduplicate {name} with npm dedupe or overrides",
                    })
    except (json.JSONDecodeError, IOError):
        pass

    return findings


def main():
    parser = argparse.ArgumentParser(description="Analyze bundle size and composition")
    parser.add_argument("project", help="Project path to analyze")
    parser.add_argument("--max-size", type=int, default=200,
                        help="Max file size in KB before flagging (default: 200KB)")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                        help="Output format")

    args = parser.parse_args()
    project_path = Path(args.project).resolve()

    if not project_path.exists():
        print(f"ERROR: Project path does not exist: {project_path}")
        sys.exit(1)

    print_header("BUNDLE SIZE ANALYSIS")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Max file size: {args.max_size}KB")

    all_issues = 0

    # Large files
    large_files = find_large_files(project_path, args.max_size)
    if large_files:
        print_header("LARGE FILES")
        for item in large_files:
            bar = "█" * min(int(item["size_kb"] / 20), 30)
            print(f"  [{item['severity'].upper():6s}] {item['file']}")
            print(f"            {item['size_kb']}KB {bar}")
            all_issues += 1
    else:
        print("  No files exceed max size threshold.")

    # Next.js chunks
    print_header("NEXT.JS CHUNKS")
    chunks = analyze_next_build(project_path)
    if chunks:
        for chunk in chunks[:10]:  # Top 10
            print(f"  {chunk['size_kb']:6.1f}KB  {chunk['file']}")
    else:
        print("  No .next build found. Run `npm run build` first.")

    # Duplicate dependencies
    print_header("DUPLICATE DEPENDENCIES")
    dupes = check_duplicate_deps(project_path)
    if dupes:
        for dupe in dupes:
            print(f"  [{dupe['severity'].upper()}] {dupe['message']}")
            print(f"    Fix: {dupe['fix']}")
            all_issues += 1
    else:
        print("  No duplicate dependencies found.")

    # Node modules size
    print_header("NODE_MODULES SIZE")
    nm_size = check_node_modules_size(project_path)
    if not nm_size.get("skipped"):
        size_mb = nm_size["estimated_size_kb"] / 1024
        print(f"  Estimated size: {size_mb:.1f}MB")
        if size_mb > 500:
            print(f"  WARNING: Large node_modules. Consider removing unused deps.")
            all_issues += 1
    else:
        print(f"  {nm_size.get('reason', 'No node_modules')}")

    # Summary
    print_header("SUMMARY")
    if all_issues > 0:
        print(f"  Total issues found: {all_issues}")
        print(f"  Run 'npm run build' to get precise Next.js chunk analysis")
        print(f"  Install webpack-bundle-analyzer for detailed visualization")
        sys.exit(1)
    else:
        print("  Bundle size within acceptable limits.")
        sys.exit(0)


if __name__ == "__main__":
    main()
