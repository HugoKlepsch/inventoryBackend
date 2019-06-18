var searchField = document.getElementById("search field");

function search() {
  if (searchField.value.length > 0) {
    // search not yet implemented
  }
}

// send a logout post to flask api
function logout() {
  var form = document.createElement("form");
  form.setAttribute("method", "post");
  form.setAttribute("action", "logout");
  document.body.appendChild(form);
  form.submit();
}
