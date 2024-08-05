// TODO: Auto add all the glyphs in the glyphs folder instead of make them manually on the HTML

document.body.onload = function() {
    var it = document.getElementById("glyph")
    it.addEventListener('mousemove', function(event) {
        console.log("MOUSEMOVE")
        const x = event.clientX;
        const y = event.clientY;
        it.style = `top: ${y};left: ${x}`
    });
}
