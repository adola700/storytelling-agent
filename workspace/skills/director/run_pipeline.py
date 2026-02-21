import sys, os, json, re, time

def log(msg): print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from director import generate_outline
from actor import perform_role

def parse_cast(direction: str) -> list[dict]:
    """Parse cast members from Director markdown output.

    Returns a list of dicts: [{character_name, acting_instructions}, ...]
    Falls back to a single "The Protagonist" entry if no ### Character: blocks found.
    """
    # Primary format: ### Character: <Name>
    blocks = re.split(r'(?=###\s+Character:\s*)', direction)
    cast = []
    for block in blocks:
        m = re.match(r'###\s+Character:\s*(.+)', block)
        if not m:
            continue
        character_name = m.group(1).strip()
        # Extract Acting Instructions section
        instr_match = re.search(
            r'\*\*Acting Instructions:\*\*\s*\n([\s\S]*?)(?=\n##|\n###|\Z)',
            block,
        )
        acting_instructions = instr_match.group(1).strip() if instr_match else block.strip()
        cast.append({"character_name": character_name, "acting_instructions": acting_instructions})

    if cast:
        return cast

    # Fallback A: **Actor:** Elena
    m = re.search(r'\*\*Actor:\*\*\s*([^\n]+)', direction)
    if m:
        name = re.split(r'\s+[-–—(]', m.group(1))[0].strip()
        return [{"character_name": name, "acting_instructions": direction}]

    # Fallback B: Cast section with bold name
    m = re.search(r'Cast[\s\S]{0,150}?-\s*\*\*([^*\n]+)\*\*', direction)
    if m:
        name = re.split(r'\s+[-–—(]', m.group(1))[0].strip()
        return [{"character_name": name, "acting_instructions": direction}]

    return [{"character_name": "The Protagonist", "acting_instructions": direction}]


def extract_scene_blueprint(direction: str) -> str:
    """Extract the ## Scene Blueprint section from the Director output."""
    m = re.search(r'(##\s+Scene Blueprint[\s\S]*)', direction)
    return m.group(1).strip() if m else direction


def main():
    if len(sys.argv) != 3:
        print(
            "\n╔══════════════════════════════════════════════════════════════════════════════╗\n"
            "║                              USAGE ERROR                                    ║\n"
            "╠══════════════════════════════════════════════════════════════════════════════╣\n"
            "║ Usage: python3 run_pipeline.py <premise-file> <output-file>                 ║\n"
            "║                                                                              ║\n"
            "║ Arguments:                                                                   ║\n"
            "║   premise-file : Path to file containing the story premise (required)        ║\n"
            "║   output-file  : Path for JSON output (required)                             ║\n"
            "╚══════════════════════════════════════════════════════════════════════════════╝\n",
            file=sys.stderr,
        )
        sys.exit(1)

    premise_file = sys.argv[1]
    output_file = sys.argv[2]

    print(
        "\n╔══════════════════════════════════════════════════════════════════════════════╗\n"
        "║                        STORYTELLING PIPELINE START                          ║\n"
        "╚══════════════════════════════════════════════════════════════════════════════╝\n"
    )

    with open(premise_file, "r", encoding="utf-8") as f:
        premise = f.read().strip()

    # ── Verification logging (temporary) ──────────────────────────────────────
    with open("/tmp/oc-premise-log.txt", "a", encoding="utf-8") as logf:
        logf.write(f"\n{'='*80}\n")
        logf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] PREMISE INPUT ({len(premise)} chars)\n")
        logf.write(f"{'='*80}\n")
        logf.write(premise)
        logf.write(f"\n{'='*80}\n\n")
    log(f"📝 Premise logged to /tmp/oc-premise-log.txt ({len(premise)} chars)")

    print("📄 INPUT:")
    print("─" * 80)
    preview = premise[:150] + ("..." if len(premise) > 150 else "")
    print(f"Premise: {preview}")
    print("─" * 80)
    print()

    # ── Stage 1: Director ────────────────────────────────────────────────────────
    print(
        "\n┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│ STAGE 1: DIRECTOR - Scene Planning                                          │\n"
        "└─────────────────────────────────────────────────────────────────────────────┘"
    )
    log("🎬 Calling Director LLM (OpenAI)...")
    print()

    direction = generate_outline(premise)

    log(f"✓ Scene plan received ({len(direction)} characters)")

    cast = parse_cast(direction)
    cast_names = ", ".join(c["character_name"] for c in cast)
    print(f"🎭 Cast: {cast_names}")

    print("\n📋 SCENE PLAN PREVIEW:")
    print("─" * 80)
    preview_text = direction[:300].replace("\n", "\n   ")
    print(f"   {preview_text}{'...' if len(direction) > 300 else ''}")
    print("─" * 80)

    scene_blueprint = extract_scene_blueprint(direction)

    # ── Stage 2: Actor (one call per cast member) ─────────────────────────────
    print(
        "\n┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│ STAGE 2: ACTOR - Character Performance(s)                                   │\n"
        "└─────────────────────────────────────────────────────────────────────────────┘"
    )

    result_cast = []
    for member in cast:
        name = member["character_name"]
        instructions = member["acting_instructions"]
        log(f"🎭 Performing as: {name}")
        log("🎬 Calling Actor LLM (OpenAI)...")
        print()

        performance = perform_role(name, instructions, scene_blueprint)

        log(f"✓ Performance received ({len(performance)} characters)")
        print("\n🎪 PERFORMANCE PREVIEW:")
        print("─" * 80)
        perf_preview = performance[:300].replace("\n", "\n   ")
        print(f"   {perf_preview}{'...' if len(performance) > 300 else ''}")
        print("─" * 80)
        print()

        result_cast.append({
            "character_name": name,
            "acting_instructions": instructions,
            "actor_performance": performance,
        })

    # ── Write output ─────────────────────────────────────────────────────────
    result = {
        "scene_plan": direction,
        "cast": result_cast,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(
        "\n╔══════════════════════════════════════════════════════════════════════════════╗\n"
        "║                           PIPELINE COMPLETE ✓                               ║\n"
        "╠══════════════════════════════════════════════════════════════════════════════╣"
    )
    print(f"║ Cast:             {cast_names[:60]:<60} ║")
    print(f"║ Scene Plan:       {len(direction):<10} characters{' ' * 49} ║")
    print(f"║ Performances:     {len(result_cast):<10} character(s){' ' * 48} ║")
    print(f"║ Output File:      {output_file[:60]:<60} ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
