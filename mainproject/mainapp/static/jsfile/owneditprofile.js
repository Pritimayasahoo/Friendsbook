//profile pic upload btn and cover pic upload btn
const pic_btn=document.getElementById("pic-btn")
const cover_btn=document.getElementById("cover-btn")

//profile pic input btn and cover-pic input btn
const pic_input=document.getElementById("profile-file")
const cover_input=document.getElementById("cover-file")

//remove disable
cover_btn.disabled=false
pic_btn.disabled=false 

//image area for profile and cover pic
const profileimgArea = document.querySelector('.img-area');
const coverimgArea = document.querySelector('.cover-pic')

//name about and school name
const profile_name=document.getElementById("name")
const about=document.getElementById("about")
const school=document.getElementById("school")

//final submission btn
const submit_btn=document.getElementById("submit-btn")
submit_btn.disabled=false; 

//formData for send details to backend by form
let formData=new FormData();

//by click this profile image upload button profile input button will automatically clicked
pic_btn.addEventListener('click', function () {
	pic_input.click();
})


//profile pic input button 
pic_input.addEventListener("change", function (event) {
//at 1st disable the submit button during compress the image
submit_btn.disabled=true;  
const imageData = pic_input.files[0];//image data is the choosen image 
const options = {
maxWidth:900, // Set the maximum width for the compressed image
maxHeight:600, // Set the maximum height for the compressed image
quality: 0.7, // Set the compression quality (0.1 to 1)

//if sucessfully image will compress this sucess will run
success(result) {
        //result.name is the choosen image name
        const compressedprofileImageFile = new File([result], `${result.name}`, { type: 'image/jpeg' }); 

        // Append the data to the FormData object
        formData.append("profile_image", compressedprofileImageFile );
        
        //Url of the compressed image
        const compressedprofileImageURL = URL.createObjectURL(result);//img url

        //Show the image
        const allImg = profileimgArea.querySelectorAll('img');
			  allImg.forEach(item=> item.remove());
			  const imgUrl = compressedprofileImageURL;
      
        const img = document.createElement('img');

            img.src = imgUrl;
			      profileimgArea.appendChild(img);
			      profileimgArea.classList.add('active');
			      profileimgArea.dataset.img = result.name;
        //After compress and show the image again enable the submit button to send the image    
        submit_btn.disabled=false
    }
  };

//At 1st pass the original image and options to compress the image
new ImageCompressor(imageData, options);

//clear the input field value for further use
pic_input.value = '';  
});


//click the cover pic upload button
cover_btn.addEventListener('click', function () {
	cover_input.click();
})

//cover pic input button
cover_input.addEventListener("change", function (event) {
  //at 1st disable the submit button   
  submit_btn.disabled=true;  
  const imageData = cover_input.files[0];//image data is the choosen image 
  const options = {
  maxWidth:900, // Set the maximum width for the compressed image
  maxHeight:600, // Set the maximum height for the compressed image
  quality: 0.7, // Set the compression quality (0.1 to 1)
  
  //if sucessfully image will compress this sucess will run
  success(result) {
          //result.name is the choosen image name
          const compressedcoverImageFile = new File([result], `${result.name}`, { type: 'image/jpeg' }); 
  
          // Append the data to the FormData object
          formData.append("cover_image", compressedcoverImageFile );
          
          //Url of the compressed image
          const compressedcoverImageURL = URL.createObjectURL(result);//img url
  
          //Show the image
          const allImg = coverimgArea.querySelectorAll('img');
          allImg.forEach(item=> item.remove());
          const imgUrl = compressedcoverImageURL;
        
          const img = document.createElement('img');
  
              img.src = imgUrl;
              coverimgArea.appendChild(img);
              coverimgArea.classList.add('active');
              coverimgArea.dataset.img = result.name;
          //After compress and show the image enable the submit button to send the image    
          submit_btn.disabled=false
  
      }
    };
  
  //At 1st pass the original image and options to compress the image
  new ImageCompressor(imageData, options);
  
  //clear the input field value 
  cover_input.value = '';  
  });

  

// Function to get the CSRF token from the cookie
function getCookie(name) {
  let value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
  }    


//send form data to backend  
submit_btn.addEventListener("click",function(e){
 const about_value=about.value;
 const school_value=school.value
 const name_value=profile_name.value
 
 //add value to form
 formData.append("about", about_value);
 formData.append("school", school_value);
 formData.append("name", name_value);

 //send data to backend
 fetch("/profile/", {
   method: "POST",
    headers: {
   // Include the CSRF token in the request header
   'X-CSRFToken':getCookie("csrftoken"),
},
//send form to backend
body: formData,
})
.then((response) => response.json())
.then((data) => {
//disabled submit button
submit_btn.disabled = true;
//go to home page
window.location.href = '/';
})
.catch((error) => {
//disable submit button
submit_btn.disabled = true;
//go to home page
window.location.href = '/';
});
 })
