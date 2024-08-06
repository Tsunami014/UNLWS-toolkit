var offset = [0,0];
var reload = true;
var current = null;
var bincover;
var selected = null;

function glyphMouseUp() {
    if (current !== null) {
        if (parseInt(current.style.left.slice(0,current.style.left.indexOf("px"))) < document.getElementById("sidebar").getBoundingClientRect().right) {
            current.parentElement.removeChild(current);
        }
        current = null;
    }
    bincover.style = "display: none;";
    reload = true;
}

function glyphMouseMove(event) {
    if (current !== null) {
        const x = event.clientX;
        const y = event.clientY;
        var flags = event.buttons !== undefined ? event.buttons : event.which;
        if ((flags & 1) === 1) {
            if (reload) {
                // Set offset to mouse position - current position of object, if set
                offset = [x - current.offsetLeft, y - current.offsetTop];
                reload = false;
            }
            current.style.top = `${y-offset[1]}px`;
            current.style.left = `${x-offset[0]}px`;
            //current.style = `top: ${y-offset[1]};left: ${x-offset[0]}`
            if (x-offset[0] < document.getElementById("sidebar").getBoundingClientRect().right) {
                bincover.style = "display: block;";
            } else {
                bincover.style = "display: none;";
            }
        }
    }
}

function rotate(elm, deg) {
    elm.style.transform = `rotate(${deg}deg)`;
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
    it.addEventListener("dblclick", function (event) {
        if (selected !== null) {
            selected.classList.remove('selected');
        }
        selected = it;
        it.classList.add('selected');
    }); 
    it.addEventListener('mousemove', function(event) {
        var flags = event.buttons !== undefined ? event.buttons : event.which;
        if ((flags & 1) === 1) {
            if (current === null) {
                current = it;
            }
            glyphMouseMove(event);
        }
    });
    it.addEventListener("mouseup", function(event){ glyphMouseUp(); })
    return it;
}

function addGlyphToSidebar(glyph) {
    var sidebar = document.getElementById("sidebar");
    // Make a new glyph and centre it on the sidebar
    var it = document.createElement("img");
    it.classList.add("sidebarGlyph");
    it.classList.add("glyph")
    it.src = `glyphs/${glyph}.svg`;
    it.width = 100;
    it.height = 100;
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
            }
        }
    });
    sidebar.appendChild(it);
    return it;
}

document.body.onload = function() {
    bincover = document.getElementById("bincover")
    bincover.style = "display: none;";
    document.addEventListener("mousedown", function(event) {
        if (selected !== null) {
            selected.classList.remove('selected');
        }
        selected = null;
    })
    document.addEventListener("mouseup", function(event){ glyphMouseUp(); });
    document.addEventListener("mousemove", function(event){ glyphMouseMove(event); })
    document.addEventListener("keydown", function(event){
        if (selected !== null) {
            if (event.key === 'ArrowRight' || event.key === 'd') {
                rotate(selected, (parseInt(selected.style.transform.slice(7, -4))||0)+15);
            } else if (event.key === 'ArrowLeft' || event.key === 'a') {
                rotate(selected, (parseInt(selected.style.transform.slice(7, -4))||0)-15);
            } else if (event.key === 'Delete' || event.key === 'Backspace') {
                selected.parentElement.removeChild(selected);
                selected = null;
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