$(function () {
    let cords = ['scrollX', 'scrollY'];
    window.scroll(...cords.map(cord => localStorage[cord]));

    $('.page_link').click(function (e) {
        e.preventDefault();
        let page = ((e.currentTarget.dataset.page));
        $('#id_page').val(page);
        $('form').submit();
    });

    $('form').submit(function () {
        let cords = ['scrollX', 'scrollY'];
        window.addEventListener('unload', e => cords.forEach(cord => localStorage[cord] = window[cord]));
    });

    $('.django_forms select').removeAttr('required');
    $('.django_forms input').removeAttr('required');

    $(".django_forms").find('input[type=text]').change(function (e) {
        $('#id_page').val(1);
        let forma = $(e.target).parents("form");
        let cords = ['scrollX', 'scrollY'];
        window.addEventListener('unload', e => cords.forEach(cord => localStorage[cord] = window[cord]));
        forma.submit();
    });

    $(".django_forms").find('input[type=date]').blur(function (e) {
        $('#id_page').val(1);
        let forma = $(e.target).parents("form");
        let cords = ['scrollX', 'scrollY'];
        window.addEventListener('unload', e => cords.forEach(cord => localStorage[cord] = window[cord]));
        forma.submit();
    });

    $(".django_forms").find('select').change(function (e) {
        $('#id_page').val(1);
        let forma = $(e.target).parents("form");
        let cords = ['scrollX', 'scrollY'];
        window.addEventListener('unload', e => cords.forEach(cord => localStorage[cord] = window[cord]));
        forma.submit();
    });

    $(".btn_sbros_poiska").click(function (e) {
        document.location.href = "/";
    });


});