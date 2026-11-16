import sys, math, random
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else '..'
D = 8


# ------------------------------------------------------------ dividers
def divider(num, label, sub, accent='teal'):
    def mk(P, mode):
        W, H = 1200, 104
        lw = width(label, 'Disp', 34, 600)
        b = [f'<text x="4" y="52" class="m" font-size="13" letter-spacing="2.5" fill="{P[accent]}">{num}</text>',
             f'<text x="58" y="56" class="d ink" font-size="34" font-weight="600" letter-spacing="-.5">{e(label)}</text>',
             f'<text x="60" y="88" class="s mut" font-size="15.5">{e(sub)}</text>',
             f'<path d="M{72+lw:.0f} 46H1170" stroke="{P["line"]}"/>',
             f'<path d="M{72+lw:.0f} 46H{140+lw:.0f}" stroke="{P[accent]}" stroke-width="2">'
             + ('' if STATIC else f'<animate attributeName="d" values="M{72+lw:.0f} 46H{140+lw:.0f};M{1102:.0f} 46H1170;M{72+lw:.0f} 46H{140+lw:.0f}" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>')
             + '</path>',
             f'<circle cx="1186" cy="46" r="4" fill="{P[accent]}" class="pulse"/>']
        return svg(W, H, ''.join(b), P, title=f'{num} {label}')
    return mk


DIVS = [
    ('d01', '01', 'The claim', 'Errors are not one thing. Different parts of the machine make them, then hide them.', 'red'),
    ('d02', '02', 'The scan result', 'Three components, three measured roles: one admits the defect, one spreads it, one hides it.', 'teal'),
    ('d03', '03', 'How the scan works', 'Hold everything fixed, change one part, score blind, recompute every number from raw files.', 'amber'),
    ('d04', '04', 'Study A · Attention', 'The Attention Ablation Test: does a false sentence in the input win over what the model knows?', 'red'),
    ('d05', '05', 'Study B · Commitment', 'If you repair the first wrong fact, do the later errors disappear?', 'amber'),
    ('d06', '06', 'Study C · The surface', 'When information is missing, can the user tell the answer is a guess?', 'teal'),
    ('d07', '07', 'How a confident error is assembled', 'The three results, read together as one account.', 'red'),
    ('d08', '08', 'Every number is checked', 'One script reads the released raw files and recomputes 132 reported figures.', 'teal'),
    ('d09', '09', 'Inside this repository', 'One thesis, three studies, every file: what each folder holds.', 'amber'),
    ('d10', '10', 'Reproduce it', 'Two commands on Windows. One 8 GB laptop GPU was enough for the architecture study.', 'teal'),
    ('d11', '11', 'Team and research', 'Built on two first-author manuscripts under review.', 'amber'),
]


# ------------------------------------------------------------ component map
def component_map(P, mode):
    W, H = 1200, 530
    b = [frame(W, H, P, 18), corners(W, H, P)]
    b.append(f'<text x="40" y="52" class="m tl" font-size="12" letter-spacing="2.4">THE SCAN RESULT · COMPONENT MAP OF CONFIDENT ERROR</text>')
    cols = [
        ('CONTEXT MIXING', 'Admits the defect', 'decides whether a false input', 'becomes an output error', P['teal'], 1,
         '650 vs 566', 'false line repeated, of 666 (2.8B pair)', 'STUDY A · ATTENTION ABLATION', 'p = 2.5×10⁻²⁰ · 14 models'),
        ('DECODING COMMITMENT', 'Spreads the defect', 'decides how far a first', 'error travels', P['amber'], 2,
         '92.5% → 48.1%', 'answers with a later error', 'STUDY B · PREFIX REPAIR', 'p = 5.5×10⁻¹² · 3 models'),
        ('OUTPUT SURFACE', 'Hides the defect', 'does not reveal that an', 'answer is a guess', P['red'], 3,
         '75.3%', 'of wrong answers carry no hedge', 'STUDY C · PRE-REGISTERED', 'AUROC 0.56 · 5 models'),
    ]
    cw, gap, x0, y0, ch = 362, 21, 26, 78, 426
    for i, (k, t, l1, l2, col, hi, big, bl, f1, f2) in enumerate(cols):
        x = x0 + i * (cw + gap)
        b.append(f'<g class="rise" style="animation-delay:{.15+i*.2:.2f}s"><rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="14" fill="{P["panel"]}" stroke="{P["line"]}"/>'
                 f'<rect x="{x}" y="{y0}" width="{cw}" height="3" rx="1.5" fill="{col}"/>')
        # mini iso stack
        ox, oy = x + cw / 2, y0 + 40
        S, hh, gp = 92, 15, 13
        layer_cols = [P['faint'], P['faint'], P['faint']]
        for j in range(3):
            z = (2 - j) * (hh + gp)
            lj = 2 - j
        stack = []
        for j in range(3):
            z = j * (hh + gp)
            c = col if (j + 1) == hi else mix(P['faint'], P['bg'], .2)
            stack.append(ibox(ox, oy + 60, 0, 0, z, S, S, hh, c, P))
            if (j + 1) == hi:
                stack.append(f'<path d="{itop(ox, oy+60, 0, 0, z+hh, S, S)}" fill="{P["ink"]}" opacity="0">'
                             + ('' if STATIC else f'<animate attributeName="opacity" values="0;.35;0" dur="2.6s" begin="{i*.8:.1f}s" repeatCount="indefinite"/>') + '</path>')
        if hi == 3:  # output token on top
            stack.append(ibox(ox, oy + 60, 30, 34, 2 * (hh + gp) + hh, 30, 14, 12, P['red'], P, cls='float'))
        if hi == 2:  # first token committing
            stack.append(ibox(ox, oy + 60, 8, 8, 2 * (hh + gp) + hh, 18, 18, 10, P['red'], P))
        b.append(f'<g class="float" style="animation-delay:{i*.7:.1f}s">{"".join(stack)}</g>')
        ty = y0 + 210
        b.append(f'<text x="{x+24}" y="{ty}" class="m" font-size="11.5" letter-spacing="2" fill="{col}">0{i+1} · {k}</text>'
                 f'<text x="{x+24}" y="{ty+34}" class="d ink" font-size="27" font-weight="600">{e(t)}</text>'
                 f'<text x="{x+24}" y="{ty+60}" class="s mut" font-size="14.5">{e(l1)}</text>'
                 f'<text x="{x+24}" y="{ty+79}" class="s mut" font-size="14.5">{e(l2)}</text>'
                 f'<path d="M{x+24} {ty+96}H{x+cw-24}" stroke="{P["line"]}"/>'
                 f'<text x="{x+24}" y="{ty+136}" class="d" font-size="34" font-weight="600" fill="{col}">{e(big)}</text>'
                 f'<text x="{x+24}" y="{ty+158}" class="s ink" font-size="13.5">{e(bl)}</text>'
                 f'<text x="{x+24}" y="{y0+ch-34}" class="m fnt" font-size="10.5" letter-spacing="1">{e(f1)}</text>'
                 f'<text x="{x+24}" y="{y0+ch-16}" class="m mut" font-size="11">{e(f2)}</text></g>')
    b.append(sweep(W, H, P, 18, 10))
    return svg(W, H, ''.join(b), P, title='Component map of confident error')


# ------------------------------------------------------------ method
def method(P, mode):
    W, H = 1200, 300
    b = [frame(W, H, P, 18)]
    steps = [('HOLD FIXED', 'Same data, tokenizer', 'and scale on both sides', P['teal']),
             ('CHANGE ONE PART', 'Swap the mixer, repair one', 'fact, or remove one word', P['amber']),
             ('SCORE BLIND, TWICE', 'Two raters, model hidden;', 'κ = 0.85 to 1.00', P['red']),
             ('RECOMPUTE', 'One script, raw files in,', '132 / 132 numbers match', P['blue'])]
    cw, gap, x0, y0 = 252, 30, 40, 64
    b.append(f'<text x="40" y="44" class="m mut" font-size="11.5" letter-spacing="2.2">PROTOCOL · ONE INTERVENTION AND ONE FALSIFIABLE PREDICTION PER COMPONENT</text>')
    for i, (k, l1, l2, col) in enumerate(steps):
        x = x0 + i * (cw + gap)
        b.append(f'<g class="rise" style="animation-delay:{.1+i*.18:.2f}s"><rect x="{x}" y="{y0}" width="{cw}" height="196" rx="12" fill="{P["panel"]}" stroke="{P["line"]}"/>'
                 f'<circle cx="{x+36}" cy="{y0+40}" r="18" fill="{col}" fill-opacity=".12" stroke="{col}"/>'
                 f'<text x="{x+36}" y="{y0+45}" class="m" font-size="14" font-weight="600" text-anchor="middle" fill="{col}">{i+1}</text>')
        ix, iy = x + 150, y0 + 42
        if i == 0:  # two locked blocks
            b.append(ibox(ix - 40, iy - 18, 0, 0, 0, 34, 34, 22, P['teal'], P) + ibox(ix + 40, iy - 18, 0, 0, 0, 34, 34, 22, P['teal'], P)
                     + f'<path d="M{ix-12} {iy+4}H{ix+12}" stroke="{col}" stroke-width="2" stroke-dasharray="3 3"/><text x="{ix}" y="{iy-2}" class="m" font-size="11" text-anchor="middle" fill="{col}">=</text>')
        if i == 1:  # swap arrows
            b.append(ibox(ix - 6, iy - 18, 0, 0, 0, 34, 34, 22, P['amber'], P)
                     + f'<path d="M{ix-60} {iy-6}C{ix-40} {iy-30} {ix-20} {iy-30} {ix-8} {iy-14}" stroke="{col}" stroke-width="1.6" fill="none" stroke-dasharray="4 4">'
                     + ('' if STATIC else '<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.2s" repeatCount="indefinite"/>') + '</path>')
        if i == 2:  # two eyes
            for dx in (-26, 26):
                b.append(f'<ellipse cx="{ix+dx}" cy="{iy}" rx="20" ry="11" fill="none" stroke="{col}" stroke-width="1.6"/>'
                         f'<circle cx="{ix+dx}" cy="{iy}" r="5" fill="{col}">' + ('' if STATIC else f'<animate attributeName="cx" values="{ix+dx-7};{ix+dx+7};{ix+dx-7}" dur="3s" repeatCount="indefinite"/>') + '</circle>')
        if i == 3:  # check ring
            c = 2 * math.pi * 20
            b.append(f'<circle cx="{ix}" cy="{iy}" r="20" fill="none" stroke="{P["line"]}" stroke-width="5"/>'
                     f'<circle cx="{ix}" cy="{iy}" r="20" fill="none" stroke="{col}" stroke-width="5" stroke-dasharray="{c:.1f} {c:.1f}" transform="rotate(-90 {ix} {iy})">'
                     + ('' if STATIC else f'<animate attributeName="stroke-dasharray" values="0 {c:.1f};{c:.1f} {c:.1f};{c:.1f} {c:.1f}" keyTimes="0;.4;1" dur="4s" repeatCount="indefinite"/>') + '</circle>'
                     f'<path d="M{ix-8} {iy}L{ix-2} {iy+6}L{ix+9} {iy-6}" stroke="{col}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
        b.append(f'<text x="{x+22}" y="{y0+112}" class="m" font-size="12" letter-spacing="1.8" fill="{col}">{k}</text>'
                 f'<text x="{x+22}" y="{y0+142}" class="s ink" font-size="15">{e(l1)}</text>'
                 f'<text x="{x+22}" y="{y0+164}" class="s mut" font-size="15">{e(l2)}</text></g>')
        if i < 3:
            b.append(f'<g>{arrow(x+cw+6, y0+98, x+cw+gap-6, P["faint"], 1.4)}</g>')
    return svg(W, H, ''.join(b), P, title='How the scan works')


# ------------------------------------------------------------ study A
PAIRS = [('160M', '130M', 312, 271, 'p = 0.014', 'mixed'), ('410M', '370M', 646, 427, 'p = 5.3×10⁻⁵⁶', ''),
         ('1B', '790M', 653, 542, 'p = 3.2×10⁻³¹', ''), ('1.4B', '1.4B', 648, 186, 'p = 1.7×10⁻¹³⁹', ''),
         ('2.8B', '2.8B', 650, 566, 'p = 2.5×10⁻²⁰', '')]


def studyA(P, mode, title_txt=True):
    W, H = 1200, 600
    b = [frame(W, H, P, 18), corners(W, H, P)]
    b.append(f'<text x="40" y="52" class="m rd" font-size="12" letter-spacing="2.4">STUDY A · SAME DATA · SAME TOKENIZER · SAME SCALE · ONLY THE MIXER CHANGES</text>')
    b.append(f'<text x="40" y="96" class="d ink" font-size="30" font-weight="600">A planted false line, 666 chances per model</text>')
    b.append(f'<text x="40" y="122" class="s mut" font-size="15">How often each model repeated the false statement instead of what it knew. Five matched pairs, 130M to 2.8B.</text>')
    # legend
    b.append(f'<rect x="40" y="142" width="12" height="12" rx="2" class="rd"/><text x="58" y="153" class="m ink" font-size="12">Pythia · attention</text>'
             f'<rect x="200" y="142" width="12" height="12" rx="2" class="tl"/><text x="218" y="153" class="m ink" font-size="12">Mamba · state space</text>')
    x0, bw, y = 130, 500, 186
    for i, (pa, ma, a, s_, pv, tag) in enumerate(PAIRS):
        yy = y + i * 68
        b.append(f'<text x="40" y="{yy+16}" class="m ink" font-size="13" font-weight="600">{pa}</text><text x="40" y="{yy+34}" class="m fnt" font-size="11">vs {ma}</text>')
        for k, (v, col, cls) in enumerate(((a, P['red'], 'rd'), (s_, P['teal'], 'tl'))):
            ry = yy + k * 20
            fw = bw * v / 666
            b.append(f'<rect x="{x0}" y="{ry}" width="{bw}" height="14" rx="4" fill="{P["line"]}" fill-opacity=".55"/>'
                     f'<rect x="{x0}" y="{ry}" width="{fw:.1f}" height="14" rx="4" fill="{col}">' + ('' if STATIC else grow_w(fw, .2 + i * .15 + k * .1, D)) + '</rect>'
                     f'<text x="{x0+bw+12}" y="{ry+12}" class="m {cls}" font-size="13" font-weight="600">{v}</text>')
        b.append(f'<text x="{x0+bw+58}" y="{yy+21}" class="m mut" font-size="11.5">{pv}</text>')
        if tag:
            b.append(f'<text x="{x0+bw+58}" y="{yy+36}" class="m fnt" font-size="10">reverses on known facts</text>')
    # right panel: three proofs
    px, pw = 900, 270
    tiles = [('FREE RECALL · 200 SIMPLEQA', '3 vs 3', 'correct, 2.8B pair · p = 1.000', P['muted'], 'memory unchanged'),
             ('ON FACTS BOTH MODELS KNEW', '264 vs 210', 'of 279 · p = 9.0×10⁻¹³', P['red'], 'not a knowledge gap'),
             ('PLANTED TRUE LINE (CONTROL)', '111 vs 110', 'of 111 read correctly', P['teal'], 'both can read context')]
    for i, (k, big, s1, col, s2) in enumerate(tiles):
        ty = 142 + i * 132
        b.append(f'<g class="rise" style="animation-delay:{.4+i*.2:.1f}s"><rect x="{px}" y="{ty}" width="{pw}" height="118" rx="12" fill="{P["panel"]}" stroke="{P["line"]}"/>'
                 f'<text x="{px+18}" y="{ty+26}" class="m mut" font-size="10.5" letter-spacing="1.2">{k}</text>'
                 f'<text x="{px+18}" y="{ty+64}" class="d" font-size="32" font-weight="600" fill="{col}">{big}</text>'
                 f'<text x="{px+18}" y="{ty+86}" class="m ink" font-size="11.5">{e(s1)}</text>'
                 f'<text x="{px+18}" y="{ty+104}" class="s mut" font-size="12.5" font-style="italic">{e(s2)}</text></g>')
    b.append(f'<path d="M40 {H-58}H{W-40}" stroke="{P["line"]}"/>')
    b.append(f'<text x="40" y="{H-26}" class="s ink" font-size="15">From 410M up, <tspan class="rd" font-weight="600">every</tspan> attention model repeats the falsehood more often. At 1.4B the split is <tspan class="rd" font-weight="600">462 items to 0</tspan>.</text>')
    b.append(sweep(W, H, P, 18, 11, 1))
    return svg(W, H, ''.join(b), P, title='Study A results')


# ------------------------------------------------------------ study B
def studyB(P, mode):
    W, H = 1200, 600
    b = [frame(W, H, P, 18), corners(W, H, P)]
    b.append(f'<text x="40" y="52" class="m am" font-size="12" letter-spacing="2.4">STUDY B · 111 WRONG ANSWERS · GPT-OSS-120B · QWEN3.6-27B · ALLAM-2-7B</text>')
    b.append(f'<text x="40" y="96" class="d ink" font-size="30" font-weight="600">Repair the first wrong fact, then let it keep writing</text>')
    # schematic chain (illustration)
    b.append(f'<text x="40" y="130" class="m fnt" font-size="10.5" letter-spacing="1.4">SCHEMATIC · ONE ANSWER, FOUR CLAIMS</text>')
    rows = [('AS GENERATED', ['claim 1 ✗', 'claim 2 ✗', 'claim 3 ✗', 'claim 4 ✗'], ['r', 'r', 'r', 'r']),
            ('FIRST FACT → CORRECT', ['claim 1 ✓', 'claim 2 ✓', 'claim 3 ✗', 'claim 4 ✓'], ['t', 't', 'r', 't']),
            ('FIRST FACT → OTHER WRONG', ['claim 1 ✗', 'claim 2 ✓', 'claim 3 ✓', 'claim 4 ✗'], ['a', 't', 't', 'r'])]
    cmap = {'r': P['red'], 't': P['teal'], 'a': P['amber']}
    for ri, (lab, toks, cs) in enumerate(rows):
        yy = 150 + ri * 50
        b.append(f'<text x="40" y="{yy+20}" class="m mut" font-size="11" letter-spacing="1">{lab}</text>')
        x = 250
        for j, (t, c) in enumerate(zip(toks, cs)):
            col = cmap[c]
            w = 104
            first = j == 0 and ri > 0
            anim = '' if STATIC else f' style="opacity:0;animation:chain 8s {ri*1.2+j*.25:.2f}s infinite"'
            b.append(f'<g{anim}><rect x="{x}" y="{yy}" width="{w}" height="30" rx="7" fill="{col}" fill-opacity=".12" stroke="{col}"{" stroke-width=\"2\"" if first else ""}/>'
                     f'<text x="{x+w/2}" y="{yy+20}" class="m" font-size="12.5" text-anchor="middle" fill="{col}">{t}</text></g>')
            if j < 3:
                b.append(arrow(x + w + 4, yy + 15, x + w + 22, P['faint'], 1.2))
            x += w + 26
    b.append(f'<text x="790" y="170" class="s mut" font-size="13.5">Later claims are <tspan class="ink" font-weight="600">elaborations</tspan></text>'
             f'<text x="790" y="190" class="s mut" font-size="13.5">of whatever was committed first.</text>'
             f'<text x="790" y="226" class="s mut" font-size="13.5">Replace that claim with <tspan class="ink" font-weight="600">anything</tspan>,</text>'
             f'<text x="790" y="246" class="s mut" font-size="13.5">even another wrong fact, and about</text>'
             f'<text x="790" y="266" class="s mut" font-size="13.5">half of the later errors disappear.</text>')
    # bars
    def hbar(x, y, w, frac, col, lab, val, delay, cls):
        fw = w * frac
        return (f'<text x="{x}" y="{y}" class="s ink" font-size="14.5">{e(lab)}</text>'
                f'<text x="{x+w}" y="{y+2}" class="d {cls}" font-size="28" font-weight="600" text-anchor="end">{e(val)}</text>'
                f'<rect x="{x}" y="{y+12}" width="{w}" height="14" rx="4" fill="{P["line"]}" fill-opacity=".6"/>'
                f'<rect x="{x}" y="{y+12}" width="{fw:.1f}" height="14" rx="4" fill="{col}">' + ('' if STATIC else grow_w(fw, delay, D)) + '</rect>')
    b.append(hbar(40, 340, 500, .925, P['red'], 'Answers with a later error, as generated', '92.5%', .3, 'rd'))
    b.append(hbar(40, 406, 500, .481, P['teal'], 'After repairing only the first wrong fact', '48.1%', .8, 'tl'))
    b.append(f'<text x="40" y="468" class="m mut" font-size="12">n = 106 paired · 50 fixed, 3 broken · exact McNemar p = 5.5×10⁻¹²</text>'
             f'<text x="40" y="488" class="m mut" font-size="12">second annotator: 97.2% → 50.0% · κ = 0.94</text>')
    # control tile
    b.append(f'<g class="rise" style="animation-delay:.6s"><rect x="590" y="318" width="270" height="180" rx="12" fill="{P["panel"]}" stroke="{P["line"]}"/>'
             f'<text x="608" y="344" class="m mut" font-size="10.5" letter-spacing="1.2">CONTROL · ERROR-FREE AFTERWARDS</text>'
             f'<text x="608" y="390" class="d tl" font-size="30" font-weight="600">54.6%</text><text x="720" y="390" class="s mut" font-size="13">correct fact</text>'
             f'<text x="608" y="434" class="d am" font-size="30" font-weight="600">60.8%</text><text x="720" y="434" class="s mut" font-size="13">different wrong fact</text>'
             f'<text x="608" y="476" class="m ink" font-size="11.5">n = 97 · p = 0.38 · no advantage</text></g>')
    # 111 dots: knew alone
    gx, gy = 890, 330
    b.append(f'<text x="{gx}" y="{gy-12}" class="m mut" font-size="10.5" letter-spacing="1.2">ANSWERED CORRECTLY WHEN ASKED ALONE</text>')
    k = 0
    for r in range(8):
        for c in range(14):
            if k >= 111:
                break
            lit = k in (37, 88)
            col = P['amber'] if lit else P['line']
            b.append(f'<circle cx="{gx+8+c*19}" cy="{gy+12+r*19}" r="6" fill="{col}"' + (' class="pulse"' if lit else '') + '/>')
            k += 1
    b.append(f'<text x="{gx}" y="{gy+178}" class="d am" font-size="22" font-weight="600">2 of 111</text>'
             f'<text x="{gx+100}" y="{gy+178}" class="s mut" font-size="13">the truth was not hiding</text>')
    b.append(f'<path d="M40 {H-58}H{W-40}" stroke="{P["line"]}"/>')
    b.append(f'<text x="40" y="{H-28}" class="s ink" font-size="15">Decoding commitment decides <tspan class="am" font-weight="600">how far</tspan> an error spreads. The model elaborates its own claim; it was not suppressing a truth it knew.</text>')
    css = '@keyframes chain{0%{opacity:0;transform:translateX(-6px)}6%{opacity:1;transform:none}88%{opacity:1}96%,100%{opacity:0}}'
    b.append(sweep(W, H, P, 18, 12, 2))
    return svg(W, H, ''.join(b), P, defs=f'<style>{css}</style>', title='Study B results')


# ------------------------------------------------------------ study C
def studyC(P, mode):
    W, H = 1200, 560
    b = [frame(W, H, P, 18), corners(W, H, P)]
    b.append(f'<text x="40" y="52" class="m tl" font-size="12" letter-spacing="2.4">STUDY C · PRE-REGISTERED (OSF CS967) · 5 MODELS · 5,620 RESPONSES · BLIND, DOUBLE-SCORED</text>')
    b.append(f'<text x="40" y="96" class="d ink" font-size="30" font-weight="600">Remove one word. The error rises. The tone does not.</text>')
    # example
    b.append(f'<rect x="40" y="118" width="560" height="64" rx="10" fill="{P["panel"]}" stroke="{P["line"]}"/>'
             f'<text x="58" y="143" class="m mut" font-size="12">"Of which tribe of Red Indians was <tspan class="tl">Geronimo</tspan> a chief?"</text>'
             f'<text x="58" y="167" class="m mut" font-size="12">"Of which tribe was <tspan class="rd">this chief</tspan>?"  same answer key</text>')

    def hbar(x, y, w, frac, col, lab, val, delay, cls):
        fw = w * frac
        return (f'<text x="{x}" y="{y}" class="s ink" font-size="14.5">{e(lab)}</text>'
                f'<text x="{x+w}" y="{y+2}" class="d {cls}" font-size="28" font-weight="600" text-anchor="end">{e(val)}</text>'
                f'<rect x="{x}" y="{y+12}" width="{w}" height="14" rx="4" fill="{P["line"]}" fill-opacity=".6"/>'
                f'<rect x="{x}" y="{y+12}" width="{fw:.1f}" height="14" rx="4" fill="{col}">' + ('' if STATIC else grow_w(fw, delay, D)) + '</rect>')
    b.append(hbar(40, 222, 560, .391, P['amber'], 'Error among attempted answers, question intact', '39.1%', .3, 'am'))
    b.append(hbar(40, 288, 560, .52, P['red'], 'Error with the referent removed', '52.0%', .8, 'rd'))
    b.append(f'<text x="40" y="350" class="m mut" font-size="12">mixed-effects OR 4.12 (95% CI 2.76–6.14) · p = 4.0×10⁻¹² · asked for clarification on 33.7%</text>')
    # identity lengths
    b.append(f'<text x="40" y="384" class="m mut" font-size="10.5" letter-spacing="1.2">SAME 50 QUESTIONS · WHO THE USER CLAIMS TO BE · MEAN WORDS</text>')
    ids = [('anonymous', 188), ('patient', 259), ('physician', 268), ('researcher', 268)]
    for i, (n, v) in enumerate(ids):
        x = 40 + i * 140
        hgt = 80 * v / 268
        yb = 500
        col = P['muted'] if i == 0 else P['blue']
        b.append(f'<rect x="{x}" y="{yb-hgt:.1f}" width="96" height="{hgt:.1f}" rx="5" fill="{col}" fill-opacity=".85">' + ('' if STATIC else grow_h(hgt, yb, .4 + i * .15, D)) + '</rect>'
                 f'<text x="{x+48}" y="{yb-hgt-8:.1f}" class="m ink" font-size="12.5" text-anchor="middle">{v}</text>'
                 f'<text x="{x+48}" y="{yb+20}" class="m mut" font-size="11.5" text-anchor="middle">{n}</text>')
    # donut 75.3
    cx, cy, r = 820, 260, 88
    c = 2 * math.pi * r
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["line"]}" stroke-width="22"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["red"]}" stroke-width="22" stroke-dasharray="{c*.753:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})">'
             + ('' if STATIC else f'<animate attributeName="stroke-dasharray" values="0 {c:.1f};{c*.753:.1f} {c:.1f};{c*.753:.1f} {c:.1f};0 {c:.1f}" keyTimes="0;.25;.86;1" dur="{D}s" begin=".5s" repeatCount="indefinite"/>') + '</circle>'
             f'<circle cx="{cx}" cy="{cy}" r="{r+22}" fill="none" stroke="{P["red"]}" stroke-opacity=".35" stroke-dasharray="2 7">'
             + ('' if STATIC else f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="18s" repeatCount="indefinite"/>') + '</circle>'
             f'<text x="{cx}" y="{cy+10}" class="d ink" font-size="38" font-weight="600" text-anchor="middle">75.3%</text>'
             f'<text x="{cx}" y="{cy+r+52}" class="s ink" font-size="15" text-anchor="middle">of wrong answers carried</text>'
             f'<text x="{cx}" y="{cy+r+72}" class="s ink" font-size="15" text-anchor="middle">no hedge at all</text>')
    # AUROC gauge
    gx, gy, gs = 960, 150, 200
    b.append(f'<rect x="{gx}" y="{gy}" width="{gs}" height="{gs}" rx="8" fill="{P["panel"]}" stroke="{P["line"]}"/>'
             f'<path d="M{gx} {gy+gs}L{gx+gs} {gy}" stroke="{P["faint"]}" stroke-dasharray="4 4"/>')
    # ROC curve for AUC ~0.56: y = x^0.78 approx (AUC = 1/(1+0.78)=0.562)
    pts = ' L'.join(f'{gx+gs*t:.1f} {gy+gs-gs*(t**0.78):.1f}' for t in [i / 40 for i in range(41)])
    L = 320
    b.append(f'<path d="M{pts}" stroke="{P["red"]}" stroke-width="2.4" fill="none" stroke-dasharray="{L} {L}">'
             + ('' if STATIC else f'<animate attributeName="stroke-dashoffset" values="{L};0;0;{L}" keyTimes="0;.3;.86;1" dur="{D}s" repeatCount="indefinite"/>') + '</path>'
             f'<text x="{gx+gs/2}" y="{gy+gs+30}" class="d rd" font-size="26" font-weight="600" text-anchor="middle">AUROC 0.56</text>'
             f'<text x="{gx+gs/2}" y="{gy+gs+50}" class="s mut" font-size="12.5" text-anchor="middle">hedging as a warning sign</text>'
             f'<text x="{gx+gs/2}" y="{gy+gs+67}" class="s mut" font-size="12.5" text-anchor="middle">(dashed line = coin flip)</text>'
             f'<text x="{gx+8}" y="{gy+18}" class="m fnt" font-size="10">illustrative curve</text>')
    b.append(f'<path d="M700 470H{W-40}" stroke="{P["line"]}"/>'
             f'<text x="700" y="500" class="s ink" font-size="15">When information is missing, models usually <tspan class="rd" font-weight="600">guess</tspan>.</text>'
             f'<text x="700" y="522" class="s mut" font-size="15">The wording barely changes, so the user cannot see it.</text>')
    b.append(sweep(W, H, P, 18, 11, 3))
    return svg(W, H, ''.join(b), P, title='Study C results')


# ------------------------------------------------------------ assembly line
def assembly(P, mode):
    W, H = 1200, 340
    b = [frame(W, H, P, 18), corners(W, H, P)]
    stages = [('INPUT', 'A false sentence,', 'or missing knowledge', P['muted']),
              ('CONTEXT MIXING', 'Attention lets the', 'false input win', P['teal']),
              ('DECODING', 'Commits to the first', 'claim, elaborates it', P['amber']),
              ('OUTPUT SURFACE', 'Same fluent tone;', 'no cue to doubt it', P['red']),
              ('THE USER', 'Receives a confident,', 'fluent, false answer', P['ink'])]
    x0, cw, gap, y0 = 34, 204, 30, 100
    path_y = y0 + 52
    track_y = 80
    b.append(f'<text x="34" y="50" class="m mut" font-size="11.5" letter-spacing="2.2">SYNTHESIS · ONE PART ADMITS THE DEFECT, ONE SPREADS IT, ONE HIDES IT</text>')
    b.append(f'<path id="ap" d="M{x0+cw/2} {track_y}H{x0+4*(cw+gap)+cw/2}" stroke="{P["line"]}" stroke-width="2" stroke-dasharray="3 6" fill="none"/>'
             + ''.join(f'<path d="M{x0+i*(cw+gap)+cw/2} {track_y}V{y0}" stroke="{P["line"]}" stroke-width="1.4"/>' for i in range(5)))
    for i, (k, l1, l2, col) in enumerate(stages):
        x = x0 + i * (cw + gap)
        b.append(f'<g class="rise" style="animation-delay:{.1+i*.15:.2f}s"><rect x="{x}" y="{y0}" width="{cw}" height="196" rx="12" fill="{P["panel"]}" stroke="{P["line"]}"/>'
                 f'<rect x="{x+cw/2-22}" y="{path_y-22}" width="44" height="44" rx="10" fill="{P["panel"]}"/><rect x="{x+cw/2-22}" y="{path_y-22}" width="44" height="44" rx="10" fill="{col}" fill-opacity=".12" stroke="{col}"/>'
                 f'<text x="{x+cw/2}" y="{path_y+5}" class="m" font-size="13" font-weight="600" text-anchor="middle" fill="{col}">{i+1}</text>'
                 f'<text x="{x+cw/2}" y="{y0+120}" class="m" font-size="11.5" letter-spacing="1.6" text-anchor="middle" fill="{col}">{k}</text>'
                 f'<text x="{x+cw/2}" y="{y0+148}" class="s ink" font-size="14" text-anchor="middle">{e(l1)}</text>'
                 f'<text x="{x+cw/2}" y="{y0+168}" class="s mut" font-size="14" text-anchor="middle">{e(l2)}</text></g>')
    if not STATIC:
        b.append(f'<circle r="7" fill="{P["red"]}"><animateMotion dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"><mpath href="#ap" xlink:href="#ap"/></animateMotion>'
                 f'<animate attributeName="r" values="5;8;5" dur="1s" repeatCount="indefinite"/></circle>')
    b.append(f'<text x="40" y="{H-22}" class="s mut" font-size="13.5">Different components produce the error, but they combine into the same confident surface. That is why hallucination looks uniform from outside.</text>')
    return svg(W, H, ''.join(b), P, title='How a confident hallucination is assembled')


# ------------------------------------------------------------ verification terminal
LEDGER = [('A', 'Free recall: Cohen\'s kappa', '0.85'), ('A', 'Conflict items followed, pythia-2.8b', '650'),
          ('A', 'Conflict items followed, mamba-2.8b-hf', '566'), ('A', '2.8B McNemar p (x1e-20)', '2.5'),
          ('A', '1.4B discordant (attention only)', '462'), ('A', '2.8B known facts, Pythia followed', '264'),
          ('A', '2.8B known facts, Mamba followed', '210'), ('A', 'Group Mann-Whitney p', '0.007'),
          ('B', 'Kappa, downstream error', '0.94'), ('B', 'Downstream error before repair (%)', '92.5'),
          ('B', 'Downstream error after repair (%)', '48.1'), ('B', 'Repair McNemar p (x1e-12)', '5.5'),
          ('B', 'Correct in isolation (of 111)', '2'), ('B', 'Correct vs wrong fact McNemar p', '0.38'),
          ('C', 'Responses in the scoring sheets', '5620'), ('C', 'Mean answer length, physician', '268')]


def verify(P, mode):
    W, H = 1200, 400
    b = [frame(W, H, P, 18)]
    tx, ty, tw, th = 30, 30, 760, 340
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{P["panel"]}" stroke="{P["line"]}"/>'
             f'<path d="M{tx} {ty+34}H{tx+tw}" stroke="{P["line"]}"/>'
             + ''.join(f'<circle cx="{tx+20+i*16}" cy="{ty+17}" r="5" fill="{c}"/>' for i, c in enumerate((P['red'], P['amber'], P['teal'])))
             + f'<text x="{tx+80}" y="{ty+21}" class="m mut" font-size="11.5">py verification/verify_thesis_numbers.py</text>')
    b.append(f'<clipPath id="term"><rect x="{tx+1}" y="{ty+40}" width="{tw-2}" height="{th-80}"/></clipPath>')
    rows = []
    rh = 22
    for i, (s, cl, v) in enumerate(LEDGER * 2):
        y = ty + 62 + i * rh
        col = {'A': P['red'], 'B': P['amber'], 'C': P['teal']}[s]
        rows.append(f'<text x="{tx+18}" y="{y}" class="m" font-size="12" fill="{col}">{s}</text>'
                    f'<text x="{tx+44}" y="{y}" class="m ink" font-size="12">{e(cl)}</text>'
                    f'<text x="{tx+520}" y="{y}" class="m mut" font-size="12" text-anchor="end">{v}</text>'
                    f'<text x="{tx+600}" y="{y}" class="m mut" font-size="12" text-anchor="end">{v}</text>'
                    f'<text x="{tx+tw-24}" y="{y}" class="m tl" font-size="12" font-weight="600" text-anchor="end">PASS</text>')
    shift = len(LEDGER) * rh
    anim = '' if STATIC else f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -{shift}" dur="16s" repeatCount="indefinite"/>'
    b.append(f'<g clip-path="url(#term)"><g>{"".join(rows)}{anim}</g></g>')
    b.append(f'<path d="M{tx} {ty+th-40}H{tx+tw}" stroke="{P["line"]}"/>'
             f'<text x="{tx+18}" y="{ty+th-15}" class="m ink" font-size="12.5">132 checks, <tspan class="tl" font-weight="600">132 passed</tspan>, 0 failed<tspan class="tl blink"> ▌</tspan></text>')
    # right summary
    cx, cy, r = 990, 170, 92
    c = 2 * math.pi * r
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["line"]}" stroke-width="14"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["teal"]}" stroke-width="14" stroke-dasharray="{c:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})">'
             + ('' if STATIC else f'<animate attributeName="stroke-dasharray" values="0 {c:.1f};{c:.1f} {c:.1f};{c:.1f} {c:.1f}" keyTimes="0;.5;1" dur="6s" repeatCount="indefinite"/>') + '</circle>'
             f'<text x="{cx}" y="{cy+4}" class="d ink" font-size="40" font-weight="600" text-anchor="middle">132</text>'
             f'<text x="{cx}" y="{cy+30}" class="m tl" font-size="12" letter-spacing="2" text-anchor="middle">OF 132 MATCH</text>'
             f'<text x="{cx}" y="{cy+r+48}" class="s ink" font-size="14.5" text-anchor="middle">Raw files in. Thesis numbers out.</text>'
             f'<text x="{cx}" y="{cy+r+70}" class="s mut" font-size="13" text-anchor="middle">Studies A and B recomputed in full;</text>'
             f'<text x="{cx}" y="{cy+r+88}" class="s mut" font-size="13" text-anchor="middle">Study C as far as the sheets allow.</text>')
    return svg(W, H, ''.join(b), P, title='Verification: 132 of 132 numbers match')


# ------------------------------------------------------------ team footer
def team(P, mode):
    W, H = 1200, 250
    b = [frame(W, H, P, 18), corners(W, H, P)]
    ppl = [('Md. Rejaul Korim Sadi', 'ID 231-115-349', P['teal']), ('Toufiqur Rahman Tasin', 'ID 231-115-345', P['amber']),
           ('Dewan Fahad Chowdhury', 'ID 231-115-268', P['red'])]
    for i, (n, idn, col) in enumerate(ppl):
        x = 40 + i * 290
        b.append(f'<g class="rise" style="animation-delay:{.1+i*.15:.2f}s"><circle cx="{x+22}" cy="72" r="22" fill="{col}" fill-opacity=".12" stroke="{col}"/>'
                 f'<text x="{x+22}" y="78" class="d" font-size="18" font-weight="600" text-anchor="middle" fill="{col}">{n.split()[-1][0] if i else "S"}</text>'
                 f'<text x="{x+56}" y="68" class="s ink" font-size="15.5" font-weight="600">{e(n)}</text>'
                 f'<text x="{x+56}" y="88" class="m mut" font-size="11.5">{idn}</text></g>')
    b.append(f'<g class="rise" style="animation-delay:.6s"><text x="910" y="64" class="m fnt" font-size="10.5" letter-spacing="1.4">SUPERVISOR</text>'
             f'<text x="910" y="86" class="s ink" font-size="15.5" font-weight="600">Golam Mostofa Naeem</text>'
             f'<text x="910" y="104" class="s mut" font-size="12.5">Lecturer, Department of CSE</text></g>')
    b.append(f'<path d="M40 136H{W-40}" stroke="{P["line"]}"/>')
    b.append(f'<text x="40" y="172" class="d ink" font-size="20" font-weight="600">Department of Computer Science and Engineering · Metropolitan University, Sylhet</text>')
    b.append(f'<text x="40" y="206" class="m fnt" font-size="11" letter-spacing="1.4">DATA CC BY 4.0 · CODE MIT · B.SC. THESIS · NOVEMBER 2026</text>')
    b.append(f'<text x="{W-40}" y="206" class="m rd" font-size="11" letter-spacing="1.4" text-anchor="end">FLUENT IS NOT THE SAME AS TRUE.</text>')
    return svg(W, H, ''.join(b), P, title='Team')


# ------------------------------------------------------------ atlas
def atlas(P, mode):
    W, H = 1200, 566
    b = [frame(W, H, P, 18), corners(W, H, P)]
    rows = [
        ('thesis/', 'The thesis: 37-page PDF and its LaTeX source', '37 pages', P['red']),
        ('evidence/study_A_attention_ablation/', 'Study A · The Attention Ablation Test', '14 models', P['teal']),
        ('evidence/study_B_commitment_repair/', 'Study B · Repairing the first wrong fact', '111 answers', P['amber']),
        ('evidence/study_C_confidence_and_identity/', 'Study C · Guessing when information is missing', '5,620 responses', P['blue']),
        ('evidence/introduction_example/', 'The GPT-2 "the late Paul Graham" example', '15 prompts', P['red']),
        ('verification/', 'One script recomputes every reported number', '132 / 132', P['teal']),
        ('docs/  ·  assets/', 'Website, two 3D models and all page artwork', 'live site', P['amber']),
    ]
    n = len(rows)
    b.append(f'<text x="310" y="58" class="m tl" font-size="12" letter-spacing="2.4">REPOSITORY ATLAS · ONE THESIS, THREE STUDIES, EVERY FILE</text>')
    S, hh, dz = 90, 14, 60
    ox, oy = 168, 434 + (n - 7) * 0
    cy0, rh = 112, 60
    cyc = 0.9 * n
    stack = []
    for i in reversed(range(n)):
        col = rows[i][3]
        z = (n - 1 - i) * dz
        stack.append(ibox(ox, oy, 0, 0, z, S, S, hh, col, P))
        anim = '' if STATIC else f'<animate attributeName="opacity" values="0;0;.55;0;0" keyTimes="0;{i/n:.3f};{(i+.5)/n:.3f};{(i+1)/n:.3f};1" dur="{cyc:.1f}s" repeatCount="indefinite"/>'
        stack.append(f'<path d="{itop(ox, oy, 0, 0, z+hh, S, S)}" fill="{P["ink"]}" opacity="0">{anim}</path>')
    b.append(f'<g class="float">{"".join(stack)}</g>')
    xr = ox + S * C30
    for i, (path, desc, stat, col) in enumerate(rows):
        cy = cy0 + i * rh
        z = (n - 1 - i) * dz
        py = oy + S * S30 - z - hh / 2
        ranim = '' if STATIC else f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{i/n:.3f};{(i+.5)/n:.3f};{(i+1)/n:.3f};1" dur="{cyc:.1f}s" repeatCount="indefinite"/>'
        b.append(f'<g class="rise" style="animation-delay:{.1+i*.12:.2f}s">'
                 f'<rect x="296" y="{cy-27}" width="{W-326}" height="54" rx="10" fill="{P["panel2"]}" opacity="0">{ranim}</rect>'
                 f'<path d="M{xr+6:.1f} {py:.1f}H286" stroke="{col}" stroke-width="1.2" stroke-dasharray="3 4" opacity=".8"/>'
                 f'<circle cx="{xr+6:.1f}" cy="{py:.1f}" r="3" fill="{col}"/>'
                 f'<rect x="306" y="{cy-5}" width="10" height="10" rx="2" fill="{col}"/>'
                 f'<text x="330" y="{cy-4}" class="m" font-size="12.5" fill="{col}">{e(path)}</text>'
                 f'<text x="330" y="{cy+17}" class="s mut" font-size="14.5">{e(desc)}</text>'
                 f'<text x="{W-44}" y="{cy+8}" class="d" font-size="22" font-weight="600" text-anchor="end" fill="{col}">{e(stat)}</text>'
                 + (f'<path d="M296 {cy+30}H{W-30}" stroke="{P["line"]}"/>' if i < n - 1 else '') + '</g>')
    return svg(W, H, ''.join(b), P, title='Repository atlas')


if __name__ == '__main__':
    for k, n, l, s, a in DIVS:
        write(OUT, k, divider(n, l, s, a))
    write(OUT, 'component_map', component_map)
    write(OUT, 'method', method)
    write(OUT, 'study_a', studyA)
    write(OUT, 'study_b', studyB)
    write(OUT, 'study_c', studyC)
    write(OUT, 'assembly', assembly)
    write(OUT, 'verify', verify)
    write(OUT, 'team', team)
    write(OUT, 'atlas', atlas)
