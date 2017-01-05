var current = 0;
var loading_img = "/static/images/loading.gif";

function modulo(m, n) {
    if(m > 0){
        return m % n;
    } else {
        return (m + n) % n;
    }
}

function show_photo(ID) {
    current = ID;

    var disp = document.getElementById("display");
    var img = document.getElementById("photo-img");
    var desc = document.getElementById("photo-description");

    img.src = loading_img;
    
    img.src = photos.url[current];
    desc.innerHTML = photos.dsc[current];

    disp.style.display = "block";
};

function close_preview() {
    var disp = document.getElementById("display");

    disp.style.display = "none";
};

function next_photo() {
    show_photo(modulo(current + 1, count));
};

function prev_photo() {
    show_photo(modulo(current - 1, count));
};
