var dropDown = document.getElementById('first-dropdown'), display1 = document.querySelector('.drop-menu');

dropDown.addEventListener('click', () =>{
    if (display1.style.display === 'none'){
        display1.style.display = 'block'
    }else if (display1.style.display === 'block'){
        display1.style.display = ' none'
    }
})