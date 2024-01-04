const input=document.getElementById("files")
const btn=document.getElementById("btn")
btn.disabled=false
const imgArea = document.querySelector('.img-area');
const about=document.getElementById("about")
const submit_btn=document.getElementById("submit")
let formData
//by click the select image button input file button will click automatically
btn.addEventListener('click', function () {
	input.click();
})

//if any photo will choosen
input.addEventListener("change", function (event) {
//at 1st disable the submit button   
submit_btn.disabled=true;  
const imageData = input.files[0];//image data is the choosen image 
const options = {
  maxWidth:900, // Set the maximum width for the compressed image
  maxHeight:600, // Set the maximum height for the compressed image
  quality: 0.7, // Set the compression quality (0.1 to 1)
  
  //if sucessfully image will compress this sucess will run
  success(result) {
          //result.name is the choosen image name
          const compressedImageFile = new File([result], `${result.name}`, { type: 'image/jpeg' }); 
  
          // Append the data to the FormData object
          formData = new FormData();
          formData.append("image_data", compressedImageFile);
          
          //Url of the compressed image
          const compressedImageURL = URL.createObjectURL(result);//img url
  
          //Show the image
          const allImg = imgArea.querySelectorAll('img');
          allImg.forEach(item=> item.remove());
          const imgUrl = compressedImageURL;
        
          const img = document.createElement('img');
  
              img.src = imgUrl;
              img.onload=function()
              { 
              //modify image height for suitable view    
              const aspectRatio = img.width / img.height;
              const containerWidth = imgArea.offsetWidth;
              const calculatedHeight = containerWidth / aspectRatio;
              img.style.height = `${calculatedHeight}px`; // Set the calculated height
              imgArea.style.height = `${calculatedHeight}px`;
              imgArea.appendChild(img);
              imgArea.classList.add('active');
              imgArea.dataset.img = result.name;
              }
          //After compress and show the image enable the submit button to send the image    
          submit_btn.disabled=false
  
      }
    };
  
  //At 1st pass the original image and options to compress the image
  new ImageCompressor(imageData, options);
  
//clear the input field value 
input.value = '';  
});
// Function to get the CSRF token from the cookie
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
  }    


     //After sucessfully  compress image send the compressed image
     submit_btn.addEventListener("click",function(e){
      const textData=about.value
      //about.value=''
      //add the text data into it
      formData.append("text_data", textData);

      // Fetch the Django backend URL and send the data using the POST method
      fetch("/save/", {
        method: "POST",
         headers: {
        // Include the CSRF token in the request header
        'X-CSRFToken':getCookie("csrftoken"),
     },
     //pass the form to Django
     body: formData,
   })
     .then((response) => response.json())
     .then((data) => {
       //Again disabled the submit button
       submit_btn.disabled = true;
       //after send the image go to home 
       window.location.href = '/';
     })
     .catch((error) => {
       //disable the submit button
       submit_btn.disabled = true;
       window.location.href = '/';
     });
    })






   