import pygame
from xml.dom import minidom
from svg.path import parse_path

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
        pygame.draw.lines(sur, colour, False, [(i[0] * size + pos[0], i[1] * size + pos[1]) for i in self.points], line_thickness)

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
