const dom = document;
dom.addEventListener('DOMContentLoaded', function (){
    const all_button = dom.querySelector('#all_li');
    const current_button = dom.querySelector('#current_li');
    const newest_button = dom.querySelector('#newest_li');
    const expected_button = dom.querySelector('#expected_li');
    const past_button = dom.querySelector('#past_li');
    const cancelled_button = dom.querySelector('#cancelled_li');
    const reservationLists = Array.from(dom.querySelectorAll('.reservation'));
    function displayNone(list) {
        list.forEach(function (el){
        el.style.display = 'none';
        });
    }
    displayNone(reservationLists)

    expected_button.addEventListener('click', function(){
        displayNone(reservationLists)
        const d = dom.querySelector('#expected_div')
        d.style.display = 'block'
        });
    current_button.addEventListener('click', function(){
        displayNone(reservationLists)
        const d = dom.querySelector('#current_div')
        d.style.display = 'block'
    });
    all_button.addEventListener('click', function(){
        displayNone(reservationLists)
        const d = dom.querySelector('#all_div')
        d.style.display = 'block'
    });
    newest_button.addEventListener('click', function(){
        displayNone(reservationLists)
        const d = dom.querySelector('#newest_div')
        d.style.display = 'block'
    });
    past_button.addEventListener('click', function(){
        displayNone(reservationLists)
        const d = dom.querySelector('#past_div')
        d.style.display = 'block'
    });
    cancelled_button.addEventListener('click', function(){
        displayNone(reservationLists)
        const d = dom.querySelector('#cancelled_div')
        d.style.display = 'block'
    });

});
