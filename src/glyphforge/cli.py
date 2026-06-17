from __future__ import annotations

import argparse
import re
from pathlib import Path

from glyphforge.templates import (
    boundary_markdown,
    case_readme,
    glyph_template,
    mesh_parameters_json,
    workflow_markdown,
)


def clean_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_\-]+", "_", value)
    value = value.strip("_-")

    if not value:
        raise ValueError("Name cannot be empty.")

    return value


def parse_boundaries(raw: str) -> list[str]:
    boundaries = [clean_name(item) for item in raw.split(",") if item.strip()]

    if not boundaries:
        raise ValueError("At least one boundary is required.")

    duplicates = sorted({name for name in boundaries if boundaries.count(name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate boundary names found: {', '.join(duplicates)}")

    return boundaries


def create_case(
    case_name: str,
    output_dir: Path,
    solver: str,
    dim: str,
    boundaries: list[str],
    first_spacing: float,
    growth_rate: float,
    overwrite: bool = False,
) -> list[Path]:
    case_name = clean_name(case_name)
    dim = dim.lower()

    if dim not in {"2d", "3d"}:
        raise ValueError("Dimension must be either '2d' or '3d'.")

    if first_spacing <= 0:
        raise ValueError("first_spacing must be greater than zero.")

    if growth_rate < 1.0:
        raise ValueError("growth_rate must be 1.0 or greater.")

    root = output_dir / case_name

    if root.exists() and not overwrite:
        raise FileExistsError(
            f"{root} already exists. Use --overwrite if you want to replace files."
        )

    folders = [
        root / "glyph",
        root / "mesh",
        root / "su2",
        root / "notes",
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    files = {
        root / "glyph" / f"{case_name}_starter.glf": glyph_template(
            case_name=case_name,
            solver=solver,
            dim=dim,
            boundaries=boundaries,
            first_spacing=first_spacing,
            growth_rate=growth_rate,
        ),
        root / "mesh" / "mesh_parameters.json": mesh_parameters_json(
            case_name=case_name,
            solver=solver,
            dim=dim,
            boundaries=boundaries,
            first_spacing=first_spacing,
            growth_rate=growth_rate,
        ),
        root / "su2" / "boundary_names.md": boundary_markdown(
            case_name=case_name,
            boundaries=boundaries,
        ),
        root / "notes" / "workflow.md": workflow_markdown(
            case_name=case_name,
            solver=solver,
            dim=dim,
        ),
        root / "README.md": case_readme(case_name),
    }

    written: list[Path] = []

    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
        written.append(path)

    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glyphforge",
        description="Generate beginner-friendly Pointwise Glyph starter workflows.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init",
        help="Create a new GlyphForge mesh workflow starter case.",
    )

    init_parser.add_argument("case_name", help="Name of the new case.")

    init_parser.add_argument(
        "--out",
        default="cases",
        help="Output folder. Default: cases",
    )

    init_parser.add_argument(
        "--solver",
        default="SU2",
        help="Target CFD solver. Default: SU2",
    )

    init_parser.add_argument(
        "--dim",
        default="2d",
        choices=["2d", "3d"],
        help="Case dimension. Default: 2d",
    )

    init_parser.add_argument(
        "--boundaries",
        default="farfield,wall,inlet,outlet",
        help="Comma-separated boundary names.",
    )

    init_parser.add_argument(
        "--first-spacing",
        type=float,
        default=0.001,
        help="Starter first cell/edge spacing value.",
    )

    init_parser.add_argument(
        "--growth-rate",
        type=float,
        default=1.2,
        help="Starter mesh growth rate.",
    )

    init_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite files if the case already exists.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            boundaries = parse_boundaries(args.boundaries)

            written = create_case(
                case_name=args.case_name,
                output_dir=Path(args.out),
                solver=args.solver,
                dim=args.dim,
                boundaries=boundaries,
                first_spacing=args.first_spacing,
                growth_rate=args.growth_rate,
                overwrite=args.overwrite,
            )

            print(f"Created GlyphForge case: {Path(args.out) / clean_name(args.case_name)}")
            print("")
            print("Files written:")

            for path in written:
                print(f"  - {path}")

            print("")
            print("Next:")
            print(f"  Open {written[0]} in Pointwise or inspect it in VS Code.")

            return 0

    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())