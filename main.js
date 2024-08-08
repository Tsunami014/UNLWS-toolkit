var offset = [0,0];
var reload = true;
var current = null;
var bincover;
var selected = null;
var glyphs;

var menu = {
    "File": {
        "Save": function(){alert("You saved something!")},
        "Save As": function(){alert("You saved something as something else!")},
        "Open": function(){alert("You opened something!")}
    },
    "Edit": {
        "Cut": function(){alert("You cut something!")},
        "Copy": function(){alert("You copied something!")},
        "Paste": function(){alert("You pasted something!")}
    }
}

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

function addGlyph(g, position=[0,0]) {
    var it = document.createElement("div");
    it.classList.add("glyph");
    it.style.left = position[0];
    it.style.top = position[1];
    var img = document.createElement("img");
    it.appendChild(img);
    img.src = "glyphs/"+(glyphs[g].filename || (g + ".svg"));
    img.width = 100;
    img.height = 100;
    if (glyphs[g].description !== null) {
        var tooltip = document.createElement("span");
        it.appendChild(tooltip);
        tooltip.classList.add("tooltiptext");
        tooltip.classList.add("unselectable");
        tooltip.innerText = glyphs[g].description;
    }
    img.ondragstart = function() { return false; };
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

function addGlyphToSidebar(g) {
    var sidebar = document.getElementById("sidebar");
    // Make a new glyph and centre it on the sidebar
    var it = document.createElement("div");
    it.classList.add("sidebarGlyph");
    it.classList.add("glyph")
    var img = document.createElement("img");
    it.appendChild(img)
    img.src = "glyphs/"+(glyphs[g].filename || (g + ".svg"));
    img.width = 100;
    img.height = 100;
    if (glyphs[g].description !== null) {
        var tooltip = document.createElement("span");
        it.appendChild(tooltip);
        tooltip.classList.add("tooltiptext");
        tooltip.classList.add("unselectable");
        tooltip.classList.add("alwaysOn");
        tooltip.innerText = glyphs[g].description;
    }
    img.ondragstart = function() { return false; };
    it.addEventListener('mousemove', function(event) {
        const x = event.clientX;
        const y = event.clientY;
        var flags = event.buttons !== undefined ? event.buttons : event.which;
        if ((flags & 1) === 1) {
            if (current === null) {
                var bbox = it.getBoundingClientRect();
                var newit = addGlyph(g, [bbox.left, bbox.top]);
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

document.body.onload = async function() {
    var resp = await fetch('glyphs/info.json')
    glyphs = await resp.json()
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
                rotate(selected.children[0], (parseInt(selected.children[0].style.transform.slice(7, -4))||0)+15);
            } else if (event.key === 'ArrowLeft' || event.key === 'a') {
                rotate(selected.children[0], (parseInt(selected.children[0].style.transform.slice(7, -4))||0)-15);
            } else if (event.key === 'Delete' || event.key === 'Backspace') {
                selected.parentElement.removeChild(selected);
                selected = null;
            }
        }
    })
    document.addEventListener("contextmenu",function(event){
        if (window.location.hash === "") {
            event.preventDefault();
            var ctxMenu = document.getElementById("ctxMenu");
            ctxMenu.innerHTML = "";
            for (let menulist in menu) {
                var newMenu = document.createElement("menu");
                newMenu.title = menulist;
                for (let menuitem in menu[menulist]) {
                var menuchild = document.createElement("menu");
                menuchild.title = menuitem;
                menuchild.onclick = menu[menulist][menuitem];
                newMenu.appendChild(menuchild);
                }
                ctxMenu.appendChild(newMenu);
            }
            ctxMenu.style.display = "block";
            ctxMenu.style.left = (event.pageX - 10)+"px";
            ctxMenu.style.top = (event.pageY - 10)+"px";
        }
    }, false);
    document.addEventListener("click",function(event){
        var ctxMenu = document.getElementById("ctxMenu");
        ctxMenu.style.display = "";
        ctxMenu.style.left = "";
        ctxMenu.style.top = "";
    }, false);

    for (var g in glyphs) {
        addGlyphToSidebar(g);
    }
}