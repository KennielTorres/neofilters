let menu_toggle = document.getElementsByClassName('menu-toggle');

window.onload = function() {
    console.log('page has loaded')
    
};

// Figure out how to use this, this onclick is not working
console.log(menu_toggle)
menu_toggle.onclick = function() {
    console.log('onclick')
    if (this.checked){
        console.log('checkbox toggled')
    }
    else {
        console.log('checkbox OFF')

    }
};
