# Single source of truth for the catgirl model: parts, cubes, UV packing and texture painting.
from PIL import Image

TEX_W, TEX_H = 128, 128

# Palette (abgeleitet aus dem Referenzbild, für Pixel-Art angepasst)
C = dict(
    hair_d=(46, 37, 41), hair=(66, 53, 58), hair_l=(92, 76, 82), hair_hl=(118, 100, 107),
    skin=(253, 233, 223), skin_s=(240, 210, 198), blush=(246, 182, 180), mouth=(201, 120, 116),
    eye_hl=(255, 236, 170), eye=(245, 166, 35), eye_d=(196, 112, 26), lash=(60, 38, 30),
    white=(246, 244, 247), white_s=(214, 210, 220),
    vest=(157, 156, 164), vest_d=(124, 123, 132), vest_l=(178, 177, 184),
    bow=(47, 134, 179), bow_d=(29, 88, 124), bow_l=(120, 190, 220),
    plaid=(112, 104, 114), plaid_d=(62, 56, 66), plaid_l=(168, 160, 170), plaid_in=(48, 44, 52),
    stock=(44, 43, 51), stock_l=(64, 62, 72), sole=(32, 31, 38),
    ear_in=(232, 168, 176), fluff=(255, 255, 255), gold=(231, 181, 58),
)
T = None  # transparent

# part: name, parent, pivot(x,y,z), cubes[(x,y,z,w,h,d, inflate, painter)]
PARTS = []
def part(name, parent, pivot, cubes):
    PARTS.append(dict(name=name, parent=parent, pivot=pivot, cubes=cubes))

# ---------- painters: f(face, i, j, w, h) -> color or None ----------
# faces: north(front,-z) south(back,+z) west(-x, character's right) east(+x) up down
def hair_shade(i, j, seed=0):
    k = (i * 7 + seed * 3) % 5
    if k == 0: return C['hair_d']
    if k == 3: return C['hair_l']
    return C['hair']

def p_head(f, i, j, w, h):
    if f == 'north':
        if j <= 2: return hair_shade(i, j)
        if i in (0, 7): return C['hair_d']
        if j == 3: return C['hair'] if i in (1, 3, 6) else C['skin']
        if j == 4: return C['lash'] if i in (1, 2, 5, 6) else C['skin']
        if j == 5:
            return {1: C['eye_hl'], 2: C['eye'], 5: C['eye'], 6: C['eye_hl']}.get(i, C['skin'])
        if j == 6:
            return {1: C['eye'], 2: C['eye_d'], 5: C['eye_d'], 6: C['eye']}.get(i, C['skin'])
        if j == 7:
            if i == 4: return C['mouth']
            if i in (1, 6): return C['blush']
            return C['skin']
    if f == 'down': return C['skin_s']
    return hair_shade(i, j, 1)

def p_hairlayer(f, i, j, w, h):
    if f == 'north':
        if j <= 1: return hair_shade(i, j, 2)
        if j == 2: return C['hair'] if i not in (2, 5) else T
        if i in (0, 7): return C['hair'] if j < 7 else C['hair_d']
        return T
    if f == 'down': return T
    if f == 'up': return C['hair_hl'] if (i + j) % 6 == 0 else hair_shade(i, j, 3)
    return C['hair_hl'] if (j == 1 and i % 3 == 1) else hair_shade(i, j, 4)

def p_ear(f, i, j, w, h):
    if f == 'north':
        if j == 0 and i != 1: return T
        if j == h - 1: return C['fluff']
        return C['ear_in']
    if f in ('west', 'east', 'south') and j == 0 and w == 3 and f == 'south' and i != 1: return T
    return C['hair']

def p_hairback(f, i, j, w, h):
    if j == h - 1 and i % 3 == 1: return T  # fransiges Ende
    if f in ('south', 'north'): return hair_shade(i, j, 5) if f == 'south' else C['hair_d']
    return C['hair']

def p_hairside(f, i, j, w, h):
    if j == h - 1 and i == 0: return T
    return hair_shade(i, j, 6)

def p_torso(f, i, j, w, h):
    if f == 'north':
        if j == 0: return C['skin'] if i in (3, 4) else C['white']
        if j == 1: return C['white'] if 1 <= i <= 6 else C['white_s']
        if j == 2: return C['white'] if 2 <= i <= 5 else C['vest_l']
        if j == 3: return C['white'] if 3 <= i <= 4 else C['vest']
        if j == 5 and i == 4: return C['gold']
        if j >= 10: return C['vest_d']
        return C['vest'] if i not in (0, 7) else C['vest_d']
    if f == 'up': return C['skin'] if 3 <= i <= 4 and j >= 1 else C['white']
    if f == 'down': return C['vest_d']
    if j == 0: return C['white']
    return C['vest_d'] if j >= 10 else C['vest']

def p_bow(f, i, j, w, h):
    if f == 'north':
        if i in (1, 2): return C['bow_d']
        return C['bow_l'] if (i + j) % 2 == 0 else C['bow']
    return C['bow_d']

def p_skirt(f, i, j, w, h):
    if f == 'up': return C['plaid_d']
    if f == 'down': return C['plaid_in']
    if j == 2 or i % 3 == 0: return C['plaid_d']
    if j == 4: return C['plaid_l']
    return C['plaid'] if i % 2 == 0 else (C['plaid'][0] - 8, C['plaid'][1] - 8, C['plaid'][2] - 8)

def p_arm(right):
    def f_(f, i, j, w, h):
        if f == 'up': return C['white']
        if f == 'down': return C['skin_s']
        if j <= 2: return C['white']
        if j == 3: return C['white_s']
        if right and j == 9: return C['fluff']  # Armband wie im Bild
        return C['skin_s'] if j == h - 1 else C['skin']
    return f_

def p_thigh(f, i, j, w, h):
    if f == 'up': return C['skin']
    if j <= 2: return C['skin'] if j < 2 else C['skin_s']
    return C['stock_l'] if (j == 3) else C['stock']

def p_shin(f, i, j, w, h):
    if f == 'down': return C['sole']
    return C['stock'] if j < h - 1 else C['sole']

def p_tail(tip):
    def f_(f, i, j, w, h):
        if tip and f == 'south': return C['hair_d']
        return C['hair'] if (i + j) % 3 else C['hair_l']
    return f_

# ---------- hierarchy (Minecraft-Modellkoordinaten, y zeigt nach unten, y=24 = Boden) ----------
part('torso', None, (0, 12, 0), [(-4, -12, -2, 8, 12, 4, 0, p_torso)])
part('head', 'torso', (0, -12, 0), [(-4, -8, -4, 8, 8, 8, 0, p_head), (-4, -8, -4, 8, 8, 8, 0.5, p_hairlayer)])
part('left_ear', 'head', (2.6, -8.3, -0.5), [(-1.5, -3, -0.5, 3, 3, 1, 0, p_ear)])
part('right_ear', 'head', (-2.6, -8.3, -0.5), [(-1.5, -3, -0.5, 3, 3, 1, 0, p_ear)])
part('hair_back', 'head', (0, -7, 4.3), [(-4.5, 0, -0.5, 9, 17, 1, 0, p_hairback)])
part('left_hair', 'head', (4.6, -5, -2.6), [(-0.5, 0, -1, 1, 11, 2, 0, p_hairside)])
part('right_hair', 'head', (-4.6, -5, -2.6), [(-0.5, 0, -1, 1, 11, 2, 0, p_hairside)])
part('bow', 'torso', (0, -10.5, -2.1), [(-2, -1, -1, 4, 2, 1, 0, p_bow)])
part('skirt', 'torso', (0, -3, 0), [(-4.5, 0, -2.5, 9, 5, 5, 0, p_skirt)])
part('tail', 'torso', (0, -1.5, 2.4), [(-0.5, -0.5, 0, 1, 1, 5, 0, p_tail(False))])
part('tail_mid', 'tail', (0, 0, 4.8), [(-0.5, -0.5, 0, 1, 1, 5, -0.05, p_tail(False))])
part('tail_tip', 'tail_mid', (0, 0, 4.8), [(-0.5, -0.5, 0, 1, 1, 4, -0.1, p_tail(True))])
part('right_arm', 'torso', (-5, -10, 0), [(-1.5, -2, -1.5, 3, 12, 3, 0, p_arm(True))])
part('left_arm', 'torso', (5, -10, 0), [(-1.5, -2, -1.5, 3, 12, 3, 0, p_arm(False))])
part('right_leg', None, (-1.9, 12, 0), [(-1.5, 0, -1.5, 3, 6, 3, 0, p_thigh)])
part('right_shin', 'right_leg', (0, 6, 0), [(-1.5, 0, -1.5, 3, 6, 3, -0.04, p_shin)])
part('left_leg', None, (1.9, 12, 0), [(-1.5, 0, -1.5, 3, 6, 3, 0, p_thigh)])
part('left_shin', 'left_leg', (0, 6, 0), [(-1.5, 0, -1.5, 3, 6, 3, -0.04, p_shin)])

# ---------- UV packing (Shelf-Packer) ----------
def net_size(w, h, d):
    import math
    w, h, d = math.ceil(w), math.ceil(h), math.ceil(d)
    return 2 * d + 2 * w, d + h

def pack():
    items = []
    for p in PARTS:
        for ci, c in enumerate(p['cubes']):
            nw, nh = net_size(*c[3:6])
            items.append((nh, nw, p['name'], ci))
    items.sort(key=lambda t: (-t[0], -t[1]))
    x = y = rowh = 0
    uv = {}
    for nh, nw, name, ci in items:
        if x + nw > TEX_W:
            x, y, rowh = 0, y + rowh, 0
        uv[(name, ci)] = (x, y)
        x += nw
        rowh = max(rowh, nh)
    assert y + rowh <= TEX_H, 'Textur zu klein'
    return uv

UV = pack()

def face_rects(u, v, w, h, d):
    import math
    w, h, d = math.ceil(w), math.ceil(h), math.ceil(d)
    return {
        'up': (u + d, v, w, d), 'down': (u + d + w, v, w, d),
        'west': (u, v + d, d, h), 'north': (u + d, v + d, w, h),
        'east': (u + d + w, v + d, d, h), 'south': (u + 2 * d + w, v + d, w, h),
    }

def build_texture(path):
    img = Image.new('RGBA', (TEX_W, TEX_H), (0, 0, 0, 0))
    px = img.load()
    for p in PARTS:
        for ci, c in enumerate(p['cubes']):
            u, v = UV[(p['name'], ci)]
            painter = c[7]
            for f, (fx, fy, fw, fh) in face_rects(u, v, *c[3:6]).items():
                for j in range(fh):
                    for i in range(fw):
                        col = painter(f, i, j, fw, fh)
                        if col is not None:
                            px[fx + i, fy + j] = (*col, 255)
    img.save(path)
    return img

def java_layer_code():
    out = []
    var = {None: 'root'}
    for p in PARTS:
        v = p['name'].replace('_', '')
        var[p['name']] = v
        cubes = ''
        for ci, c in enumerate(p['cubes']):
            u, vv = UV[(p['name'], ci)]
            x, y, z, w, h, d, inf = c[:7]
            dim = f'new CubeDeformation({inf}f)' if inf else 'CubeDeformation.NONE'
            cubes += f'\n\t\t\t\t.texOffs({u}, {vv}).addBox({x}f, {y}f, {z}f, {w}f, {h}f, {d}f, {dim})'
        px_, py, pz = p['pivot']
        out.append(f'\t\tPartDefinition {v} = {var[p["parent"]]}.addOrReplaceChild("{p["name"]}", CubeListBuilder.create(){cubes},\n\t\t\t\tPartPose.offset({px_}f, {py}f, {pz}f));')
    return '\n'.join(out)
