
window.onload = function() {
    let menu_toggle = document.getElementById('filter-toggle');
    let filter_options_block = document.getElementById('filtering_options')
    
    menu_toggle.onclick = function() {
        if (this.checked){
            console.log('menu toggle ON')
            filter_options_block.style.display = 'block'
        }
        else {
            console.log('menu toggle OFF')
            filter_options_block.style.display = 'none'
        }
    };
};


