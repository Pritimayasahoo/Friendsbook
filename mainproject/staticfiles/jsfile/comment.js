const uploadForm = document.getElementById('uploadForm');
const uploadid = document.getElementById('hide');
const comment_id = document.getElementById('comment');
console.log(comment_id)
console.log(comment)
const id=uploadid.value
const postUrl = uploadForm.dataset.postUrl;
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
//recent commenter
const commentByInput = document.getElementById('commentBy');
const commentposter = commentByInput.value;

// Function to scroll to the bottom of the comments section
function scrollToBottom() {
  const commentBlock = document.getElementById('comment_block');
  commentBlock.scrollTop = commentBlock.scrollHeight;
}

// Scroll to the bottom on page load (when the DOM is ready)
document.addEventListener('DOMContentLoaded', () => {
  scrollToBottom();
});


console.log(postUrl)
    //const errorDiv = document.getElementById('error-message');
    
    uploadForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const comment=comment_id.value
      const message=comment
      comment_id.value=""
      //const fileInput = document.getElementById('image');
      //const file = fileInput.files[0];
    
      //if (!file) {
      //  errorDiv.textContent = 'Please select an image file.';
      //  return;
      //}
    
      const formData = new FormData();
      formData.append('comment', comment);
      formData.append('id', id);
    
      //let reader = new FileReader();
      //reader.readAsDataURL(file);
    
    
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
                const commentElement = document.createElement('div');
                commentElement.classList.add('comment'); // Ensure it has the same class as other comments

                const commentBy = document.createElement('h1');
                commentBy.textContent = `Comment by: ${commentposter}`;
                const commentmessage=document.createElement('h3')
                commentmessage.textContent=`${message}`
                commentElement.appendChild(commentBy);
                commentElement.appendChild(commentmessage)

                //const commentText = document.createElement('h3');
                //commentText.textContent = newComment.text;
                //commentElement.appendChild(commentText);

                // Append the newly created comment element to the comments section
                const commentsSection = document.getElementById('comment_block');
                commentsSection.appendChild(commentElement);
                //Scrool to bottom
                scrollToBottom();
                // Handle server response here
                //window.location.href = '/';
              })
              .catch((error) => {
                // Handle error
                console.log(error)
              });
    });
    