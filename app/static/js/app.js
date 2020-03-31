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
    })

});