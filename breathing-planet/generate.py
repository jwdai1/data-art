#!/usr/bin/env python3
"""
THERMAL PULSE — Breathing Planet
NASA GISS temperature anomaly data (1880-2025) rendered as generative art.

Outputs: thermal-pulse.png (4096x4096)
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math
import os

# ─── NASA GISS Data ───────────────────────────────────────────────────
GISS = [
    (1880,-0.17),(1881,-0.09),(1882,-0.11),(1883,-0.18),(1884,-0.28),
    (1885,-0.34),(1886,-0.32),(1887,-0.36),(1888,-0.18),(1889,-0.11),
    (1890,-0.36),(1891,-0.23),(1892,-0.28),(1893,-0.32),(1894,-0.31),
    (1895,-0.23),(1896,-0.12),(1897,-0.12),(1898,-0.28),(1899,-0.18),
    (1900,-0.09),(1901,-0.17),(1902,-0.29),(1903,-0.38),(1904,-0.48),
    (1905,-0.27),(1906,-0.23),(1907,-0.39),(1908,-0.43),(1909,-0.49),
    (1910,-0.45),(1911,-0.45),(1912,-0.37),(1913,-0.36),(1914,-0.16),
    (1915,-0.15),(1916,-0.37),(1917,-0.47),(1918,-0.31),(1919,-0.28),
    (1920,-0.28),(1921,-0.19),(1922,-0.29),(1923,-0.27),(1924,-0.28),
    (1925,-0.22),(1926,-0.11),(1927,-0.22),(1928,-0.20),(1929,-0.36),
    (1930,-0.16),(1931,-0.09),(1932,-0.16),(1933,-0.29),(1934,-0.13),
    (1935,-0.20),(1936,-0.15),(1937,-0.03),(1938, 0.00),(1939,-0.02),
    (1940, 0.12),(1941, 0.18),(1942, 0.06),(1943, 0.09),(1944, 0.20),
    (1945, 0.09),(1946,-0.07),(1947,-0.03),(1948,-0.11),(1949,-0.11),
    (1950,-0.17),(1951,-0.07),(1952, 0.01),(1953, 0.08),(1954,-0.13),
    (1955,-0.14),(1956,-0.19),(1957, 0.05),(1958, 0.06),(1959, 0.03),
    (1960,-0.02),(1961, 0.06),(1962, 0.03),(1963, 0.05),(1964,-0.20),
    (1965,-0.11),(1966,-0.06),(1967,-0.02),(1968,-0.08),(1969, 0.05),
    (1970, 0.03),(1971,-0.08),(1972, 0.01),(1973, 0.16),(1974,-0.07),
    (1975,-0.01),(1976,-0.10),(1977, 0.18),(1978, 0.07),(1979, 0.16),
    (1980, 0.25),(1981, 0.32),(1982, 0.14),(1983, 0.31),(1984, 0.15),
    (1985, 0.12),(1986, 0.18),(1987, 0.32),(1988, 0.39),(1989, 0.27),
    (1990, 0.45),(1991, 0.40),(1992, 0.22),(1993, 0.23),(1994, 0.31),
    (1995, 0.44),(1996, 0.33),(1997, 0.46),(1998, 0.61),(1999, 0.38),
    (2000, 0.39),(2001, 0.53),(2002, 0.62),(2003, 0.61),(2004, 0.53),
    (2005, 0.68),(2006, 0.64),(2007, 0.66),(2008, 0.54),(2009, 0.65),
    (2010, 0.72),(2011, 0.61),(2012, 0.64),(2013, 0.67),(2014, 0.75),
    (2015, 0.89),(2016, 1.01),(2017, 0.91),(2018, 0.85),(2019, 0.98),
    (2020, 1.01),(2021, 0.85),(2022, 0.89),(2023, 1.17),(2024, 1.28),
    (2025, 1.19),
]

MIN_A, MAX_A = -0.49, 1.28

# ─── Settings (Preset C: Supernova) ───────────────────────────────────
SEED = 42
SIZE = 4096
PARTICLES_PER_YEAR = 250
TURBULENCE = 5.0
TRAIL_STEPS = 50
NOISE_SCALE = 0.007
BREATHING_AMP = 3.0
SPHERE_RADIUS = 0.25  # fraction of canvas

# ─── Perlin Noise (pure numpy) ────────────────────────────────────────
class PerlinNoise:
    def __init__(self, seed=0):
        rng = np.random.RandomState(seed)
        self.p = np.arange(256, dtype=int)
        rng.shuffle(self.p)
        self.p = np.tile(self.p, 2)

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, t, a, b):
        return a + t * (b - a)

    def _grad(self, h, x, y, z):
        """Compute gradient dot product."""
        h = h & 15
        u = np.where(h < 8, x, y)
        v = np.where(h < 4, y, np.where((h == 12) | (h == 14), x, z))
        return np.where(h & 1, -u, u) + np.where(h & 2, -v, v)

    def noise3(self, x, y, z):
        """Vectorized 3D Perlin noise for arrays."""
        X = np.floor(x).astype(int) & 255
        Y = np.floor(y).astype(int) & 255
        Z = np.floor(z).astype(int) & 255
        x = x - np.floor(x)
        y = y - np.floor(y)
        z = z - np.floor(z)
        u = self._fade(x)
        v = self._fade(y)
        w = self._fade(z)

        p = self.p
        A  = p[X] + Y;     AA = p[A] + Z;   AB = p[A + 1] + Z
        B  = p[X + 1] + Y; BA = p[B] + Z;   BB = p[B + 1] + Z

        return self._lerp(w,
            self._lerp(v,
                self._lerp(u, self._grad(p[AA], x, y, z),
                              self._grad(p[BA], x-1, y, z)),
                self._lerp(u, self._grad(p[AB], x, y-1, z),
                              self._grad(p[BB], x-1, y-1, z))),
            self._lerp(v,
                self._lerp(u, self._grad(p[AA+1], x, y, z-1),
                              self._grad(p[BA+1], x-1, y, z-1)),
                self._lerp(u, self._grad(p[AB+1], x, y-1, z-1),
                              self._grad(p[BB+1], x-1, y-1, z-1))))

# ─── Color gradient ───────────────────────────────────────────────────
COLOR_STOPS = [
    (-0.50, (11,  11,  43)),
    (-0.25, (20,  60,  110)),
    (-0.05, (30,  100, 160)),
    ( 0.15, (60,  140, 180)),
    ( 0.35, (160, 150, 80)),
    ( 0.55, (200, 120, 50)),
    ( 0.75, (195, 60,  40)),
    ( 1.00, (230, 70,  30)),
    ( 1.30, (250, 170, 40)),
]

def anomaly_to_color(a):
    if a <= COLOR_STOPS[0][0]:
        return COLOR_STOPS[0][1]
    if a >= COLOR_STOPS[-1][0]:
        return COLOR_STOPS[-1][1]
    for i in range(len(COLOR_STOPS) - 1):
        t0, c0 = COLOR_STOPS[i]
        t1, c1 = COLOR_STOPS[i + 1]
        if t0 <= a <= t1:
            f = (a - t0) / (t1 - t0)
            f = f * f * (3 - 2 * f)  # smoothstep
            return tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
    return COLOR_STOPS[0][1]

# ─── Pseudo-random (deterministic per particle) ──────────────────────
def pseudo_random(yi, pi, ch):
    h = yi * 65537 + pi * 2147483647 + ch * 16807
    h = (((h >> 16) ^ h) * 0x45d9f3b) & 0xFFFFFFFF
    h = (((h >> 16) ^ h) * 0x45d9f3b) & 0xFFFFFFFF
    h = ((h >> 16) ^ h) & 0xFFFFFFFF
    return (h % 10000) / 10000.0

# ─── Main render ──────────────────────────────────────────────────────
def render():
    print(f"Rendering THERMAL PULSE at {SIZE}x{SIZE}...")

    np.random.seed(SEED)
    pnoise = PerlinNoise(SEED)

    # RGBA image for alpha compositing
    img = Image.new('RGBA', (SIZE, SIZE), (5, 5, 26, 255))

    cx, cy = SIZE / 2, SIZE / 2
    base_r = SIZE * SPHERE_RADIUS

    total_years = len(GISS)

    for yi, (year, anomaly) in enumerate(GISS):
        norm_a = (anomaly - MIN_A) / (MAX_A - MIN_A)
        time_frac = yi / (total_years - 1)

        col = anomaly_to_color(anomaly)
        num_particles = int(PARTICLES_PER_YEAR * (0.6 + norm_a * 0.8))

        base_alpha = int(15 + time_frac * 60 + norm_a * 35)
        base_alpha = min(base_alpha, 255)
        weight = max(1, int((1.0 + time_frac * 2.5 + norm_a * 1.5)))

        steps = max(15, int(TRAIL_STEPS * (1.2 - norm_a * 0.5)))
        turb = 0.15 + norm_a * TURBULENCE
        year_offset = yi * 137.508

        # Create a layer for this year
        layer = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)

        for p in range(num_particles):
            theta = pseudo_random(yi, p, 0) * 2 * math.pi
            phi = math.acos(1 - 2 * pseudo_random(yi, p, 1))
            projected_r = math.sin(phi)
            spawn_r = base_r * projected_r + (pseudo_random(yi, p, 2) - 0.5) * base_r * 0.12

            px = cx + math.cos(theta) * spawn_r
            py = cy + math.sin(theta) * spawn_r

            # Build trail points
            points = [(px, py)]
            for s in range(steps):
                angle = math.atan2(py - cy, px - cx)

                n1 = pnoise.noise3(
                    px * NOISE_SCALE + year_offset,
                    py * NOISE_SCALE,
                    yi * 0.03
                )
                n2 = pnoise.noise3(
                    px * NOISE_SCALE + 500,
                    py * NOISE_SCALE + 500,
                    yi * 0.03 + 100
                )

                noise_angle = (n1 - 0.0) * math.pi * 2 * turb  # n1 is ~[-1,1]
                radial = (n2 - 0.0) * turb * BREATHING_AMP + norm_a * 0.3 * BREATHING_AMP

                spd = 2.2 * (0.8 + projected_r * 0.6)

                px += -math.sin(angle) * spd + math.cos(noise_angle) * turb * 0.8 + math.cos(angle) * radial
                py +=  math.cos(angle) * spd + math.sin(noise_angle) * turb * 0.8 + math.sin(angle) * radial

                points.append((px, py))

            # Draw trail as connected line segments with fading alpha
            for s in range(len(points) - 1):
                fade = 1.0 - (s / len(points)) * 0.6
                alpha = int(base_alpha * fade)
                alpha = max(1, min(255, alpha))
                line_col = col + (alpha,)
                draw.line([points[s], points[s+1]], fill=line_col, width=weight)

        # Composite layer
        img = Image.alpha_composite(img, layer)

        # Progress
        if (yi + 1) % 10 == 0 or yi == total_years - 1:
            pct = int((yi + 1) / total_years * 100)
            print(f"  {year} ({pct}%)")

    # ─── Post-processing ──────────────────────────────────────────────

    # Subtle glow: duplicate, blur, screen-blend
    print("  Applying glow...")
    glow = img.copy()
    glow = glow.filter(ImageFilter.GaussianBlur(radius=30))
    # Screen blend: result = 1 - (1-a)(1-b)
    img_arr = np.array(img, dtype=np.float32) / 255.0
    glow_arr = np.array(glow, dtype=np.float32) / 255.0
    blended = 1.0 - (1.0 - img_arr) * (1.0 - glow_arr * 0.3)
    blended = (np.clip(blended, 0, 1) * 255).astype(np.uint8)
    img = Image.fromarray(blended, 'RGBA')

    # Convert to RGB for final PNG
    final = Image.new('RGB', (SIZE, SIZE), (5, 5, 26))
    final.paste(img, mask=img.split()[3])

    # Vignette
    print("  Applying vignette...")
    vig = np.zeros((SIZE, SIZE), dtype=np.float32)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2) / (SIZE * 0.5)
    vig = np.clip((dist - 0.6) * 1.2, 0, 1) ** 1.5
    final_arr = np.array(final, dtype=np.float32)
    bg = np.array([5, 5, 26], dtype=np.float32)
    for c in range(3):
        final_arr[:, :, c] = final_arr[:, :, c] * (1 - vig * 0.7) + bg[c] * vig * 0.7
    final = Image.fromarray(final_arr.astype(np.uint8), 'RGB')

    # Save
    out_path = os.path.join(os.path.dirname(__file__), 'thermal-pulse.png')
    final.save(out_path, 'PNG', optimize=True)
    print(f"\nDone: {out_path}")
    print(f"Size: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")

if __name__ == '__main__':
    render()
