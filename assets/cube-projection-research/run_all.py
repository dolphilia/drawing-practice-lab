"""Rebuild and verify this research pack; does not run a human experiment."""
from pathlib import Path
import os, shutil, subprocess, sys

HERE=Path(__file__).resolve().parent
for name in ['probe.py','make_cases.py','test_geometry.py','evaluate.py',
             'supplement.py','source_model_check.py','make_materials.py','write_results_docs.py']:
    subprocess.run([sys.executable,str(HERE/name)],check=True)
renderer=os.environ.get('RSVG_CONVERT') or shutil.which('rsvg-convert')
if not renderer:raise RuntimeError('rsvg-convert required to render the original SVG figures')
for svg in sorted(HERE.glob('*.svg')):
    subprocess.run([renderer,str(svg),'-o',str(svg.with_suffix('.png'))],check=True)
print('Rebuilt calculations, original figures and result documents; visual review remains separate.')
