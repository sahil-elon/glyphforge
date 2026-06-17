from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from glyphforge.cli import create_case, parse_boundaries


class TestGlyphForgeCLI(unittest.TestCase):
    def test_parse_boundaries(self):
        boundaries = parse_boundaries("farfield, wall, inlet, outlet")
        self.assertEqual(boundaries, ["farfield", "wall", "inlet", "outlet"])

    def test_create_case_writes_expected_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            written = create_case(
                case_name="airfoil2d",
                output_dir=Path(temp_dir),
                solver="SU2",
                dim="2d",
                boundaries=["farfield", "wall"],
                first_spacing=0.001,
                growth_rate=1.2,
            )

            paths = [path.name for path in written]

            self.assertIn("airfoil2d_starter.glf", paths)
            self.assertIn("mesh_parameters.json", paths)
            self.assertIn("boundary_names.md", paths)
            self.assertIn("workflow.md", paths)
            self.assertIn("README.md", paths)

            glyph_file = Path(temp_dir) / "airfoil2d" / "glyph" / "airfoil2d_starter.glf"
            content = glyph_file.read_text(encoding="utf-8")

            self.assertIn("GlyphForge Starter Script", content)
            self.assertIn("farfield", content)
            self.assertIn("wall", content)


if __name__ == "__main__":
    unittest.main()