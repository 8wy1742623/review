var show_another = function(div1, div2) {
    log(div1.style.display)
    log(div2.style.display)
    div1.style.display = 'None'
    div2.style.display = ''
}

var flip_over = function() {
    d1 = e('#d1')
    d2 = e('#d2')
    flip_btn = e('#flip_over')

    flipped = 0
    flip_btn.addEventListener("click", function(event) {
        if (flipped == 0) {
            show_another(d1, d2)
            flip_btn.innerText = 'Hide Back'
            flipped = 1
        }
        else {
            show_another(d2, d1)
            flip_btn.innerText = 'Show Back'
            flipped = 0
        }
    })
}


var __main = function() {
    flip_over()
}


__main()
