const uploadForm = document.getElementById('like-url');
const postUrl = uploadForm.dataset.postUrl;
const lazyImages = document.querySelectorAll('.lazy-image');

const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const image = entry.target;
      const imageUrl = image.getAttribute('data-src');

      // Calculate the index of the image within the lazyImages array
      const currentIndex = Array.from(lazyImages).indexOf(image);

      // Calculate the index of the image before the current image
      const prevIndex = Math.max(currentIndex - 1, 0);

      // Get the image that should be loaded before the current image
      const prevImage = lazyImages[prevIndex];

      // Load the previous image before the current image
      if (prevImage) {
        const prevImageUrl = prevImage.getAttribute('data-src');
        prevImage.setAttribute('src', prevImageUrl);
      }

      // Load the current image
      image.setAttribute('src', imageUrl);

      // Add a loading blur effect
      image.classList.add('loading');

      // Listen for the load event on the current image
      image.addEventListener('load', () => {
        // Remove the loading blur effect
        image.classList.remove('loading');
      });

      observer.unobserve(image);
    }
  });
});

lazyImages.forEach((lazyImage) => {
  imageObserver.observe(lazyImage);
});

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
          likeCountElement.textContent = data.likes;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
