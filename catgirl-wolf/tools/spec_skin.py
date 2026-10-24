# Catgirl-Modell im Standard-Spielerskin-Layout (64x64, schmale Arme / "Alex").
# Jeder normale Minecraft-Skin passt damit direkt als Textur.
# Ohren und Schwanz haben im Skinformat keinen eigenen Platz: Sie lesen ihre Pixel
# aus den Haarbereichen des Kopfes (Seite bzw. Rückseite) und bekommen so automatisch die Haarfarbe.
from PIL import Image
import spec as old

C = old.C
TEX_W, TEX_H = 64, 64

def none(*a): return None

def p_leg(f, i, j, w, h):
    if f in ('up', 'down'): return C['skin'] if f == 'up' else C['sole']
    return old.p_thigh(f, i, j, w, 6) if j < 6 else old.p_shin(f, i, j - 6, w, 6)

def p_jacket(f, i, j, w, h):  # Rock als Overlay-Ebene über der Hüfte
    if f in ('up', 'down'): return None
    return old.p_skirt(f, i, j - 9, w, 5) if j >= 9 else None

def p_pants(f, i, j, w, h):
    if f in ('up', 'down'): return None
    return old.p_skirt(f, i, j + 3, w, 5) if j <= 1 else None

# Name, Eltern, Pivot, [(x,y,z,w,h,d, inflate, texOffs, Maler für Standardtextur)]
PARTS = [
 ('torso', None, (0, 12, 0), [(-4, -12, -2, 8, 12, 4, 0, (16, 16), old.p_torso), (-4, -12, -2, 8, 12, 4, 0.25, (16, 32), p_jacket)]),
 ('head', 'torso', (0, -12, 0), [(-4, -8, -4, 8, 8, 8, 0, (0, 0), old.p_head), (-4, -8, -4, 8, 8, 8, 0.5, (32, 0), old.p_hairlayer)]),
 ('left_ear', 'head', (2.6, -8.3, -0.5), [(-1.5, -3, -0.5, 3, 3, 1, 0, (0, 8), None)]),
 ('right_ear', 'head', (-2.6, -8.3, -0.5), [(-1.5, -3, -0.5, 3, 3, 1, 0, (0, 8), None)]),
 ('tail', 'torso', (0, -1.5, 2.4), [(-0.5, 0, -0.5, 1, 5, 1, 0, (24, 8), None)]),
 ('tail_mid', 'tail', (0, 4.8, 0), [(-0.5, 0, -0.5, 1, 5, 1, -0.05, (28, 8), None)]),
 ('tail_tip', 'tail_mid', (0, 4.8, 0), [(-0.5, 0, -0.5, 1, 4, 1, -0.1, (24, 9), None)]),
 ('right_arm', 'torso', (-5, -10, 0), [(-1.5, -2, -2, 3, 12, 4, 0, (40, 16), old.p_arm(True)), (-1.5, -2, -2, 3, 12, 4, 0.25, (40, 32), none)]),
 ('left_arm', 'torso', (5, -10, 0), [(-1.5, -2, -2, 3, 12, 4, 0, (32, 48), old.p_arm(False)), (-1.5, -2, -2, 3, 12, 4, 0.25, (48, 48), none)]),
 # Bein = Oberschenkel (obere 6 Skin-Zeilen) + Unterschenkel (untere 6 Zeilen) für das Kniegelenk
 ('right_leg', None, (-1.9, 12, 0), [(-2, 0, -2, 4, 6, 4, 0, (0, 16), None), (-2, 0, -2, 4, 6, 4, 0.25, (0, 32), None)]),
 ('right_shin', 'right_leg', (0, 6, 0), [(-2, 0, -2, 4, 6, 4, -0.02, (0, 22), None), (-2, 0, -2, 4, 6, 4, 0.23, (0, 38), None)]),
 ('left_leg', None, (1.9, 12, 0), [(-2, 0, -2, 4, 6, 4, 0, (16, 48), None), (-2, 0, -2, 4, 6, 4, 0.25, (0, 48), None)]),
 ('left_shin', 'left_leg', (0, 6, 0), [(-2, 0, -2, 4, 6, 4, -0.02, (16, 54), None), (-2, 0, -2, 4, 6, 4, 0.23, (0, 54), None)]),
]

# Ganze Beinnetze für die Standardtextur (12 Zeilen hoch) malen
LEG_NETS = [((0, 16), p_leg), ((16, 48), p_leg), ((0, 32), p_pants), ((0, 48), p_pants)]

def build_default_texture(path):
    img = Image.new('RGBA', (TEX_W, TEX_H), (0, 0, 0, 0)); px = img.load()
    def paint(uv, w, h, d, painter):
        for f, (fx, fy, fw, fh) in old.face_rects(uv[0], uv[1], w, h, d).items():
            for j in range(fh):
                for i in range(fw):
                    c = painter(f, i, j, fw, fh)
                    if c is not None: px[fx + i, fy + j] = (*c, 255)
    for name, parent, pivot, cubes in PARTS:
        for c in cubes:
            if c[8] is not None: paint(c[7], *c[3:6], c[8])
    for uv, painter in LEG_NETS: paint(uv, 4, 12, 4, painter)
    img.save(path); return img

def java_layer_code():
    out = []
    for name, parent, pivot, cubes in PARTS:
        v = name.replace('_', ''); par = parent.replace('_', '') if parent else 'root'
        cb = ''
        for x, y, z, w, h, d, inf, uv, _ in cubes:
            dim = f'new CubeDeformation({inf}f)' if inf else 'CubeDeformation.NONE'
            cb += f'\n\t\t\t\t.texOffs({uv[0]}, {uv[1]}).addBox({x}f, {y}f, {z}f, {w}f, {h}f, {d}f, {dim})'
        out.append(f'\t\tPartDefinition {v} = {par}.addOrReplaceChild("{name}", CubeListBuilder.create(){cb},\n\t\t\t\tPartPose.offset({pivot[0]}f, {pivot[1]}f, {pivot[2]}f));')
    return '\n'.join(out)
