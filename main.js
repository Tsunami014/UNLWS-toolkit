// TODO: Auto add all the glyphs in the glyphs folder instead of make them manually on the HTML

var offset = [0,0];
var reload = true;
var current = null;
var cover;
var bincover;
var sidebarh = 10;

function reset() {
    if (parseInt(current.style.left.slice(0,current.style.left.indexOf("px"))) < document.getElementById("sidebar").getBoundingClientRect().right) {
        current.parentElement.removeChild(current);
    }
    cover.style = "display: none;";
    bincover.style = "display: none;";
    reload = true;
    current = null;
}

function addGlyph(glyph, position=[0,0]) {
    var it = document.createElement("img");
    it.classList.add("glyph");
    it.src = `glyphs/${glyph}.svg`;
    it.width = 100;
    it.height = 100;
    it.style.left = position[0];
    it.style.top = position[1];
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
            if (current === it) {
                if (reload) {
                    // Set offset to mouse position - current position of object, if set
                    offset = [x - it.offsetLeft, y - it.offsetTop];
                    reload = false;
                }
                it.style = `top: ${y-offset[1]};left: ${x-offset[0]}`
                if (x-offset[0] < document.getElementById("sidebar").getBoundingClientRect().right) {
                    bincover.style = "display: block;";
                } else {
                    bincover.style = "display: none;";
                }
            }
        }
    });
    it.addEventListener("mouseup", function(event){
        reset();
    })
    return it;
}

function addGlyphToSidebar(glyph) {
    var sidebar = document.getElementById("sidebar");
    // Make a new glyph and centre it on the sidebar
    var it = document.createElement("img");
    it.classList.add("glyph");
    it.src = `glyphs/${glyph}.svg`;
    it.width = 100;
    it.height = 100;
    it.style.left = (sidebar.clientWidth - 100) / 2;
    it.style.top = sidebarh;
    it.ondragstart = function() { return false; };
    it.addEventListener('mousemove', function(event) {
        const x = event.clientX;
        const y = event.clientY;
        var flags = event.buttons !== undefined ? event.buttons : event.which;
        if ((flags & 1) === 1) {
            if (current === null) {
                var bbox = it.getBoundingClientRect();
                var newit = addGlyph(glyph, [bbox.left, bbox.top]);
                offset = [x - bbox.left, y - bbox.top];
                reload = false;
                current = newit;
                document.getElementById("main").appendChild(newit);
                cover.style = "display: block;";
            }
        }
    });
    sidebar.appendChild(it);
    sidebarh += 110;
    return it;
}

document.body.onload = function() {
    cover = document.getElementById("cover");
    bincover = document.getElementById("bincover")
    cover.style = "display: none;";
    bincover.style = "display: none;";
    cover.addEventListener("mouseup", function(event){reset();});
    cover.addEventListener("mousemove", function(event){
        if (current !== null) {
            const x = event.clientX;
            const y = event.clientY;
            current.style = `top: ${y-offset[1]};left: ${x-offset[0]}`
            if (x-offset[0] < document.getElementById("sidebar").getBoundingClientRect().right) {
                bincover.style = "display: block;";
            } else {
                bincover.style = "display: none;";
            }
        }
    })
    fetch('glyphs/').then(resp=>{resp.text().then(txt=>{
        var el = document.createElement('html');
        el.innerHTML = txt;
        var files = el.getElementsByTagName('a');
        for (var i = 0;i < files.length;i++) {
            var href = files[i].href;
            if (href.endsWith('.svg')) {
                addGlyphToSidebar(href.slice(href.lastIndexOf("/")+1, href.lastIndexOf(".")));
            }
        }
    })});
}