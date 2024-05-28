import pygame, json, math
from xml.dom import minidom
import svg.path as svgPath

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

class RelLine: # Works with absolute coords
    def __init__(self, points: list[int,int]):
        global _UIDCOUNT
        self.points = points
        _UIDCOUNT += 1
        self.uid = _UIDCOUNT
    
    def draw(self, sur, colour, line_thickness=8, highlight_thickness=4, dot_thickness=12, dotColour=None, show_bps=True, highlight=None):
        if dotColour is None:
            dotColour = colour
        if highlight is not None:
            pygame.draw.lines(sur, highlight, False, self.points, line_thickness + 2*highlight_thickness)
            for i in self.points:
                pygame.draw.circle(sur, highlight, i, line_thickness/2 + highlight_thickness)
        pygame.draw.lines(sur, colour, False, self.points, line_thickness)
        for i in self.points:
                pygame.draw.circle(sur, colour, i, line_thickness/2)
        if show_bps:
            for i in self.points:
                pygame.draw.circle(sur, dotColour, i, dot_thickness)
    
    def getBps(self):
        return self.points
    
    def __hash__(self) -> int:
        return hash([self.uid, self.points])
    def __str__(self) -> str:
        return f'<Rel Line object with points ({",".join(self.points)})>'
    def __repr__(self) -> str: return str(self)
    
    def copy(self):
        return RelLine(self.points)

class Glyph: # Works with relative coords
    def __init__(self, name: str, points = None) -> None:
        global _UIDCOUNT
        self.name = name
        self.data = DAT[name]
        _UIDCOUNT += 1
        self.uid = _UIDCOUNT
        self.rotation = 0
        self.connections = {}
        self.position = [-99, -99]
        if points is not None:
            self.points = points
        else:
            try:
                self.points = _getGlyph(name)
            except KeyError:
                raise KeyError('No glyph named "%s" exists in `glyphs.svg`!' % name)
    
    def rotate(self, newRot):
        self.rotation = newRot
    
    def moveby(self, x, y, ignores=[]):
        self.position = (self.position[0] + x, self.position[1] + y)
        for i in self.connections:
            if self.connections[i][0] not in ignores:
                self.connections[i][0].moveby(x, y, ignores + [self])
    
    def moveto(self, x, y, ignores=[]):
        movement = (x - self.position[0], y - self.position[1])
        self.position = (x, y)
        for i in self.connections:
            if self.connections[i][0] not in ignores:
                self.connections[i][0].moveby(movement[0], movement[1], ignores + [self])
    
    # TODO: ScaleBy and ScaleTo
    
    def _draw_once(self, sur, colour, size, thickness):
        ma, mi = self.correct()
        def correct(x, y):
            rot = _rotate(((x - mi[0]) / ma * size, (y - mi[1]) / ma * size), self.rotation)
            return [rot[0] + self.position[0], rot[1] + self.position[1]]
        for i in self.points:
            if isinstance(i, svgPath.Move):
                start = correct(i.start.real, i.start.imag)
                pygame.draw.circle(sur, colour, start, thickness/2)
            elif isinstance(i, svgPath.Line):
                start = correct(i.start.real, i.start.imag)
                end = correct(i.end.real, i.end.imag)
                pygame.draw.line(sur, colour, start, end, thickness)
                pygame.draw.circle(sur, colour, end, thickness/2)
            elif isinstance(i, svgPath.CubicBezier): # Thanks to https://stackoverflow.com/questions/69804595/trying-to-make-a-bezier-curve-on-pygame-library !
                calc = lambda v: correct(v.real, v.imag)
                p1, p1_handle, p2_handle, p2 = calc(i.start), calc(i.control1), calc(i.control2), calc(i.end)
                lastPoint = None
                for t2 in range(0, 100):
                    t = t2 / 100
                    point = (p1[0] * (1 - t) ** 3 + 3 * p1_handle[0] * t * (1 - t) ** 2 + 3 * p2_handle[0] * t ** 2 * (1 - t) + p2[0] * t ** 3,
                             p1[1] * (1 - t) ** 3 + 3 * p1_handle[1] * t * (1 - t) ** 2 + 3 * p2_handle[1] * t ** 2 * (1 - t) + p2[1] * t ** 3)
                    if lastPoint is not None:
                        pygame.draw.line(sur, colour, lastPoint, point, thickness)
                    lastPoint = point
                pygame.draw.circle(sur, colour, lastPoint, thickness/2)
            else:
                raise ValueError(
                    'Path segment is not of a recognised type!! Found: ' + str(type(i))
                )
    
    def draw(self, sur, colour, size, line_thickness=8, highlight_thickness=4, dot_thickness=12, dotColours=(None, None), show_bps=True, highlight=None):
        if dotColours == (None, None):
            dotColours = (colour, (255, 50, 10))
        elif len(dotColours) != 2:
            dotColours = (dotColours, (255, 50, 10))
        if highlight is not None:
            self._draw_once(sur, highlight, size, line_thickness + 2*highlight_thickness)
        self._draw_once(sur, colour, size, line_thickness)
        if show_bps:
            j = 0
            for i in self.getBps(self.position, size):
                pygame.draw.circle(sur, dotColours[int(j in self.connections)], i, dot_thickness)
                j += 1
    
    def getRect(self, size, spacing=0):
        points = [(i[0] * size + self.position[0], i[1] * size + self.position[1]) for i in self.getCorrectedPoints()]
        ma, mi = _correction(points)
        return pygame.Rect(
            mi[0] - spacing/2,
            mi[1] - spacing/2,
            ma + spacing,
            ma + spacing
        )
    
    def getCorrectedPoints(self):
        points = _parsePath(self.points)
        ma, mi = self.correct()
        return [_rotate(((i[0] - mi[0]) / ma, (i[1] - mi[1]) / ma), self.rotation) for i in points]
    
    def correct(self):
        points = _parsePath(self.points)
        ma, mi = _correction(points)
        ma2, mi2 = _correction([_rotate(((i[0] - mi[0]) / ma, (i[1] - mi[0]) / ma), self.rotation) for i in points])
        return ma * ma2, (mi[0] + mi2[0], mi[1] + mi2[1])
    
    def getBps(self, pos, size):
        bps = []
        points = self.getCorrectedPoints()
        for i in self.data['BPs']:
            p = points[i]
            bps.append((p[0] * size + pos[0], p[1] * size + pos[1]))
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
    return {i.attributes.get('inkscape:label').value: Glyph(i.attributes.get('inkscape:label').value, svgPath.parse_path(i.attributes.get('d').value))
            for i in DOC if i.nodeName == 'path'}

def _getGlyph(name: str) -> list[tuple[int,int]]:
    allGlyphs = {i.attributes.get('inkscape:label').value: i.attributes.get('d').value for i in DOC if i.nodeName == 'path'}
    return allGlyphs[name]

def _parsePath(path) -> list[tuple[int,int]]:
    points = []
    for segment in path:
        points.append((segment.start.real, segment.start.imag))
        points.append((segment.end.real, segment.end.imag))
    return points

def _correction(points: list[tuple[int,int]]) -> list[tuple[int,int]]:
    mi = (min([i[0] for i in points]), min([i[1] for i in points]))
    newpts = [(i[0] - mi[0], i[1] - mi[1]) for i in points]
    ma = max([max([i[0] for i in newpts]), max([i[1] for i in newpts])])
    return ma, mi
