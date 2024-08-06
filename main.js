// TODO: Auto add all the glyphs in the glyphs folder instead of make them manually on the HTML

var offset = [0,0];
var reload = true;
var current = null;
var cover;

document.body.onload = function() {
    cover = document.getElementById("cover");
    cover.style = "display: none;";
    cover.addEventListener("mouseup", function(event){
        cover.style = "display: none;";
        reload = true;
        current = null;
    })
    cover.addEventListener("mousemove", function(event){
        if (current !== null) {
            const x = event.clientX;
            const y = event.clientY;
            current.style = `top: ${y-offset[1]};left: ${x-offset[0]}`
        }
    })
    var it = document.getElementById("glyph")
    it.ondragstart = function() { return false; };
    it.addEventListener('mousemove', function(event) {
        const x = event.clientX;
        const y = event.clientY;
        var flags = event.buttons !== undefined ? event.buttons : event.which;
        if ((flags & 1) === 1) {
            if (current === null) {
                current = it;
                cover.style = "display: block;";
            }
            if (reload) {
                // Set offset to mouse position - current position of object, if set
                offset = [x - it.offsetLeft, y - it.offsetTop];
                reload = false;
            }
            it.style = `top: ${y-offset[1]};left: ${x-offset[0]}`
        }
    });
    it.addEventListener("mouseup", function(event){
        cover.style = "display: none;";
        reload = true;
        current = null;
    });
}
