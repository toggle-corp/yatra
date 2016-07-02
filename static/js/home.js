$(document).ready(function(){
    $('#register-link').on('click', function(){
        $('#signin-form').slideUp(500, function(){
            $('#register-form').slideDown();
        });
    });
    $('#signin-link').on('click', function(){
        $('#register-form').slideUp(500, function(){
            $('#signin-form').slideDown();
        });
    });
});
