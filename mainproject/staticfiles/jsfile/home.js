const uploadForm = document.getElementById('like-url');
const postUrl = uploadForm.dataset.postUrl;
const clickimg= document.getElementById('click-img');
const subMenu= document.getElementById("subMenu") 
//click the image for show box
clickimg.addEventListener("click",function(){
  //add this class if not there or remove that
  subMenu.classList.toggle("open-menu")

})

const likeButtons = document.querySelectorAll('.like-me');

  likeButtons.forEach(button => {
    button.addEventListener('click', () => {
      const postId = button.getAttribute('data-post-id');

      // Make an asynchronous request to the Django backend
      fetch(`${postUrl}?like_id=${postId}`)
        .then(response => response.json())
        .then(data => {
          // Update the like count on the frontend
          const likeCountElement = document.getElementById(`like-count-${postId}`);
          if (data.likes==0)
          {
            likeCountElement.textContent = `No like`;
          }
          else if(data.likes==1)
          {
            likeCountElement.textContent =`1 like`; 
          }
          else
          {
            likeCountElement.textContent =`${data.likes} likes`;
          }

        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });