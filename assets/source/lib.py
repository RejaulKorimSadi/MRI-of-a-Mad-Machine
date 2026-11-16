import base64, io, os, html, math, sys
from fontTools.ttLib import TTFont
from fontTools import subset

FS = os.environ.get('FONTSOURCE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules', '@fontsource')) + '/'
e = html.escape
STATIC = os.environ.get('STATIC') == '1'

FONTS = {
    'Disp': [('fraunces/files/fraunces-latin-600-normal.woff2', 600, 'normal'),
             ('fraunces/files/fraunces-latin-400-italic.woff2', 400, 'italic'),
             ('fraunces/files/fraunces-latin-300-italic.woff2', 300, 'italic')],
    'Mono': [('jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2', 400, 'normal'),
             ('jetbrains-mono/files/jetbrains-mono-latin-600-normal.woff2', 600, 'normal'),
             ('jetbrains-mono/files/jetbrains-mono-greek-400-normal.woff2', 400, 'normal')],
    'Sans': [('inter/files/inter-latin-400-normal.woff2', 400, 'normal'),
             ('inter/files/inter-latin-600-normal.woff2', 600, 'normal'),
             ('inter/files/inter-greek-400-normal.woff2', 400, 'normal')],
}
CHARS = ''.join(chr(c) for c in range(32, 127)) + '›·–—…’“”×κχ→←↑↓✓✗≈≥≤°−⁻¹²³⁴⁵⁶⁷⁸⁹⁰'
_cache = {}


def sub(path):
    if path in _cache:
        return _cache[path]
    f = TTFont(FS + path)
    o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['kern', 'liga']
    s = subset.Subsetter(o); s.populate(text=CHARS); s.subset(f)
    b = io.BytesIO(); f.flavor = 'woff2'; f.save(b)
    _cache[path] = base64.b64encode(b.getvalue()).decode()
    return _cache[path]


def fontcss(fams):
    return ''.join(f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{sub(p)}) format('woff2');font-weight:{w};font-style:{st}}}"
                   for fam in fams for p, w, st in FONTS[fam])


_m = {}


def width(text, fam, size, weight=400, style='normal'):
    key = (fam, weight, style)
    if key not in _m:
        p = [x for x in FONTS[fam] if x[1] == weight and x[2] == style][0][0]
        t = TTFont(FS + p); _m[key] = (t.getBestCmap(), t['hmtx'].metrics, t['head'].unitsPerEm)
    cm, hm, upm = _m[key]
    return sum(hm[cm[ord(c)]][0] if ord(c) in cm else upm * .5 for c in text) * size / upm


DARK = dict(bg='#090C11', panel='#0E131A', panel2='#121923', line='#1C2531', grid='#141B24', ink='#ECF0F3',
            muted='#8B98A7', faint='#4C5867', teal='#6FE3D3', amber='#F2B460', red='#FF5D4F', blue='#7AA7FF', glow='.55')
LIGHT = dict(bg='#F6F2EA', panel='#FFFCF6', panel2='#FBF6EC', line='#E2DACB', grid='#ECE5D8', ink='#15181D',
             muted='#5C6672', faint='#A69E90', teal='#0D7A6E', amber='#A3600E', red='#C4372A', blue='#2F5FBF', glow='.25')


def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    A, B = hx(a), hx(b)
    return '#%02X%02X%02X' % tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))


BASE_CSS = '''
.d{font-family:Disp}.m{font-family:Mono}.s{font-family:Sans}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.15}}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes glitch{0%,86%,100%{opacity:1;transform:none}88%{opacity:.2;transform:translateX(2px)}90%{opacity:1;transform:translateX(-2px)}92%{opacity:.4}94%{opacity:1;transform:none}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.blink{animation:blink 1.4s steps(1) infinite}.pulse{animation:pulse 3s ease-in-out infinite}
.rise{opacity:0;animation:rise .9s cubic-bezier(.2,.7,.2,1) forwards}
.glitch{animation:glitch 4s infinite;transform-box:fill-box}
.float{animation:float 5s ease-in-out infinite;transform-box:fill-box}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.rise{opacity:1}}
'''


SUPMAP = str.maketrans('⁻¹²³⁴⁵⁶⁷⁸⁹⁰', '−1234567890')


def supfix(body):
    import re
    return re.sub(r'[⁻¹²³⁴⁵⁶⁷⁸⁹⁰]+', lambda m: f'<tspan baseline-shift="super" font-size="68%">{m.group(0).translate(SUPMAP)}</tspan>', body)


def svg(W, H, body, P, fams=('Disp', 'Mono', 'Sans'), defs='', title=''):
    body = supfix(body)
    css = fontcss(fams) + BASE_CSS + (
        f".ink{{fill:{P['ink']}}}.mut{{fill:{P['muted']}}}.fnt{{fill:{P['faint']}}}.tl{{fill:{P['teal']}}}"
        f".am{{fill:{P['amber']}}}.rd{{fill:{P['red']}}}.bl{{fill:{P['blue']}}}")
    if STATIC:
        css += '*{animation:none!important}.rise{opacity:1!important}'
    t = f'<title>{e(title)}</title>' if title else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">{t}'
            f'<defs><style>{css}</style>'
            f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{P["grid"]}"/></pattern>{defs}</defs>{body}</svg>')


def frame(W, H, P, r=16):
    return (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{r}" fill="{P["bg"]}" stroke="{P["line"]}"/>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{r}" fill="url(#dots)" opacity=".9"/>')


def corners(W, H, P, m=14, L=18):
    c = P['faint']
    return ''.join(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.2"/>' for d in [
        f'M{m} {m+L}V{m}H{m+L}', f'M{W-m-L} {m}H{W-m}V{m+L}', f'M{m} {H-m-L}V{H-m}H{m+L}', f'M{W-m-L} {H-m}H{W-m}V{H-m-L}'])


def arrow(x1, y, x2, col, w=1.4, dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="M{x1} {y}H{x2}" stroke="{col}" stroke-width="{w}"{da} fill="none"/>'
            f'<path d="M{x2-7} {y-4.5}L{x2} {y}L{x2-7} {y+4.5}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def sup(t, size=None):
    s = f' font-size="{size}"' if size else ' font-size="70%"'
    return f'<tspan{s} dy="-0.45em">{e(t)}</tspan><tspan dy="0.45em"> </tspan>'


def sweep(W, H, P, r=16, dur=9, begin=0):
    """soft light band crossing the card"""
    gid = f'sw{abs(hash((W, H, dur, begin))) % 99999}'
    return (f'<linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{P["teal"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{P["teal"]}" stop-opacity="{float(P["glow"])*.12:.3f}"/><stop offset="1" stop-color="{P["teal"]}" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="c{gid}"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{r}"/></clipPath>'
            f'<g clip-path="url(#c{gid})"><rect x="-260" y="0" width="240" height="{H}" fill="url(#{gid})">'
            f'<animate attributeName="x" values="-260;{W+20};{W+20}" keyTimes="0;.45;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></rect></g>')


def grow_w(final, delay, dur=8):
    """width animation that holds final value (base attribute should be final for static renderers)"""
    return (f'<animate attributeName="width" values="0;{final:.1f};{final:.1f};0" keyTimes="0;.22;.88;1" dur="{dur}s" begin="{delay}s" '
            f'repeatCount="indefinite" calcMode="spline" keySplines=".2 .7 .2 1;0 0 1 1;.6 0 .8 .3"/>')


def grow_h(final, y_end, delay, dur=8):
    return (f'<animate attributeName="height" values="0;{final:.1f};{final:.1f};0" keyTimes="0;.22;.88;1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .7 .2 1;0 0 1 1;.6 0 .8 .3"/>'
            f'<animate attributeName="y" values="{y_end};{y_end-final:.1f};{y_end-final:.1f};{y_end}" keyTimes="0;.22;.88;1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .7 .2 1;0 0 1 1;.6 0 .8 .3"/>')


# ---------- isometric 3D ----------
C30, S30 = math.cos(math.radians(30)), .5


def iso(ox, oy, x, y, z):
    return ox + (x - y) * C30, oy + (x + y) * S30 - z


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'


def ibox(ox, oy, x, y, z, w, d, h, col, P, stroke=None, op=1, cls='', extra='', top_override=None):
    """isometric box with three shaded faces; (x,y,z) = near-bottom-left corner in iso space"""
    top = [iso(ox, oy, x, y, z + h), iso(ox, oy, x + w, y, z + h), iso(ox, oy, x + w, y + d, z + h), iso(ox, oy, x, y + d, z + h)]
    left = [iso(ox, oy, x, y + d, z), iso(ox, oy, x + w, y + d, z), iso(ox, oy, x + w, y + d, z + h), iso(ox, oy, x, y + d, z + h)]
    right = [iso(ox, oy, x + w, y, z), iso(ox, oy, x + w, y + d, z), iso(ox, oy, x + w, y + d, z + h), iso(ox, oy, x + w, y, z + h)]
    dk = P['bg']
    lt = '#FFFFFF'
    st = stroke or mix(col, dk, .55)
    tc = top_override or mix(col, lt, .18)
    c = f' class="{cls}"' if cls else ''
    return (f'<g opacity="{op}"{c}{extra}>'
            f'<path d="{poly(left)}" fill="{mix(col, dk, .28)}" stroke="{st}" stroke-width=".8" stroke-linejoin="round"/>'
            f'<path d="{poly(right)}" fill="{mix(col, dk, .48)}" stroke="{st}" stroke-width=".8" stroke-linejoin="round"/>'
            f'<path d="{poly(top)}" fill="{tc}" stroke="{st}" stroke-width=".8" stroke-linejoin="round"/></g>')


def itop(ox, oy, x, y, z, w, d):
    return poly([iso(ox, oy, x, y, z), iso(ox, oy, x + w, y, z), iso(ox, oy, x + w, y + d, z), iso(ox, oy, x, y + d, z)])


def write(outdir, name, mk):
    os.makedirs(outdir, exist_ok=True)
    for mode, P in (('dark', DARK), ('light', LIGHT)):
        s = mk(P, mode)
        open(f'{outdir}/{name}-{mode}.svg', 'w', encoding='utf-8').write(s)
    print(f'{name}', len(s) // 1024, 'KB')
