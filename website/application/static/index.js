// Function to add new messages to the chat window
async function add_messages(msg, scroll) {
  // Check if the message contains a name
  if (typeof msg.name !== 'undefined') {
    var date = dateNow();

    // Check if the message contains a time; if not, use the current time
    if (typeof msg.time !== "undefined") {
      var n = msg.time;
    } else {
      var n = date;
    }

    // Load the user's global name
    var global_name = await load_name();

    // Set the content of the message based on whether it's the user's message or others' message
    var content = '<div class="container">' + '<b style="color:#000" class="right">' + msg.name + '</b><p>' + msg.message + '</p><span class="time-right">' + n + '</span></div>';
    if (global_name == msg.name) {
      content = '<div class="container darker">' + '<b style="color:#000" class="left">' + msg.name + '</b><p>' + msg.message + '</p><span class="time-left">' + n + '</span></div>';
    }

    // Update the chat window
    var messageDiv = document.getElementById("messages");
    messageDiv.innerHTML += content;
  }

  // If scroll is true, scroll to the bottom of the chat window
  if (scroll) {
    scrollSmoothToBottom("messages");
  }
}

// Function to load the user's name from the server
async function load_name() {
  return await fetch('/get_name')
    .then(async function (response) {
      return await response.json();
    }).then(function (text) {
      return text["name"];
    });
}

// Function to load messages from the server
async function load_messages() {
  return await fetch('/get_messages')
    .then(async function (response) {
      return await response.json();
    }).then(function (text) {
      console.log(text);
      return text;
    });
}

// Set the height of the chat window based on window height
$(function () {
  $('.msgs').css({ 'height': (($(window).height()) * 0.7) + 'px' });

  $(window).bind('resize', function () {
    $('.msgs').css({ 'height': (($(window).height()) * 0.7) + 'px' });
  });
});

// Function to scroll smoothly to the bottom of the chat window
function scrollSmoothToBottom(id) {
  var div = document.getElementById(id);
  $('#' + id).animate({
    scrollTop: div.scrollHeight - div.clientHeight
  }, 500);
}

// Function to get the current date and time in a specific format
function dateNow() {
  var date = new Date();
  var aaaa = date.getFullYear();
  var gg = date.getDate();
  var mm = (date.getMonth() + 1);

  if (gg < 10)
    gg = "0" + gg;

  if (mm < 10)
    mm = "0" + mm;

  var cur_day = aaaa + "-" + mm + "-" + gg;

  var hours = date.getHours()
  var minutes = date.getMinutes()
  var seconds = date.getSeconds();

  if (hours < 10)
    hours = "0" + hours;

  if (minutes < 10)
    minutes = "0" + minutes;

  if (seconds < 10)
    seconds = "0" + seconds;

  return cur_day + " " + hours + ":" + minutes;
}

// Connect to the socket.io server and handle events
var socket = io.connect('http://' + location.hostname + ':' + location.port);
socket.on('connect', async function () {
  var usr_name = await load_name();
  if (usr_name != "") {
    socket.emit('event', {
      message: usr_name + ' just connected to the server!',
      connect: true
    });
  }

  var form = $('form#msgForm').on('submit', async function (e) {
    e.preventDefault();

    // Get input from the message box
    let msg_input = document.getElementById("msg");
    let user_input = msg_input.value;
    let user_name = await load_name();

    // Clear message box value
    msg_input.value = "";

    // Send message to other users
    socket.emit('event', {
      message: user_input,
      name: user_name
    });
  });
});

// Handle incoming message response from the server
socket.on('message response', function (msg) {
  add_messages(msg, true);
});

// Load messages and user name when the window loads
window.onload = async function () {
  var msgs = await load_messages();
  for (i = 0; i < msgs.length; i++) {
    scroll = false;
    if (i == msgs.length - 1) { scroll = true; }
    add_messages(msgs[i], scroll);
  }

  let name = await load_name();
  if (name != "") {
    $("#login").hide();
  } else {
    $("#logout").hide();
  }
};
