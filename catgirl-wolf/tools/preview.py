import math, numpy as np
from PIL import Image, ImageDraw
import spec

PI = math.pi
TAIL_VERTICAL = False

def anim(s):
    """Python-Spiegel von CatgirlWolfModel.setupAnim. Gibt pro Teil (x,y,z,xr,yr,zr) zurück."""
    P = {p['name']: list(p['pivot']) + [0.0, 0.0, 0.0] for p in spec.PARTS}
    age, wp, ws = s['age'], s['walkPos'], min(s['walkSpeed'], 1.0)
    yaw, pitch = math.radians(s['yaw']), math.radians(s['pitch'])
    breath = math.sin(age * 0.08)
    sway = math.sin(age * 0.12)

    if s['sitting']:
        P['torso'][1] = 21.8; P['torso'][3] = 0.30 + breath * 0.015
        P['head'][3] = pitch - 0.16; P['head'][4] = yaw; P['head'][5] = 0.14
        for side, sg in (('right', -1), ('left', 1)):
            leg, shin, arm = P[side + '_leg'], P[side + '_shin'], P[side + '_arm']
            leg[0] = 1.9 * sg; leg[1] = 22.4; leg[2] = -0.6
            leg[3] = -PI / 2; leg[4] = 0.22 * sg
            shin[5] = -(PI - 0.95) * sg
            arm[3] = -0.78 + breath * 0.02; arm[5] = 0.16 * sg
        P['tail'][3] = -0.15; P['tail'][4] = 0.75 + sway * 0.08
        P['tail_mid'][3] = 0.85; P['tail_mid'][4] = sway * 0.12
        P['tail_tip'][3] = 0.8; P['tail_tip'][4] = sway * 0.18
    else:
        P['torso'][3] = 0.15 * ws + breath * 0.012
        P['head'][3] = pitch; P['head'][4] = yaw
        ph = wp * 0.6662
        for side, sg, off in (('right', -1, 0.0), ('left', 1, PI)):
            leg, shin, arm = P[side + '_leg'], P[side + '_shin'], P[side + '_arm']
            leg[3] = math.cos(ph + off) * 1.1 * ws
            shin[3] = max(0.0, -math.sin(ph + off)) * 1.0 * ws
            arm[3] = math.cos(ph + off + PI) * 0.9 * ws - 0.1 * ws
            arm[5] = (0.07 + 0.025 * breath) * -sg
        tw = math.cos(ph) * 0.35 * ws
        P['tail'][3] = -0.85 + 0.35 * ws; P['tail'][4] = sway * 0.35 + tw
        P['tail_mid'][3] = 0.95 - 0.5 * ws; P['tail_mid'][4] = math.sin(age * 0.12 - 0.8) * 0.3
        P['tail_tip'][3] = 0.7 - 0.4 * ws; P['tail_tip'][4] = math.sin(age * 0.12 - 1.6) * 0.3

    # Ohren: Grundneigung + gelegentliches Zucken
    t = age % 97
    flick = math.sin(t / 7 * PI) * 0.35 if t < 7 else 0.0
    P['left_ear'][5] = 0.2; P['right_ear'][5] = -0.2
    P['left_ear'][3] = -flick
    if s.get('angry') or s.get('hurt'):
        for e, sg in (('left_ear', 1), ('right_ear', -1)):
            P[e][3] = -0.65; P[e][5] = 0.55 * sg
    if s.get('angry') and not s['sitting']:
        P['tail'][3] = -0.25
        for side in ('right', 'left'): P[side + '_arm'][3] -= 0.55
    if s.get('hurt'):
        P['head'][3] -= 0.3
    # Haare hängen schwerkraftgerecht nach unten
    if TAIL_VERTICAL: P['tail'][3] += PI / 2
    if 'hair_back' not in P: return P
    hx = P['torso'][3] + P['head'][3]
    P['hair_back'][3] = -hx * (0.45 if s['sitting'] else 1.0) + 0.06 + 0.25 * ws * (0 if s['sitting'] else 1) + breath * 0.02
    P['left_hair'][3] = P['right_hair'][3] = -hx * 0.85
    P['left_hair'][5] = -P['head'][5]; P['right_hair'][5] = -P['head'][5]
    return P

def rot(xr, yr, zr):
    cx, sx, cy, sy, cz, sz = math.cos(xr), math.sin(xr), math.cos(yr), math.sin(yr), math.cos(zr), math.sin(zr)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

def world_mats(P):
    M = {}
    for p in spec.PARTS:
        x, y, z, xr, yr, zr = P[p['name']]
        L = np.eye(4); L[:3, :3] = rot(xr, yr, zr); L[:3, 3] = (x, y, z)
        M[p['name']] = (M[p['parent']] @ L) if p['parent'] else L
    return M

FACES = {  # origin, u-dir, v-dir (in Würfelkoordinaten, Vorzeichen auf die Grenzen bezogen)
    'north': (('x0', 'y0', 'z0'), (1, 0, 0), (0, 1, 0)),
    'south': (('x1', 'y0', 'z1'), (-1, 0, 0), (0, 1, 0)),
    'west':  (('x0', 'y0', 'z1'), (0, 0, -1), (0, 1, 0)),
    'east':  (('x1', 'y0', 'z0'), (0, 0, 1), (0, 1, 0)),
    'up':    (('x0', 'y0', 'z1'), (1, 0, 0), (0, 0, -1)),
    'down':  (('x0', 'y1', 'z0'), (1, 0, 0), (0, 0, 1)),
}

def render(P, tex, yaw_deg=25, pitch_deg=12, scale=14, size=(560, 620)):
    M = world_mats(P)
    px = tex.load()
    cy_, sy_ = math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg))
    cp, sp = math.cos(math.radians(pitch_deg)), math.sin(math.radians(pitch_deg))
    V = np.array([[cy_, 0, -sy_], [0, 1, 0], [sy_, 0, cy_]])
    V = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]]) @ V
    quads = []
    for p in spec.PARTS:
        W = M[p['name']]
        for ci, c in enumerate(p['cubes']):
            x, y, z, w, h, d, inf = c[:7]
            b = dict(x0=x - inf, y0=y - inf, z0=z - inf, x1=x + w + inf, y1=y + h + inf, z1=z + d + inf)
            u0, v0 = spec.UV[(p['name'], ci)]
            rects = spec.face_rects(u0, v0, w, h, d)
            for f, (org, ud, vd) in FACES.items():
                fx, fy, fw, fh = rects[f]
                o = np.array([b[k] for k in org], float)
                span_u = {(1, 0, 0): b['x1'] - b['x0'], (-1, 0, 0): b['x1'] - b['x0'], (0, 0, 1): b['z1'] - b['z0'], (0, 0, -1): b['z1'] - b['z0']}[ud]
                span_v = {(0, 1, 0): b['y1'] - b['y0'], (0, 0, -1): b['z1'] - b['z0'], (0, 0, 1): b['z1'] - b['z0']}[vd]
                du = np.array(ud, float) * span_u / fw; dv = np.array(vd, float) * span_v / fh
                for j in range(fh):
                    for i in range(fw):
                        col = px[fx + i, fy + j]
                        if col[3] == 0: continue
                        pts = [o + du * i + dv * j, o + du * (i + 1) + dv * j, o + du * (i + 1) + dv * (j + 1), o + du * i + dv * (j + 1)]
                        wp = [(W @ np.append(q, 1))[:3] for q in pts]
                        vp = [V @ np.array([q[0], q[1] - 12, q[2]]) for q in wp]
                        n = np.cross(vp[1] - vp[0], vp[3] - vp[0])
                        quads.append((np.mean([q[2] for q in vp]), vp, col, n))
    img = Image.new('RGBA', size, (236, 240, 232, 255))
    dr = ImageDraw.Draw(img)
    # Boden
    gy = size[1] / 2 + (12 * cp) * scale
    dr.line([(0, gy), (size[0], gy)], fill=(160, 170, 150), width=2)
    light = np.array([0.4, -0.7, -0.6]); light /= np.linalg.norm(light)
    for zc, vp, col, n in sorted(quads, key=lambda q: -q[0]):
        nn = np.linalg.norm(n)
        shade = 0.72 + 0.28 * abs(np.dot(n / nn, light)) if nn > 0 else 1
        c = tuple(int(min(255, v * shade)) for v in col[:3])
        poly = [(size[0] / 2 + q[0] * scale, size[1] / 2 + q[1] * scale) for q in vp]
        dr.polygon(poly, fill=c, outline=c)
    return img
