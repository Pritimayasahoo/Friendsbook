const uploadForm = document.getElementById('uploadForm');
const uploadid = document.getElementById('hide');
const comment_id = document.getElementById('comment');
const id = uploadid.value
const postUrl = uploadForm.dataset.postUrl;
const recentUser = document.getElementById("hidden");
const profileImageUrl = document.getElementById("profileImageUrl").value;
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
//recent comment poster
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

    const comment_profile = document.createElement('div')
    comment_profile.classList.add('comment-profile')

    const img = new Image();
    img.src = profileImageUrl;

    const commentBy = document.createElement('p');
    commentBy.textContent = `${commentposter}`;
    const commentmessage = document.createElement('h4')
    commentmessage.textContent = `${comment}`

    comment_profile.appendChild(img)
    comment_profile.appendChild(commentBy)
    comment_profile.appendChild(commentmessage)

    commentElement.appendChild(comment_profile);

    // Append the newly created comment element to the comments section
    const commentsSection = document.getElementById('comment_block');
    commentsSection.appendChild(commentElement);
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



