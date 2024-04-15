function sendform(formobject) {
    let form_name = "form-" + formobject.id;
    let form = document.getElementsByName(form_name);
    form[0].submit();
}

function redirectto(url) {
    window.location.replace(url);
}