(function($) {
    $(document).ready(function($) {
        setTimeout(function(){
            var wdg = document.getElementsByClassName("django-ckeditor-widget")[0];
            var txt = document.getElementById("id_content");
            var cke = document.getElementById("cke_id_content"); // cke div
            var elements = [wdg, txt, cke];

            for(var idx = 0; idx < elements.length; idx++) {
                elements[idx].style.width = "100%";
            }
        }, 1000);
    });
})(django.jQuery);
