function textboxAlert() {
  username = document.getElementById("username").value
  password = document.getElementById("password").value
  if (username == ""){
    alert ("Please enter username");
    return false;
  }
  if (password == ""){
    alert ("Please enter password");
    return false;
  }
  return true;
}
