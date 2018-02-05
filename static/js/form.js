// Initialize Firebase (ADD YOUR OWN DATA)
var config = {
  apiKey: "xxxxx",
  authDomain: "xxxxx",
  databaseURL: "xxxxx",
  projectId: "xxxxx",
  storageBucket: "xxxxx",
  messagingSenderId: "xxxxx"
};
firebase.initializeApp(config);

// Reference messages collection
var messagesRef = firebase.database().ref('messages');

// Listen for form submit
document.getElementById('contactForm').addEventListener('submit', submitForm);

// Submit form
function submitForm(e){
  e.preventDefault();

  // Get values

  var food = food;
  if (food.checked()){
      getInputVal('food');
  }

  var water=water;
  if (water.checked()){
      getInputVal('water');
  }

  var assistance=assistance;
  if (assistance.checked()){
      getInputVal('assistance');
  }

  var outdoor=outdoor;
  if (outdoor.checked()){
      getInputVal('outdoor');
  }

  var other=other;
  if (other.checked()){
      getInputVal(document.getElementById("other").value);

  alert(outdoor);
  }





}