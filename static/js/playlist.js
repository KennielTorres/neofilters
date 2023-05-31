
window.onload = function() {
    let menu_toggle = document.getElementById('menu-toggle');
    let side_container = document.getElementById('side_container')
    
    menu_toggle.onclick = function() {
        if (this.checked){
            console.log('checkbox ON')
            side_container.classList.toggle('menu-slide')
        }
        else {
            console.log('checkbox OFF')
    
        }
    };
};

// Figure out how to use this, this onclick is not working
// console.log(menu_toggle)

