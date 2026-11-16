import sys, math
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lib import *
import t_assets as T

OUT = sys.argv[1] if len(sys.argv) > 1 else '../../evidence/study_A_attention_ablation/assets'


def tower(ox, oy, P, col, n=5, S=86, hh=16, gp=10, label='', sub=''):
    g = []
    for j in range(n):
        z = j * (hh + gp)
        g.append(ibox(ox, oy, 0, 0, z, S, S, hh, col if j != n // 2 else col, P))
    return ''.join(g)


def ab_hero(P, mode):
    W, H = 1200, 560
    b = [frame(W, H, P, 20), corners(W, H, P)]
    b.append(f'<radialGradient id="hal" cx="880" cy="300" r="320" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{P["teal"]}" stop-opacity="{float(P["glow"])*.26:.2f}"/><stop offset="1" stop-color="{P["teal"]}" stop-opacity="0"/></radialGradient><circle cx="880" cy="300" r="320" fill="url(#hal)"/>')
    b.append(f'<text x="44" y="50" class="m mut" font-size="11" letter-spacing="2.2">STUDY A OF THE THESIS · MRI OF A MAD MACHINE</text>')
    b.append(f'<circle cx="{W-176}" cy="46" r="4" class="rd blink"/><text x="{W-164}" y="50" class="m mut" font-size="11" letter-spacing="2.2">14 MODELS · 8 GB</text>')
    b.append(f'<text x="62" y="124" class="m rd rise" font-size="13" letter-spacing="3" style="animation-delay:.1s">ARCHITECTURE ABLATION · HALLUCINATION</text>')
    b.append(f'<text x="58" y="200" class="d ink rise" font-size="68" font-weight="600" letter-spacing="-1.4" style="animation-delay:.25s">The Attention</text>')
    b.append(f'<text x="58" y="272" class="d ink rise" font-size="68" font-weight="600" letter-spacing="-1.4" style="animation-delay:.4s">Ablation Test<tspan class="rd">.</tspan></text>')
    for i, ln in enumerate(['Same data. Same tokenizer. Same scale.', 'Only the way the model mixes context changes.',
                            'Does a false sentence now win over what it knows?']):
        b.append(f'<text x="62" y="{322+i*27}" class="s {"ink" if i==2 else "mut"} rise" font-size="18" style="animation-delay:{.6+i*.12:.2f}s">{e(ln)}</text>')
    chips = [('650 vs 566 · p = 2.5×10⁻²⁰', P['red']), ('3 vs 3 FREE RECALL', P['teal'])]
    x = 62
    for t, c in chips:
        w = width(t.replace('⁻²⁰', '-20'), 'Mono', 11.5) + len(t) + 26
        b.append(f'<g class="rise" style="animation-delay:1.1s"><rect x="{x}" y="418" width="{w:.0f}" height="28" rx="14" fill="{c}" fill-opacity=".10" stroke="{c}" stroke-opacity=".7"/>'
                 f'<text x="{x+13}" y="436.5" class="m" font-size="11.5" letter-spacing="1" fill="{c}">{t}</text></g>')
        x += w + 10
    b.append(f'<path d="M62 488H{W-62}" stroke="{P["line"]}"/>')
    b.append(f'<text x="62" y="516" class="m fnt" font-size="11" letter-spacing="1.4">PYTHIA (ATTENTION) VS MAMBA (STATE SPACE) · 130M TO 2.8B · THE PILE · GPT-NEOX TOKENIZER</text>')
    # two towers
    g = []
    ax, bx, ty = 760, 1000, 280
    S, hh, gp, n = 92, 15, 11, 5
    g.append(f'<text x="{ax}" y="96" class="m rd" font-size="12" letter-spacing="1.6" text-anchor="middle">PYTHIA · ATTENTION</text>'
             f'<text x="{bx}" y="96" class="m tl" font-size="12" letter-spacing="1.6" text-anchor="middle">MAMBA · STATE SPACE</text>')
    for cx, col, kind in ((ax, P['red'], 'a'), (bx, P['teal'], 's')):
        for j in range(n):
            z = j * (hh + gp)
            c = col if j in (1, 3, n - 1) else mix(P['faint'], P['bg'], .15)
            g.append(ibox(cx, ty, 0, 0, z, S, S, hh, c, P))
            if j == n - 1:
                # mixing pattern on top face: attention = all-to-all arcs, ssm = sequential chain
                topz = z + hh
                pts = [iso(cx, ty, 14 + k * 16, S / 2, topz) for k in range(5)]
                if kind == 'a':
                    arcs = ''.join(f'M{pts[i][0]:.1f} {pts[i][1]:.1f}Q{(pts[i][0]+pts[k][0])/2:.1f} {min(pts[i][1],pts[k][1])-10-4*(k-i):.1f} {pts[k][0]:.1f} {pts[k][1]:.1f}'
                                   for i in range(5) for k in range(i + 1, 5))
                else:
                    arcs = ''.join(f'M{pts[i][0]:.1f} {pts[i][1]:.1f}L{pts[i+1][0]:.1f} {pts[i+1][1]:.1f}' for i in range(4))
                g.append(f'<path d="{arcs}" stroke="{P["ink"] if mode=="dark" else P["bg"]}" stroke-width="1.2" fill="none" opacity=".9"/>'
                         + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="{P["ink"] if mode=="dark" else P["bg"]}"/>' for x, y in pts))
    # shared base plate
    g.append(f'<path d="M{ax-80} {ty+112}H{bx+80}" stroke="{P["line"]}" stroke-width="1.2"/>'
             f'<text x="{(ax+bx)/2:.0f}" y="{ty+134}" class="m mut" font-size="11" letter-spacing="1.4" text-anchor="middle">SAME DATA · SAME TOKENIZER · SAME SCALE</text>')
    # planted false sentence feeding both
    py = 138
    g.append(f'<text x="{(ax+bx)/2:.0f}" y="{py-26}" class="m fnt" font-size="9.5" letter-spacing="1.4" text-anchor="middle">EXAMPLE ITEM (SCHEMATIC)</text>')
    g.append(f'<rect x="{(ax+bx)/2-150:.0f}" y="{py-18}" width="300" height="30" rx="8" fill="{P["panel"]}" stroke="{P["red"]}" stroke-dasharray="4 3"/>'
             f'<text x="{(ax+bx)/2:.0f}" y="{py+1}" class="m ink" font-size="12" text-anchor="middle">"The capital of Canada is <tspan class="rd">Toronto</tspan>."</text>')
    for cx in (ax, bx):
        g.append(f'<path d="M{(ax+bx)/2:.0f} {py+12}C{(ax+bx)/2:.0f} {py+40} {cx} {py+20} {cx} {py+52}" stroke="{P["red"]}" stroke-width="1.6" fill="none" stroke-dasharray="5 5">'
                 + ('' if STATIC else '<animate attributeName="stroke-dashoffset" from="0" to="-40" dur="1.4s" repeatCount="indefinite"/>') + '</path>')
    # outputs
    oy = ty + 146
    for cx, txt, col, cls, val in ((ax, 'Toronto', P['red'], 'rd', '650 / 666'), (bx, 'Ottawa', P['teal'], 'tl', '566 / 666')):
        g.append(f'<g class="float"><rect x="{cx-60}" y="{oy}" width="120" height="32" rx="8" fill="{col}" fill-opacity=".12" stroke="{col}"/>'
                 f'<text x="{cx}" y="{oy+21}" class="m {cls}{" glitch" if cls=="rd" else ""}" font-size="14" font-weight="600" text-anchor="middle">{txt}</text></g>'
                 f'<text x="{cx}" y="{oy+54}" class="m mut" font-size="11" text-anchor="middle">followed the lie: {val}</text>')
    b.append(''.join(g))
    return svg(W, H, ''.join(b), P, title='The Attention Ablation Test')


def ab_design(P, mode):
    W, H = 1200, 430
    b = [frame(W, H, P, 18), corners(W, H, P)]
    b.append(f'<text x="40" y="50" class="m tl" font-size="12" letter-spacing="2.4">DESIGN · 111 FACTS × 9 CONDITIONS = 999 ITEMS PER MODEL · 14 MODELS</text>')
    b.append(f'<text x="40" y="92" class="d ink" font-size="28" font-weight="600">One fact, nine ways to ask it</text>')
    conds = [('BASELINE', 'question alone', 'prior answer', P['muted'], 0, ''),
             ('CONFLICT', '9 lines · early', 'false line', P['red'], 9, 'early'), ('CONFLICT', '9 lines · middle', 'false line', P['red'], 9, 'middle'),
             ('CONFLICT', '9 lines · late', 'false line', P['red'], 9, 'late'),
             ('CONFLICT', '31 lines · early', 'false line', P['red'], 31, 'early'), ('CONFLICT', '31 lines · middle', 'false line', P['red'], 31, 'middle'),
             ('CONFLICT', '31 lines · late', 'false line', P['red'], 31, 'late'),
             ('SUPPORT', '9 lines · middle', 'true line', P['teal'], 9, 'middle'), ('SUPPORT', '31 lines · middle', 'true line', P['teal'], 31, 'middle')]
    cw, gap, x0, y0 = 116, 10, 40, 122
    for i, (k, l1, l2, col, n, where) in enumerate(conds):
        x = x0 + i * (cw + gap)
        b.append(f'<g class="rise" style="animation-delay:{.1+i*.08:.2f}s"><rect x="{x}" y="{y0}" width="{cw}" height="214" rx="10" fill="{P["panel"]}" stroke="{P["line"]}"/>')
        # mini document
        dx, dy, dw = x + 18, y0 + 18, cw - 36
        lines = 9 if n == 9 else (14 if n == 31 else 1)
        pos = {'early': 0, 'middle': lines // 2, 'late': lines - 1}
        hot = pos.get(where)
        lh = 110 / max(lines, 1) if lines > 1 else 0
        if n == 0:
            b.append(f'<rect x="{dx}" y="{dy+50}" width="{dw}" height="10" rx="3" fill="{col}" fill-opacity=".7"/>'
                     f'<text x="{dx+dw/2}" y="{dy+40}" class="m mut" font-size="22" text-anchor="middle">?</text>')
        else:
            for r in range(lines):
                ww = dw * (.6 + .4 * ((r * 37) % 10) / 10)
                c2 = col if r == hot else P['line']
                b.append(f'<rect x="{dx}" y="{dy+r*lh:.1f}" width="{ww:.1f}" height="{max(lh-3,3):.1f}" rx="1.5" fill="{c2}"'
                         + (' class="pulse"' if r == hot else '') + '/>')
        b.append(f'<text x="{x+12}" y="{y0+156}" class="m" font-size="10.5" letter-spacing="1.4" fill="{col}">{k}</text>'
                 f'<text x="{x+12}" y="{y0+178}" class="s ink" font-size="12.5">{e(l1)}</text>'
                 f'<text x="{x+12}" y="{y0+196}" class="s mut" font-size="12">{e(l2)}</text></g>')
    b.append(f'<text x="40" y="{y0+250}" class="s ink" font-size="14.5">A conflict answer is <tspan class="rd" font-weight="600">followed</tspan> if it contains the planted answer and not the true one. Scored automatically, whole-word match.</text>'
             f'<text x="40" y="{y0+274}" class="s mut" font-size="14">Greedy decoding, fp16, 12 new tokens. Two worked examples with invented facts come before every context item.</text>')
    return svg(W, H, ''.join(b), P, title='Design of the context-conflict probe')


def ab_twoprobes(P, mode):
    W, H = 1200, 330
    b = [frame(W, H, P, 18), corners(W, H, P)]
    cards = [('PROBE 1 · FREE RECALL', '200 SimpleQA questions, 2.8B pair', '3 vs 3', 'correct · McNemar p = 1.000 · κ = 0.85',
              'Swapping attention out does not change recall from memory.', P['muted']),
             ('PROBE 2 · CONTEXT CONFLICT', '666 conflict items per model, 14 models', '650 vs 566', 'followed the lie · p = 2.5×10⁻²⁰ (2.8B)',
              'It changes whether a passage can override what the model knows.', P['red'])]
    for i, (k, s1, big, s2, s3, col) in enumerate(cards):
        x = 30 + i * 580
        b.append(f'<g class="rise" style="animation-delay:{.15+i*.25:.2f}s"><rect x="{x}" y="30" width="560" height="270" rx="14" fill="{P["panel"]}" stroke="{P["line"]}"/>'
                 f'<rect x="{x}" y="30" width="560" height="3" rx="1.5" fill="{col}"/>'
                 f'<text x="{x+26}" y="68" class="m" font-size="12" letter-spacing="2" fill="{col}">{k}</text>'
                 f'<text x="{x+26}" y="96" class="s mut" font-size="14.5">{e(s1)}</text>'
                 f'<text x="{x+26}" y="176" class="d" font-size="64" font-weight="600" fill="{col}">{big}</text>'
                 f'<text x="{x+26}" y="208" class="m ink" font-size="12.5">{s2}</text>'
                 f'<path d="M{x+26} 232H{x+534}" stroke="{P["line"]}"/>'
                 f'<text x="{x+26}" y="266" class="s ink" font-size="15">{e(s3)}</text></g>')
    return svg(W, H, ''.join(b), P, title='Two probes, opposite answers')


RDIVS = [('r01', '01', 'The question', 'Is self-attention a separable cause of confident error?', 'red'),
         ('r02', '02', 'Design', 'Five matched pairs, four extra attention models, nine conditions per fact.', 'teal'),
         ('r03', '03', 'Results', 'Free recall does not move. Context conflict splits the architectures.', 'red'),
         ('r04', '04', 'What it means', 'Attention is the machinery that lets an input override stored belief.', 'amber'),
         ('r05', '05', 'Reproduce', 'One 8 GB laptop GPU. Every output and score is in this repository.', 'teal'),
         ('r06', '06', 'Files', 'Where everything lives.', 'amber'),
         ('r07', '07', 'Cite', 'Part of the thesis and of the R1 manuscript.', 'red')]


def ab_footer(P, mode):
    W, H = 1200, 170
    b = [frame(W, H, P, 18), corners(W, H, P)]
    b.append(f'<text x="40" y="66" class="d ink" font-size="24" font-weight="600">Fluent is not the same as true<tspan class="rd">.</tspan></text>'
             f'<text x="40" y="96" class="s mut" font-size="14.5">Md. Rejaul Korim Sadi · Toufiqur Rahman Tasin · Dewan Fahad Chowdhury · supervised by Golam Mostofa Naeem, Lecturer</text>'
             f'<text x="40" y="132" class="m fnt" font-size="11" letter-spacing="1.4">DEPARTMENT OF CSE · METROPOLITAN UNIVERSITY, SYLHET · CODE MIT · DATA CC BY 4.0</text>')
    return svg(W, H, ''.join(b), P, title='Footer')


if __name__ == '__main__':
    write(OUT, 'hero', ab_hero)
    write(OUT, 'design', ab_design)
    write(OUT, 'results', T.studyA)
    write(OUT, 'two_probes', ab_twoprobes)
    write(OUT, 'footer', ab_footer)
    for k, n, l, s, a in RDIVS:
        write(OUT, k, T.divider(n, l, s, a))
