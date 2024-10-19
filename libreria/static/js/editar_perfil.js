document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_profile_picture');
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = function() {
            const userPic = document.getElementById('userPic');
            userPic.src = reader.result;
        }
        if (file) {
            reader.readAsDataURL(file);
        }
    });
});