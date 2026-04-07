# data-art

Generative art driven by real-world scientific data. Each piece transforms public datasets into visual compositions through algorithmic processes — not AI image generation, but code that metabolizes data into form, color, and texture.

---

ジェネラティブアート。公開されている科学データを素材に、アルゴリズムによって視覚作品を生成する。AI画像生成ではなく、データを形・色・テクスチャに変換するコードによる表現。

## Works / 作品

### [Breathing Planet — Thermal Pulse](./breathing-planet/)

NASA GISS global temperature anomaly data (1880–2025) rendered as particle trails on a dark canvas. 146 years of climate data become visible as shifting turbulence, color, and density.

NASA GISS 地表面温度偏差データ（1880–2025）をパーティクルの軌跡として描画。146年分の気候データが、乱流・色彩・密度の変化として可視化される。

Three compositions:
- **C: Supernova** — Spherical projection, particles orbiting and scattering
- **A: Last Gasp** — Vertical strata, calm ocean below to burning sky above
- **B: Slow Burn** — Full-canvas flow field, all-over composition

## Stack / 技術

- Python (Pillow + NumPy)
- Custom Perlin noise implementation
- Direct PNG generation (no browser/canvas dependency)

## Philosophy / 哲学

Data art is not data visualization. The goal is not to communicate information efficiently, but to create works that move people — using real scientific data as raw material rather than invented aesthetics. The code is the brush; the data is the pigment.

データアートはデータ可視化ではない。目的は情報の効率的な伝達ではなく、人を動かす作品を作ること。実際の科学データを素材として使い、恣意的な美学ではなくデータそのものが形を決める。コードが筆であり、データが顔料である。
