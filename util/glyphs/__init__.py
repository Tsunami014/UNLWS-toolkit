import pygame
from xml.dom import minidom
class Glyph:
    def __init__(self, name: str, points: list[tuple[int,int]] = None) -> None:
        self.name = name
        if points is not None:
            self.points = points
        else:
            try:
                self.points = _getGlyph(name)
            except KeyError:
                raise KeyError('No glyph named "%s" exists in `glyphs.svg`!' % name)
    
    def draw(self, sur, colour, pos, size, line_thickness=8):
        prev = self.points[0]
        for i in self.points[1:]:
            pygame.draw.line(sur, colour, (prev[0] * size + pos[0], prev[1] * size + pos[1]), (i[0] * size + pos[0], i[1] * size + pos[1]), line_thickness)
            prev = i

def getAllGlyphNames() -> list[str]:
    doc = minidom.parse('util/glyphs/glyphs.svg')
    return [i.attributes.get('inkscape:label').value for i in doc.documentElement.childNodes if i.nodeName == 'path']

def getAllGlyphs() -> dict[str:Glyph]:
    doc = minidom.parse('util/glyphs/glyphs.svg')
    return {i.attributes.get('inkscape:label').value: Glyph(i.attributes.get('inkscape:label').value, _correctGlyph(_parseGlyph(i.attributes.get('d').value)))
            for i in doc.documentElement.childNodes if i.nodeName == 'path'}


def _getGlyph(name: str) -> list[tuple[int,int]]:
    doc = minidom.parse('util/glyphs/glyphs.svg')
    allGlyphs = {i.attributes.get('inkscape:label').value: i.attributes.get('d').value for i in doc.documentElement.childNodes if i.nodeName == 'path'}
    return _correctGlyph(_parseGlyph(allGlyphs[name].attributes.get('d').value))

def _parseGlyph(ptsstr: str) -> list[tuple[int,int]]:
    cmd = None
    typ = None
    points = []
    for i in ptsstr.split(' '):
        if len(i) == 1:
            typ = (-1 if i == i.upper() else 1)
            i = i.upper()
            if not i in ['M', 'V', 'H', 'L']:
                raise ValueError(
                    'Unable to parse glyph: Incorrectly structured path - command not known!'
                )
            cmd = i
        else:
            if cmd is None:
                raise ValueError(
                    'Unable to parse glyph: Incorrectly structured path - command does not exist!'
                )
            if cmd == 'M':
                points.append(tuple([float(j) for j in i.split(',')]))
            elif cmd == 'V':
                if len(points) == 0:
                    raise ValueError(
                        'Unable to parse glyph: Incorrectly structured path - Cannot move vertically if there\'s nothing to move up from!'
                    )
                points.append((points[-1][0], points[-1][1] + (float(i) * typ)))
            elif cmd == 'H':
                if len(points) == 0:
                    raise ValueError(
                        'Unable to parse glyph: Incorrectly structured path - Cannot move horizontally if there\'s nothing to move horizontally from!'
                    )
                points.append((points[-1][0] + (float(i) * typ), points[-1][1]))
            elif cmd == 'L':
                if len(points) == 0:
                    raise ValueError(
                        'Unable to parse glyph: Incorrectly structured path - Cannot move if there\'s nothing to move from!'
                    )
                i = i.split(',')
                points.append((points[-1][0] + (float(i[0]) * typ), points[-1][1] + (float(i[1]) * typ)))
    return points
            

def _correctGlyph(points: list[tuple[int,int]]) -> list[tuple[int,int]]:
    mi = (min([i[0] for i in points]), min([i[1] for i in points]))
    newpts = [(i[0] - mi[0], i[1] - mi[1]) for i in points]
    ma = max([max([i[0] for i in newpts]), max([i[1] for i in newpts])])
    return [(i[0] / ma, i[1] / ma) for i in newpts]

pass