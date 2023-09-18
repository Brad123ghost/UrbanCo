// // Add active class to the current list tem (highlight it)
// var checkoutList = document.getElementById("checkoutList");
// var checkoutItems = checkoutList.getElementsByClassName("step-checkout_item");
// for (var i = 0; i < checkoutItems.length; i++) {
//     checkoutItems[i].addEventListener("click", function() {
//     var current = document.getElementsByClassName("active");
//     current[0].className = current[0].className.replace(" active", "");
//     this.className += " active";
//   });
// }

var currentStep = 1

function checkStep() {
  if (currentStep == 1) {
    document.getElementById("back-btn").innerHTML = "Return to Cart"
  } else {
    document.getElementById("back-btn").innerHTML = "Back"
  }  

  if(currentStep == 4) {
    document.getElementById("next-btn").innerHTML = "Confirm Purchase"
  } else {
    document.getElementById("next-btn").innerHTML = "Continue"
  }
}

function next() {
  if (currentStep < 4) {
    document.getElementById("stepCheckoutItem" + currentStep.toString()).classList.remove("active")
    currentStep++
    document.getElementById("stepCheckoutItem" + currentStep.toString()).classList.add("active")
    checkStep()
  }
  else {
    window.location.href = "/payment/success"
  }
  console.log(currentStep)
}

function prev() {
  if (currentStep > 1) {
    document.getElementById("stepCheckoutItem" + currentStep.toString()).classList.remove("active")
    currentStep--
    document.getElementById("stepCheckoutItem" + currentStep.toString()).classList.add("active")
    checkStep()
  } else {
    window.location.href = "/"
  }
  console.log(currentStep)
}
