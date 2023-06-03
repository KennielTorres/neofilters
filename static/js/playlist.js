
window.onload = function() {
    let menu_toggle = document.getElementById('filter-toggle');
    let options_parent_div = document.getElementById('options-parent');
    let filter_options_block = document.getElementById('filtering_options');
    let menu_arrow = document.getElementById('toggle-arrow-img'); 
    
    menu_toggle.onclick = function() {
        if (this.checked){
            options_parent_div.style.display = 'block'
            filter_options_block.style.display = 'block'
            menu_arrow.classList.remove('turn-up')
            menu_arrow.classList.add('turn-down')

        }
        else {
            options_parent_div.style.display = 'none'
            filter_options_block.style.display = 'none'
            menu_arrow.classList.remove('turn-down')
            menu_arrow.classList.add('turn-up')
        }
    };
};


