document.addEventListener('DOMContentLoaded', function() {
    const uploadButton = document.getElementById('upload-button');
    const profilePicture = document.getElementById('profile-picture');
  
    profilePicture.addEventListener('click', function() {
      uploadButton.click();
    });
  
    uploadButton.addEventListener('change', function(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
  
      reader.onload = function() {
        profilePicture.src = reader.result;
      };
  
      if (file) {
        reader.readAsDataURL(file);
      }
    });
  });