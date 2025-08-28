var dropDown = document.getElementById('first-dropdown'), display2 = document.querySelector('.drop-menu');

dropDown.addEventListener('click', () =>{
    if (display2.style.display === 'none'){
        display2.style.display = 'block'
    }else if (display2.style.display === 'block'){
        display2.style.display = ' none'
    }
})
