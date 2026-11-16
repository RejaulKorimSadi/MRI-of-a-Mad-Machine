# Artwork source

Python that draws every SVG in `assets/` (dark and light) and the 3D model.

```powershell
cd assets\source; npm i @fontsource/fraunces @fontsource/jetbrains-mono @fontsource/inter; py -m pip install fonttools brotli; py t_hero.py ..; py t_assets.py ..; py -c "import stl; open('../mri_machine_3d.stl','w').write(stl.ascii_stl(stl.model(56,12)))"
```

Fonts (Fraunces, JetBrains Mono, Inter; SIL Open Font Licence) are subset and embedded in each SVG, so the images look the same everywhere. Every number drawn in the artwork is taken from the thesis and checked against `verification/verification_report.txt`.
