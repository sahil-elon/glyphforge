# GlyphForge

Beginner-friendly Pointwise/Glyph workflow generator for aerospace CFD learners.

GlyphForge helps students create organized starter folders for Pointwise meshing workflows, Glyph script templates, boundary-name documentation, mesh parameter notes, and SU2-ready workflow notes.

## Why this exists

Beginners often struggle with:

- inconsistent boundary names
- missing mesh notes
- messy Pointwise-to-SU2 workflow
- undocumented spacing/growth-rate choices
- not knowing how to start a Glyph script

GlyphForge gives them a clean starting point.

## Install locally

```bash
python -m pip install -e .
```

## First command

```bash
glyphforge init airfoil2d --solver SU2 --dim 2d --boundaries farfield,wall,inlet,outlet
```

## Output

```txt
cases/airfoil2d/
├─ glyph/
│  └─ airfoil2d_starter.glf
├─ mesh/
│  └─ mesh_parameters.json
├─ su2/
│  └─ boundary_names.md
├─ notes/
│  └─ workflow.md
└─ README.md
```

## Run tests

```bash
python -m unittest
```

## Roadmap

- [x] Generate starter Glyph script
- [x] Generate boundary-name docs
- [x] Generate mesh parameter JSON
- [x] Generate workflow notes
- [x] Add tests
- [ ] Add airfoil-specific template
- [ ] Add nozzle-specific template
- [ ] Add SU2 config marker checker
- [ ] Add Pointwise Glyph Server integration