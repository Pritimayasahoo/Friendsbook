let pid = null;
function showConfirmation(event) {
  const confirmationBox = document.getElementById('confirmationBox');
  const overlay = document.getElementById('overlay');
  // Get the clicked image
  const clickedImage = event.target;

  // Calculate the position of the clicked image
  const rect = clickedImage.getBoundingClientRect();
  const top = rect.top + window.pageYOffset;
  const left = rect.left + window.pageXOffset;
  pid = clickedImage.dataset.postid;

  // Position the confirmation box over the clicked image
  confirmationBox.style.top = top + 'px';
  confirmationBox.style.left = left + 'px';

  // Add blur class to body and show the confirmation box
  document.body.classList.add('blur');
  confirmationBox.classList.remove('hidden');
  overlay.classList.remove('hidden');

  // Prevent click events from propagating to elements behind the confirmation box
  event.stopPropagation();
}

function closeConfirmation() {
  const confirmationBox = document.getElementById('confirmationBox');
  const overlay = document.getElementById('overlay');

  // Remove blur class from body and hide the confirmation box
  document.body.classList.remove('blur');
  confirmationBox.classList.add('hidden');
  overlay.classList.add('hidden');
  pid = null;
}

function deletePhoto() {
  // Perform the delete operation
  // ...
  // Redirect to another page
  window.location.href = `/deletepic/?value=${pid}`;
}