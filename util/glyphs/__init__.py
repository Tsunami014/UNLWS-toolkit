import pygame, json, math
from xml.dom import minidom
from svg.path import parse_path

DOC = minidom.parse('util/glyphs/glyphs.svg').documentElement.childNodes
DAT = json.load(open('util/glyphs/glyph_data.json'))

_UIDCOUNT = 0

def _rotate(point, angle): # Thanks, https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python !
    """
    Rotate a point clockwise by a given angle around (0, 0).

    The angle should be given in degrees.
    """
    angle = math.radians(-angle)
    px, py = point
    
    cos = math.cos(angle)
    sin = math.sin(angle)

    qx = cos * px - sin * py
    qy = sin * px + cos * py
    return qx, qy

class Glyph:
    def __init__(self, name: str, points: list[tuple[int,int]] = None) -> None:
        global _UIDCOUNT
        self.name = name
        self.data = DAT[name]
        _UIDCOUNT += 1
        self.uid = _UIDCOUNT
        self.rotation = 0
        if points is not None:
            self.basepoints = points
        else:
            try:
                self.basepoints = _getGlyph(name)
            except KeyError:
                raise KeyError('No glyph named "%s" exists in `glyphs.svg`!' % name)
        self.points = self.basepoints
    
    def rotate(self, newRot):
        self.rotation = newRot
        self.points = _correctGlyph([_rotate(i, newRot) for i in self.basepoints])
    
    def draw(self, sur, colour, pos, size, line_thickness=8, highlight_thickness=4, dot_thickness=12, dotColour=None, show_bps=True, highlight=None):
        if dotColour is None:
            dotColour = colour
        points = [(i[0] * size + pos[0], i[1] * size + pos[1]) for i in self.points]
        if highlight is not None:
            pygame.draw.lines(sur, highlight, False, points, line_thickness + 2*highlight_thickness)
        pygame.draw.lines(sur, colour, False, points, line_thickness)
        if show_bps:
            for i in self.data['BPs']:
                point = self.points[i]
                pygame.draw.circle(sur, dotColour, (int(point[0] * size + pos[0]), int(point[1] * size + pos[1])), dot_thickness)
    
    def getBps(self, pos, size):
        bps = []
        for i in self.data['BPs']:
            point = self.points[i]
            bps.append((int(point[0] * size + pos[0]), int(point[1] * size + pos[1])))
        return bps
    
    def __hash__(self) -> int:
        return hash([self.uid, self.name, self.points])
    
    def __str__(self) -> str:
        return f'<Glyph object of name {self.name}>'
    def __repr__(self) -> str: return str(self)

    def copy(self):
        return Glyph(self.name, self.points)

def getAllGlyphNames() -> list[str]:
    return [i.attributes.get('inkscape:label').value for i in DOC if i.nodeName == 'path']

def getAllGlyphs() -> dict[str:Glyph]:
    return {i.attributes.get('inkscape:label').value: Glyph(i.attributes.get('inkscape:label').value, _correctGlyph(_parseGlyph(i.attributes.get('d').value)))
            for i in DOC if i.nodeName == 'path'}


def _getGlyph(name: str) -> list[tuple[int,int]]:
    allGlyphs = {i.attributes.get('inkscape:label').value: i.attributes.get('d').value for i in DOC if i.nodeName == 'path'}
    return _correctGlyph(_parseGlyph(allGlyphs[name].attributes.get('d').value))

def _parseGlyph(ptsstr: str) -> list[tuple[int,int]]:
    path = parse_path(ptsstr)
    points = []
    for segment in path:
        points.append((segment.start.real, segment.start.imag))
        points.append((segment.end.real, segment.end.imag))
    return points

def _correctGlyph(points: list[tuple[int,int]]) -> list[tuple[int,int]]:
    mi = (min([i[0] for i in points]), min([i[1] for i in points]))
    newpts = [(i[0] - mi[0], i[1] - mi[1]) for i in points]
    ma = max([max([i[0] for i in newpts]), max([i[1] for i in newpts])])
    return [(i[0] / ma, i[1] / ma) for i in newpts]
