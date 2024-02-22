const uploadForm = document.getElementById('like-url');
const postUrl = uploadForm.dataset.postUrl;
const clickimg = document.getElementById('click-img');
const subMenu = document.getElementById("subMenu")
//click the image for show box
clickimg.addEventListener("click", function () {
  //add this class if not there or remove that
  subMenu.classList.toggle("open-menu")

})
// Send Lie status to backend asynchronously
const Like_send = async function (postUrl, postId) {
  try {
    const response = await fetch(`${postUrl}?like_id=${postId}`)

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json()
    // Update the like count on the frontend
    const likeCountElement = document.getElementById(`like-count-${postId}`);
    if (data.likes == 0) {
      likeCountElement.textContent = `No like`;
    }
    else if (data.likes == 1) {
      likeCountElement.textContent = `1 like`;
    }
    else {
      likeCountElement.textContent = `${data.likes} likes`;
    }

  }
  catch (error) {
    console.error('There was a problem fetching the data:', error);
  }

}

const likeButtons = document.querySelectorAll('.like-me');
likeButtons.forEach(button => {
  button.addEventListener('click', () => {
    const postId = button.getAttribute('data-post-id');
    Like_send(postUrl, postId)
  });
});