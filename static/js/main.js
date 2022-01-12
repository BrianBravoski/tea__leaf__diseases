$(document).ready(function () {
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
               
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-detect').show();
        
        
        readURL(this);
    });


    $('#btn-detect').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                
                
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
            },

        })
    
    });

});