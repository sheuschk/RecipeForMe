/* Javascript for app*/
window.addEventListener('load', function () {
    "use strict";


    $('#name').change(function () {
        let name = $(this).val();
        let url = this.parentElement.getAttribute('data-ajax');
        console.log(url);
        $.ajax({
            url: url,
            data: {'cocktail_name': name},
            dataType: 'json',
            success: function (data) {
                if (data.is_taken === true){
                    alert('taken')
                }
            }
        })
    });


    let all_ings = document.querySelectorAll('.ing_wrapper');
    let count = 0;
    for (let ing of all_ings) {
        if (count > 1){
            ing.style.display = "None";
        }
        count++
    }


    let plus_sign = document.getElementById('plus_sign');
    // plus_sign.style.display = 'block';
    plus_sign.onclick = add_field;

    function add_field() {
        let ing_array = [];
        console.log('add');
        let ing_fields = document.querySelectorAll('.ing_wrapper');
        for (let ing of ing_fields){
            if (ing.style.display === 'none'){
                ing_array.push(ing)
            }
        }
        console.log(ing_array);

        let new_field = ing_array.shift();
        new_field.style.display = 'block';

        console.log(ing_array.length);
        if (ing_array.length === 1 ){
            plus_sign.style.display = 'None';
            plus_sign.disabled = 'disabled';
        }
    }

});


let form = document.getElementById('search_filter_form');
form.onchange = check_field;
function check_field(){
    console.log('jump');
    form.submit()
}