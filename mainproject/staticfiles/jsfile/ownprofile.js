const WIDTH = 800;
const profileForm = document.getElementById('profileForm');
const errorDiv = document.getElementById('error-message');

profileForm.addEventListener('submit', (event) => {
  event.preventDefault();
  
  const fileInput = document.getElementById('profilepic');
  const file = fileInput.files[0];
  
  let formData = new FormData();
  formData.append('name', document.getElementById('name').value);
  formData.append('about', document.getElementById('about').value);
  formData.append('school', document.getElementById('school').value);
  
  if (!file) {
    errorDiv.textContent = 'Please select an image file.';
    return;
  }
  
  let reader = new FileReader();
  reader.readAsDataURL(file);
  
  reader.onload = (event) => {
    let image = new Image();
    image.src = event.target.result;
    
    image.onload = (e) => {
      let canvas = document.createElement('canvas');
      let ratio = WIDTH / e.target.width;
      canvas.width = WIDTH;
      canvas.height = e.target.height * ratio;
      
      const context = canvas.getContext('2d');
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      
      let compressedImage = canvas.toDataURL('image/jpeg', 5);
      
      formData.append('compressed_image', dataURLtoFile(compressedImage, 'compressed.jpg'));
      
      fetch('/profile/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData,
      })
      .then((response) => {
        // Handle server response here
        // Redirect to desired location
        window.location.href = '/';
      })
      .catch((error) => {
        // Handle error
      });
    };
  };
});

// Helper function to convert data URL to a File object
function dataURLtoFile(dataURL, filename) {
  const arr = dataURL.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new File([u8arr], filename, { type: mime });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}