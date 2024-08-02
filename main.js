document.body.onload = function() {
    const outputDiv = document.getElementById("output");
    document.body.addEventListener('mousedown', function(event) {
        outputDiv.innerHTML += 'Mouse button down!' + JSON.stringify(event) + "<br>";
    });

    document.body.addEventListener('mouseup', function(event) {
        outputDiv.innerHTML += 'Mouse button up!' + JSON.stringify(event) + "<br>";
    });
}
