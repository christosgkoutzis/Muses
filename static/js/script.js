// Checks if form input fields are empty
function isFilled(input)
{
    if (input.value =="")
    {  alert(input.name + " is blank");
    // Focuses on the element that needs to be filled without refreshing
      input.focus();
      return false;
    }    
    else
        return true;
}   

// Accepts a form as an input and checks through the other function its inputs one by one
function checkInput(checkform)
{   
  // Contact form
  if (checkform.id == "contact-form"){
    check = ((isFilled(checkform.Email)) && (isFilled(checkform.Name)) && (isFilled(checkform.Subject)));
    // Checks if user has accepted terms and conditions (checkbox)
    if (!(checkbox = document.getElementById("checkbox").checked) && (check)){
      alert("Please accept the terms and conditions.")
      checkform.focus();
      check = false;
    }
  }
  // Newsletter form
  else if (checkform.id == "newsletter-form"){
    check = (isFilled(checkform.Email));
  }
  // Admin form
  else{
    check = ((isFilled(checkform.Username)) && (isFilled(checkform.Password)))
  }
  if(check){
    alert("Form submitted successfully.")
  }
  return check;
}

// Sends email after succesfully submitting the Newsletter Form

function sendEmail(form){
  // Checks for correct submit of the form
  if(checkInput(form)){
    Email.send({
      Host : "smtp.elasticemail.com",
      // Credentials from elasticemail SMTP API
      Username : "",
      Password : "",
      // Email address that your elasticemail account was created (not the username)
      From : "",
      To : document.getElementById("newsletter-email").value,
      Subject : "Muses Newsletter Subscription",
      Body : "Congratulations!!! You have subscribed to Muses newsletter."
    }).then(
    message => alert(message)
    );
  }
}