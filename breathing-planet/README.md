# Breathing Planet — Thermal Pulse

NASA GISS global mean temperature anomaly data (1880–2025) transformed into generative art. 146 years of planetary fever rendered as particle trails — each year a layer, each particle a breath.

NASA GISS 地表面温度偏差データ（1880–2025）をジェネラティブアートに変換。146年分の惑星の熱をパーティクルの軌跡として描画。各年がレイヤーとなり、各粒子が呼吸となる。

## Gallery / ギャラリー

### C: Supernova — 球体投影

![Supernova](thermal-pulse.png)

Particles spawn on a spherical surface projection (uniform distribution via `acos(1-2r)`), orbiting tangentially. High-anomaly years scatter particles outward — the sphere exhales, its skin breaking apart. Cool blue at the core, incandescent orange at the fraying edges.

球面投影上にパーティクルをスポーン。高anomaly年で粒子が外へ散逸し、球体の表皮が剥がれる。中心に冷たい青、外縁に白熱のオレンジ。

### A: Last Gasp — 縦の地層

![Last Gasp](thermal-pulse-last-gasp.png)

Vertical strata composition. Bottom = 1880 (calm, deep ocean), top = 2025 (burning sky). Particles flow horizontally within each year's band, turbulence increasing upward. The horizon catches fire. Time reads bottom-to-top like a geological core sample.

縦の地層構図。下が1880年（穏やかな深海）、上が2025年（燃える空）。年代ごとの水平バンド内でパーティクルが流れ、上に行くほど乱流が増す。地平線が炎上する。

### B: Slow Burn — 全面フローフィールド

![Slow Burn](thermal-pulse-slow-burn.png)

Full-canvas flow field with no geometric boundary. Particles spawn everywhere, following a dual-layer Perlin noise field that shifts with each year's anomaly value. The entire surface becomes a palimpsest of 146 years of flow — like ocean currents seen from orbit, or the tangled nervous system of a warming planet.

幾何学的な境界を持たない全面フローフィールド。二重レイヤーのPerlin noiseフィールドに沿って全面にパーティクルが流れる。146年分の流れが重なり合う。

## Algorithm / アルゴリズム

### Data / データ

NASA Goddard Institute for Space Studies (GISS) Surface Temperature Analysis v4. Annual global mean temperature anomaly (°C, baseline 1951–1980). Range: -0.49 (1909) to +1.28 (2024).

### Process / プロセス

1. For each year (1880–2025), spawn particles at composition-specific positions
2. Each particle traces a path following a Perlin noise flow field
3. The year's temperature anomaly modulates: turbulence amplitude, trail length, color, opacity, and stroke weight
4. Years are rendered sequentially — old layers underneath, recent on top
5. Post-processing: Gaussian blur screen-blend glow + radial vignette

### Color System / カラーシステム

9-stop thermodynamic gradient with smoothstep interpolation:

| Anomaly (°C) | Color | Name |
|---|---|---|
| -0.50 | `rgb(15,15,60)` | Glacial indigo |
| -0.25 | `rgb(25,75,140)` | Midnight blue |
| -0.05 | `rgb(40,120,200)` | Cerulean |
| +0.15 | `rgb(70,170,220)` | Steel cyan |
| +0.35 | `rgb(200,180,50)` | Oxidized amber |
| +0.55 | `rgb(240,130,30)` | Warm copper |
| +0.75 | `rgb(230,50,30)` | Vermillion |
| +1.00 | `rgb(255,60,20)` | Searing red |
| +1.30 | `rgb(255,200,50)` | Incandescent orange |

### Presets / プリセット

| Preset | Particles/yr | Turbulence | Trail | Noise | Breath | Radius |
|--------|-------------|-----------|-------|-------|--------|--------|
| A: Last Gasp | 320 | 4.2 | 70 | 0.005 | 2.8 | — |
| B: Slow Burn | 300 | 3.0 | 150 | 0.002 | 1.8 | — |
| C: Supernova | 250 | 5.0 | 50 | 0.007 | 3.0 | 0.25 |

## Run / 実行

Requires Python 3.8+ with Pillow and NumPy.

```bash
pip install Pillow numpy

# Generate each preset
python generate.py      # C: Supernova → thermal-pulse.png
python generate_a.py    # A: Last Gasp → thermal-pulse-last-gasp.png
python generate_b.py    # B: Slow Burn → thermal-pulse-slow-burn.png
```

Output: 4096x4096 PNG. Takes 3–30 minutes depending on preset.

## Data Source / データソース

- [NASA GISS Surface Temperature Analysis v4](https://data.giss.nasa.gov/gistemp/)
- Column: J-D (January–December annual mean)
- License: Public domain (US Government work)
