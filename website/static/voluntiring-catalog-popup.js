var modal = document.getElementById('email-modal');
var btns = document.querySelectorAll('.organnization-list-item-button'); 
const closeBtn = document.querySelector('.close-btn');
const sumbit = document.querySelectorAll ('.modal-input-btn');

[].forEach.call(btns, function(el) {
  el.onclick = function() {
      modal.style.display = "block";
  }
})

closeBtn.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

//form validation

const form = document.getElementById('form');
const firstname = document.getElementById('firstname');
const lastname = document.getElementById('lastname');
const email = document.getElementById('email');

//show error nessage

function showError(input, message){
    const formValidation = input.parentElement;
    formValidation.classname = 'form-validation error'
    const errorMassege = formValidation.querySelector('p');
    errorMassege.innerText = message;
}
 
function showValid (input){
    const formValidation = input.parentElement;
    formValidation.classname = 'form-validation valid'
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    
    const firstnameValue = firstname.value.trim();
	const lastnameValue = lastname.value.trim();
	const emailValue = email.value.trim();

    if(firstnameValue == '') {
		showError(firstname, 'Username cannot be blank');
	
	}

    if(lastnameValue == '') {
		showError(lastname, 'Username cannot be blank');
	} 
	
	
	if(emailValue == '') {
		showError(email, 'Email cannot be blank');
    }

})

