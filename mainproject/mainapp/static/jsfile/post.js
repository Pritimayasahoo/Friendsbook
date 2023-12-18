 // ... Your previous code ...
//const uploadForm = document.getElementById('uploadForm');
//Pass the url from html and use that in here as now our js file is in different folder(inside static folder)
//const postUrl = uploadForm.dataset.postUrl;
//use csrf token
//const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
document.getElementById("infile").disabled = false;
document.getElementById("infile").addEventListener("change", function (event) {
  const imageData = document.querySelector("[name='image_data']").files[0];
  const text = document.querySelector("[name='text_data']");
  const options = {
    maxWidth:900, // Set the maximum width for the compressed image
    maxHeight:600, // Set the maximum height for the compressed image
    quality: 0.7, // Set the compression quality (0.1 to 1)
    success(result) {
      // ... Your previous success function ...
      // Display the compressed image in the container
      console.log(result)
        //const compressedImageBlob = dataURLtoBlob(result);
        const compressedImageFile = new File([result], 'compressed.jpg', { type: 'image/jpeg' });
        console.log(compressedImageFile) 

        // Append the data to the FormData object
        const formData = new FormData();
        //formData.append("text_data", textData);
        formData.append("image_data", compressedImageFile);

      const compressedImageContainer = document.getElementById('compressedImageContainer');
      const compressedImage = document.getElementById('compressedImage');
      //compressedImage.disabled = false;
      const compressedImageURL = URL.createObjectURL(result);
      compressedImage.style.display = 'block';
      compressedImage.src =compressedImageURL;
      //compressedImageContainer.innerHTML = `<img src="${compressedImageURL}" alt="Compressed Image">`;

      // Enable the submit button
      document.getElementById("submit").disabled = false;
      document.getElementById("submit").addEventListener("click",function(e){
        e.preventDefault()
        const textData=text.value
        console.log(textData)
        formData.append("text_data", textData);
        // Fetch the Django backend URL and send the data using the POST method
        fetch("/save/", {
          method: "POST",
           headers: {
          // Include the CSRF token in the request header
          'X-CSRFToken':getCookie("csrftoken"),
       },
       body: formData,
     })
       .then((response) => response.json())
       .then((data) => {
         // Handle the response from the Django backend (if needed)
         console.log(data);
         document.getElementById("submit").disabled = true;
         document.getElementById("infile").disabled = false;
         window.location.href = '/';
         //compressedImageContainer.innerHTML = ``;

       })
       .catch((error) => {
         console.error("Error:", error);
         document.getElementById("submit").disabled = true;
         document.getElementById("infile").disabled = false;
         window.location.href = '/';
         //compressedImageContainer.innerHTML = ``;

       });
      })
    },
    error(e) {
      console.log('Error:', e.message);
    },
  };
  new ImageCompressor(imageData, options);
  
// Function to get the CSRF token from the cookie
function getCookie(name) {
var value = "; " + document.cookie;
var parts = value.split("; " + name + "=");
if (parts.length === 2) return parts.pop().split(";").shift();
}

  // Disable the input and submit buttons during the asynchronous task
  document.getElementById("infile").disabled = true;
  document.getElementById("submit").disabled = true;
});


