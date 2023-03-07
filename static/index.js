const inputField = document.querySelector('input[name="url1"]');
const form = document.querySelector('form[action="/downloadZip"]');

// add event listener for form submit
form.addEventListener('submit', function(event) {

  // check if input field is empty
  if (inputField.value.trim() === '') {
    // prevent form submission
    event.preventDefault();
    // add red border to input field
    inputField.classList.add('error');
  } else{
    // remove red border from input field
    inputField.classList.remove('error');
  }
});
const inputField1 = document.querySelector('input[name="url"]');
const form1 = document.querySelector('form[action="/download"]');

// add event listener for form submit
form1.addEventListener('submit', function(event) {

  // check if input field is empty
  if (inputField1.value.trim() === '') {
    // prevent form submission
    event.preventDefault();
    // add red border to input field
    inputField1.classList.add('error');
  } else{
    // remove red border from input field
    inputField1.classList.remove('error');
  }
});

