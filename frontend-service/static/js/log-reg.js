var loginForm = document.getElementById("loginForm")
var regForm = document.getElementById("regForm")
var indicator = document.getElementById("indicator")

function login(){
    loginForm.style.transform = "translateX(0px)"
    regForm.style.transform = "translateX(0px)"
    indicator.style.transform = "translateX(0px)"
    loginForm.classList.add("transition")
    regForm.classList.add("transition")
    indicator.classList.add("transition")
}

function register(){
    loginForm.style.transform = "translateX(-450px)"
    regForm.style.transform = "translateX(-450px)"
    indicator.style.transform = "translateX(100px)"
    loginForm.classList.add("transition")
    regForm.classList.add("transition")
    indicator.classList.add("transition")
}

function registererror(){
    loginForm.style.transform = "translateX(-450px)"
    regForm.style.transform = "translateX(-450px)"
    indicator.style.transform = "translateX(100px)"
    loginForm.classList.remove("transition")
    regForm.classList.remove("transition")
    indicator.classList.remove("transition")
}

function check() {
    if(document.getElementById("confirmpwd").value != document.getElementById("pwd").value) {
        document.getElementById("confirmpwd").setCustomValidity("Password does not match")
    } else {
        document.getElementById("confirmpwd").setCustomValidity("")
    }
}

function showToast() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl)
    })
    toastList.forEach(toast => toast.show())
}
