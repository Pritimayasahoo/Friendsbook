const uploadForm = document.getElementById('uploadForm');
const uploadid = document.getElementById('hide');
const comment_id = document.getElementById('comment');
const id = uploadid.value
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


//Asynchronously send comment to backend
let Send_comment = async function (postUrl, formData, comment) {
  try {
    const response = await fetch(postUrl, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      body: formData,
    })

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const commentElement = document.createElement('div');
    commentElement.classList.add('comment'); // Ensure it has the same class as other comments

    const commentBy = document.createElement('h1');
    commentBy.textContent = `comment by: ${commentposter}`;
    const commentmessage = document.createElement('h3')
    commentmessage.textContent = `${comment}`
    commentElement.appendChild(commentBy);
    commentElement.appendChild(commentmessage)


    // Append the newly created comment element to the comments section
    const commentsSection = document.getElementById('comment_block');
    commentsSection.appendChild(commentElement);
    //Scrool to bottom
    scrollToBottom();

  }
  catch (error) {
    console.error('There was a problem fetching the data:', error);
  }

}


uploadForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const comment = comment_id.value
  comment_id.value = ""
  const formData = new FormData();
  formData.append('comment', comment);
  formData.append('id', id);
  //Send Message Asynchronously
  Send_comment(postUrl, formData, comment)

});



