// Add active class to the current list tem (highlight it)
var checkoutList = document.getElementById("checkoutList");
var checkoutItems = checkoutList.getElementsByClassName("step-checkout_item");
for (var i = 0; i < checkoutItems.length; i++) {
    checkoutItems[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}

var currentStep = 1

function checkStep() {
  if (currentStep == 1) {
    document.getElementById("back-btn").innerHTML = "Return to Cart"
  } else {
    document.getElementById("back-btn").innerHTML = "Back"
  }  
}

function next() {
  if (currentStep < 4) {
    currentStep++
    document.getElementById("stepCheckoutItem" + currentStep.toString()).click()
    checkStep()
  }
  console.log(currentStep)
}

function prev() {
  if (currentStep > 1) {
    currentStep--
    document.getElementById("stepCheckoutItem" + currentStep.toString()).click()
    checkStep()
  } else {
    window.location.href = "/"
  }
  console.log(currentStep)
}
