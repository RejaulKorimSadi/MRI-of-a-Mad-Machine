import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else '..'


def chip_row(b, P, x, y, chips, size=11.5, ls=1.0):
    for t, c in chips:
        w = width(t, 'Mono', size) + len(t) * ls + 28
        b.append(f'<g class="rise" style="animation-delay:1.2s"><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="{c}" fill-opacity=".10" stroke="{c}" stroke-opacity=".7"/>'
                 f'<text x="{x+14:.0f}" y="{y+18.5}" class="m" font-size="{size}" letter-spacing="{ls}" fill="{c}">{t}</text></g>')
        x += w + 12
    return x


def hero(P, mode):
    W, H = 1200, 600
    b = [frame(W, H, P, 20), corners(W, H, P)]
    # ---------------- left column ----------------
    b.append(f'<text x="44" y="50" class="m mut" font-size="11" letter-spacing="2.2">MRI · SUBJECT: LANGUAGE MODEL · SEQUENCE: COMPONENT ABLATION</text>')
    b.append(f'<circle cx="{W-152}" cy="46" r="4" class="rd blink"/><text x="{W-140}" y="50" class="m mut" font-size="11" letter-spacing="2.2">LIVE SCAN</text>')
    b.append(f'<text x="62" y="126" class="m tl rise" font-size="13" letter-spacing="3" style="animation-delay:.1s">B.SC. THESIS · CSE · METROPOLITAN UNIVERSITY, SYLHET</text>')
    b.append(f'<text x="58" y="206" class="d ink rise" font-size="74" font-weight="600" letter-spacing="-1.6" style="animation-delay:.25s">MRI of a</text>')
    b.append(f'<text x="58" y="290" class="d ink rise" font-size="74" font-weight="600" letter-spacing="-1.6" style="animation-delay:.4s">Mad Machine<tspan class="rd">.</tspan></text>')
    q = 'The Structural Origins of Hallucination'
    qw = width(q, 'Disp', 26, 400, 'italic') + 12
    b.append(f'<clipPath id="qc"><rect x="58" y="304" width="{qw if STATIC else 0:.0f}" height="46">'
             + ('' if STATIC else f'<animate attributeName="width" from="0" to="{qw:.0f}" begin=".9s" dur="2.2s" fill="freeze" calcMode="spline" keySplines=".4 0 .2 1" keyTimes="0;1"/>')
             + f'</rect></clipPath><g clip-path="url(#qc)"><text x="60" y="336" class="d ink" font-size="26" font-style="italic">{e(q)}</text></g>'
             + ('' if STATIC else f'<rect x="60" y="316" width="2" height="27" class="tl"><animate attributeName="x" from="60" to="{60+qw:.0f}" begin=".9s" dur="2.2s" fill="freeze" calcMode="spline" keySplines=".4 0 .2 1" keyTimes="0;1"/><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'))
    for i, ln in enumerate(['Which part of a language model turns a defect', 'into a confident error? Three controlled studies',
                            'scan it, one component at a time.']):
        b.append(f'<text x="62" y="{388+i*25}" class="s mut rise" font-size="17" style="animation-delay:{.7+i*.12:.2f}s">{e(ln)}</text>')
    chip_row(b, P, 62, 468, [('21 MODELS', P['teal']), ('132/132 RE-VERIFIED', P['amber']), ('OPEN DATA', P['red'])])
    b.append(f'<path d="M62 540H{W-62}" stroke="{P["line"]}"/>')
    b.append(f'<text x="62" y="566" class="m fnt" font-size="11" letter-spacing="1.4">SADI · TASIN · CHOWDHURY — SUPERVISOR: GOLAM MOSTOFA NAEEM, LECTURER</text>')
    b.append(f'<text x="{W-62}" y="566" class="m fnt" font-size="11" letter-spacing="1.4" text-anchor="end">NOVEMBER 2026</text>')

    # ---------------- the machine (right) ----------------
    g = []
    ox, oy = 832, 312
    S, hgt, gap = 130, 28, 30
    zs = [i * (hgt + gap) for i in range(3)]
    layers = [('TRAINING OBJECTIVE', 'rewards the likely next word', P['red']),
              ('CONTEXT MIXING', 'attention or state space', P['teal']),
              ('DECODING', 'commits one token at a time', P['amber'])]
    cx, cy = iso(ox, oy, S / 2, S / 2, 0)
    R = 108
    rx, ry = R * 1.2247 * 1.05, R * .7071 * 1.05
    LX = 1012                                     # label column (right of the collar)
    g.append(f'<radialGradient id="hal" cx="{cx:.0f}" cy="{cy-40:.0f}" r="300" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{P["teal"]}" stop-opacity="{float(P["glow"])*.30:.2f}"/><stop offset="1" stop-color="{P["teal"]}" stop-opacity="0"/></radialGradient><circle cx="{cx:.0f}" cy="{cy-40:.0f}" r="300" fill="url(#hal)"/>')
    # iso floor grid
    g.append('<clipPath id="flc"><rect x="600" y="300" width="350" height="228"/></clipPath><g clip-path="url(#flc)">')
    for k in range(0, 10):
        a = k * 26 - 60
        p1, p2 = iso(ox, oy + 150, a, -60, 0), iso(ox, oy + 150, a, 190, 0)
        q1, q2 = iso(ox, oy + 150, -60, a, 0), iso(ox, oy + 150, 190, a, 0)
        g.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}M{q1[0]:.1f} {q1[1]:.1f}L{q2[0]:.1f} {q2[1]:.1f}" stroke="{P["line"]}" stroke-width=".8" opacity=".7"/>')
    g.append('</g>')
    g.append(f'<radialGradient id="shd"><stop offset="0" stop-color="#000" stop-opacity="{.12 if mode=="light" else .55}"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
             f'<ellipse cx="{cx:.1f}" cy="{cy+78:.1f}" rx="{rx:.1f}" ry="{ry*.7:.1f}" fill="url(#shd)"/>')
    # collar positions
    gy0 = cy - zs[2] - hgt / 2
    gy1 = cy + 4
    dur = 6
    collar_anim = '' if STATIC else (f'<animateTransform attributeName="transform" type="translate" values="0 {gy0-cy:.1f};0 {gy1-cy:.1f};0 {gy0-cy:.1f}" '
                                     f'keyTimes="0;.5;1" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>')
    PH = os.environ.get('PHASE', 'mid')
    st_off = (f' transform="translate(0 {dict(mid=(gy0+gy1)/2, top=gy0, bottom=gy1)[PH]-cy:.1f})"') if STATIC else ''

    def collar(half):
        sf = 0 if half == 'back' else 1
        d1 = f'M{cx-rx:.1f} {cy:.1f}A{rx:.1f} {ry:.1f} 0 0 {sf} {cx+rx:.1f} {cy:.1f}'
        d2 = f'M{cx-rx-10:.1f} {cy:.1f}A{rx+10:.1f} {ry+6:.1f} 0 0 {sf} {cx+rx+10:.1f} {cy:.1f}'
        op = .45 if half == 'back' else 1
        spin = '' if STATIC else f'<animate attributeName="stroke-dashoffset" from="0" to="{-36 if sf else 36}" dur="1.6s" repeatCount="indefinite"/>'
        return (f'<path d="{d1}" fill="none" stroke="{P["teal"]}" stroke-width="10" stroke-opacity="{.14*op:.2f}"/>'
                f'<path d="{d1}" fill="none" stroke="{P["teal"]}" stroke-width="2.2" stroke-opacity="{op}"/>'
                f'<path d="{d2}" fill="none" stroke="{P["teal"]}" stroke-width="1.2" stroke-opacity="{.6*op:.2f}" stroke-dasharray="2 7">{spin}</path>')
    plane = f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx-4:.1f}" ry="{ry-3:.1f}" fill="{P["teal"]}" fill-opacity="{float(P["glow"])*.16:.3f}"/>'
    g.append(f'<g{st_off}>{collar("back")}{collar_anim}</g>')
    # layers explode apart and reassemble (3D breathing), labels travel with their layer
    EX = 9
    for i, (name, desc, col) in enumerate(layers):
        z = zs[i]
        dy = {0: EX, 1: 0, 2: -EX}[i]
        part = [ibox(ox, oy, 0, 0, z, S, S, hgt, col, P)]
        tp = []
        for a in range(1, 5):
            t1, t2 = iso(ox, oy, a * S / 5, 0, z + hgt), iso(ox, oy, a * S / 5, S, z + hgt)
            u1, u2 = iso(ox, oy, 0, a * S / 5, z + hgt), iso(ox, oy, S, a * S / 5, z + hgt)
            tp.append(f'M{t1[0]:.1f} {t1[1]:.1f}L{t2[0]:.1f} {t2[1]:.1f}M{u1[0]:.1f} {u1[1]:.1f}L{u2[0]:.1f} {u2[1]:.1f}')
        part.append(f'<path d="{"".join(tp)}" stroke="{mix(col, P["bg"], .45)}" stroke-width=".8" fill="none" opacity=".8"/>')
        # flash when the collar passes this layer
        ylay = cy - z - hgt / 2
        t = min(max((ylay - gy0) / (gy1 - gy0), .03), .47)
        k1, k2 = t / 2, 1 - t / 2
        part.append(f'<path d="{itop(ox, oy, 0, 0, z + hgt, S, S)}" fill="{P["ink"]}" opacity="0">'
                    + ('' if STATIC else f'<animate attributeName="opacity" values="0;0;.5;0;0;.5;0;0" keyTimes="0;{max(k1-.05,0):.3f};{k1:.3f};{k1+.05:.3f};{k2-.05:.3f};{k2:.3f};{min(k2+.05,1):.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
                    + '</path>')
        lx, ly = iso(ox, oy, S, 0, z + hgt / 2)
        part.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3" fill="{col}"/><path d="M{lx+5:.1f} {ly:.1f}H{LX-8}" stroke="{col}" stroke-opacity=".55" stroke-dasharray="2 3"/>'
                    f'<text x="{LX}" y="{ly-4:.1f}" class="m" font-size="11" letter-spacing="1.1" fill="{col}">0{i+1} {name}</text>'
                    f'<text x="{LX}" y="{ly+13:.1f}" class="s mut" font-size="12.5">{e(desc)}</text>')
        anim = '' if STATIC else (f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {dy};0 {dy};0 0;0 0" keyTimes="0;.3;.5;.8;1" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;0 0 1 1;.4 0 .2 1;0 0 1 1"/>')
        sto = f' transform="translate(0 {dy})"' if (STATIC and PH != 'mid') else ''
        g.append(f'<g{sto}>{"".join(part)}{anim}</g>')
    g.append(f'<g{st_off}>{plane}{collar("front")}{collar_anim}</g>')

    # terminal row: prompt + generated tokens (above the machine, nothing overlaps)
    tx0, ty0 = 668, 78
    tw = 486
    g.append(f'<rect x="{tx0}" y="{ty0}" width="{tw}" height="40" rx="9" fill="{P["panel"]}" stroke="{P["line"]}"/>'
             f'<circle cx="{tx0+16}" cy="{ty0+20}" r="3.5" class="tl pulse"/>')
    pr = 'GPT-2 › Python was created by'
    g.append(f'<text x="{tx0+28}" y="{ty0+25}" class="m mut" font-size="12">{e(pr)}</text>')
    x = tx0 + 28 + width(pr, 'Mono', 12) + 10
    toks = [('the', P['ink'], 0), ('late', P['ink'], 1), ('Paul Graham', P['red'], 2)]
    for j, (t, col, k) in enumerate(toks):
        w = width(t, 'Mono', 12.5, 600) + 16
        anim = '' if STATIC else f' style="opacity:0;animation:tok{j} 6s {.5 + j*.5:.2f}s infinite"'
        g.append(f'<g{anim}><rect x="{x:.1f}" y="{ty0+8}" width="{w:.1f}" height="24" rx="6" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".8"/>'
                 f'<text x="{x+w/2:.1f}" y="{ty0+24.5}" class="m{" glitch" if k==2 else ""}" font-size="12.5" font-weight="600" text-anchor="middle" fill="{col}">{e(t)}</text></g>')
        x += w + 6
    g.append(f'<text x="{tx0}" y="{ty0+56}" class="m fnt" font-size="9.5" letter-spacing="1.4">REAL GPT-2 OUTPUT · CORRECT ANSWER: GUIDO VAN ROSSUM</text>')
    css_tok = ''.join(f'@keyframes tok{j}{{0%{{opacity:0;transform:translateY(8px)}}10%{{opacity:1;transform:none}}82%{{opacity:1}}94%,100%{{opacity:0}}}}' for j in range(3))
    # readout
    bx, by = 962, 446
    g.append(f'<text x="{bx}" y="{by-10}" class="m rd" font-size="10.5" letter-spacing="1.6">DIAGNOSIS: CONFIDENT ERROR</text>'
             f'<g transform="translate({bx} {by})"><rect width="176" height="52" rx="7" fill="{P["panel"]}" stroke="{P["line"]}"/>'
             f'<text x="12" y="21" class="m mut" font-size="10.5" letter-spacing="1">FLUENCY</text><text x="12" y="41" class="m mut" font-size="10.5" letter-spacing="1">TRUTH</text>'
             + ''.join(f'<rect x="{82+i*14}" y="11" width="9" height="12" rx="1.5" fill="{P["teal"]}"/>' for i in range(6))
             + ''.join(f'<rect x="{82+i*14}" y="31" width="9" height="12" rx="1.5" fill="none" stroke="{P["faint"]}"/>' for i in range(6))
             + f'<rect x="82" y="31" width="9" height="12" rx="1.5" fill="{P["red"]}" class="blink"/></g>')
    return svg(W, H, ''.join(b) + ''.join(g), P, defs=f'<style>{css_tok}</style>',
               title='MRI of a Mad Machine: The Structural Origins of Hallucination')


if __name__ == '__main__':
    write(OUT, 'hero', hero)
