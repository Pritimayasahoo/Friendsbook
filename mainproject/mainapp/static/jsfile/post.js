const uploadForm = document.getElementById('uploadForm');

//Pass the url from html and use that in here as now our js file is in different folder(inside static folder)
const postUrl = uploadForm.dataset.postUrl;
//use csrf token
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

console.log(postUrl)
    const errorDiv = document.getElementById('error-message');
    
    uploadForm.addEventListener('submit', (event) => {
      event.preventDefault();
    
      const fileInput = document.getElementById('image');
      const file = fileInput.files[0];
    
      if (!file) {
        errorDiv.textContent = 'Please select an image file.';
        return;
      }
    
      const formData = new FormData();
      formData.append('image', file);
    
      let reader = new FileReader();
      reader.readAsDataURL(file);
    
      reader.onload = (event) => {
        const image = new Image();
        image.src = event.target.result;
    
        image.onload = () => {
          const canvas = document.createElement('canvas');
          const maxImageSize = 800; // Maximum dimension for the compressed image
          let width = image.width;
          let height = image.height;
    
          // Calculate new dimensions while maintaining aspect ratio
          if (width > height && width > maxImageSize) {
            height *= maxImageSize / width;
            width = maxImageSize;
          } else if (height > width && height > maxImageSize) {
            width *= maxImageSize / height;
            height = maxImageSize;
          }
    
          canvas.width = width;
          canvas.height = height;
    
          const context = canvas.getContext('2d');
          context.drawImage(image, 0, 0, width, height);
    
          canvas.toBlob((blob) => {
            formData.append('compressedImage', blob, 'compressed.jpg');
            
            //use the url postUrl(grab on the top) to go to the postviews
            fetch(postUrl, {
              method: 'POST',
              headers: {
                'X-CSRFToken': csrfToken,
              },
              body: formData,
            })
              .then((response) => {
                console.log(response)
                // Handle server response here
                window.location.href = '/';
              })
              .catch((error) => {
                // Handle error
                console.log(error)
              });
          }, 'image/jpeg', 0.999);
        };
      };
    });
    