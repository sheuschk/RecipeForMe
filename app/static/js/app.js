/* Javascript for app*/
window.addEventListener('load', function () {
    "use strict";

    $('#name').change(function () {
        let name = $(this).val();
        $.ajax({
            url: '/ajax/validate_cocktail/',
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
    for (let ing of all_ings) {
        ing.style.visibility = "hidden";
    }

});