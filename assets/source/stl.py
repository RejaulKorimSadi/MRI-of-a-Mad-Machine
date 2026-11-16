import math, sys


def box(x, y, z, w, d, h):
    v = [(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z), (x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)]
    f = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    return [(v[a], v[b], v[c]) for a, b, c in f]


def torus(cx, cy, cz, R, r, nu, nv, axis='z'):
    tris = []

    def p(u, v):
        a, b = 2 * math.pi * u / nu, 2 * math.pi * v / nv
        x = (R + r * math.cos(b)) * math.cos(a)
        y = (R + r * math.cos(b)) * math.sin(a)
        z = r * math.sin(b)
        if axis == 'x':
            x, y, z = z, x, y
        return (cx + x, cy + y, cz + z)
    for i in range(nu):
        for j in range(nv):
            a, b, c, d = p(i, j), p(i + 1, j), p(i + 1, j + 1), p(i, j + 1)
            tris += [(a, b, c), (a, c, d)]
    return tris


def normal(t):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
    return nx / l, ny / l, nz / l


def model(nu=40, nv=10):
    T = []
    S, h, g = 60, 8, 12
    for i in range(3):                       # objective, context mixing, decoding
        T += box(-S / 2, -S / 2, i * (h + g), S, S, h)
    T += box(-S / 2 + 6, -S / 2 + 6, 3 * (h + g) - g + 4, 10, 10, 6)       # "the"
    T += box(-S / 2 + 20, -S / 2 + 10, 3 * (h + g) - g + 12, 12, 10, 6)    # "late"
    T += box(-S / 2 + 36, -S / 2 + 14, 3 * (h + g) - g + 22, 22, 10, 7)    # "Paul Graham"
    T += torus(0, 0, 1.5 * (h + g), 54, 4, nu, nv)                        # scan collar
    return T


def ascii_stl(T, name='mri_of_a_mad_machine'):
    out = [f'solid {name}']
    for t in T:
        n = normal(t)
        out.append(f' facet normal {n[0]:.3f} {n[1]:.3f} {n[2]:.3f}\n  outer loop')
        for v in t:
            out.append(f'   vertex {v[0]:.2f} {v[1]:.2f} {v[2]:.2f}')
        out.append('  endloop\n endfacet')
    out.append(f'endsolid {name}')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    full = model(56, 12)
    small = model(20, 5)
    open(sys.argv[1], 'w').write(ascii_stl(full))
    open(sys.argv[2], 'w').write(ascii_stl(small))
    print(len(full), len(small))


def model_towers(nb=1):
    T = []
    S, h, g = 34, 6, 5
    for k, xo in enumerate((-30, 30)):
        for i in range(5):
            T += box(xo - S / 2, -S / 2, i * (h + g), S, S, h)
    T += box(-60, -26, -4, 120, 52, 2)
    return T
