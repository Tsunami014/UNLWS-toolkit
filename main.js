// TODO: Auto add all the glyphs in the glyphs folder instead of make them manually on the HTML

var offset = [0,0];
var reload = true;

document.body.onload = function() {
    var it = document.getElementById("glyph")
    it.ondragstart = function() { return false; };
    it.addEventListener('mousemove', function(event) {
        const x = event.clientX;
        const y = event.clientY;
        var flags = event.buttons !== undefined ? event.buttons : event.which;
        if ((flags & 1) === 1) {
            if (reload) {
                // Set offset to mouse position - current position of object, if set
                offset = [x - it.offsetLeft, y - it.offsetTop];
                reload = false;
            }
            it.style = `top: ${y-offset[1]};left: ${x-offset[0]}`
        }
    });
    it.addEventListener("mouseup", function(event){reload = true;});
}
