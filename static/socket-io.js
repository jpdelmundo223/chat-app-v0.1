// Get document URL
var url = document.URL;
console.log(url);

let username;
let room;

var message_section = document.querySelector("#messages-section");
var room_section = document.querySelector("#room-section");
var ul = document.querySelector("#messages");

ul.style.display = "none";

// Check if a a user is already in a room
if (room == null) {
  message_section.style.display = "none";
}

// Initialize socket
var socket = io(url);

// Start connection
socket.on("connect", function () {
  // Send data to server
  console.log("Socket is running!");
});

// Receive message
socket.on("message", function (data) {
  var li = document.createElement("li");
  var ul = document.querySelector("#messages");

  // Set received value to li element
  li.innerHTML = data;

  ul.append(li);
});

// Function to enter a room
function joinRoom(username, room) {
  socket.emit("join", { username: username, room: room });
}

// Function to leave a room
function leaveRoom(username, room) {
  socket.emit("leave", { username: username, room: room });
}

document
  .querySelector("form#roomForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    // Get the value of the username
    username = document.querySelector("#username").value;

    // Get the value of the room
    room = document.querySelector("#room").value;

    // Leave room
    // leaveRoom(username, room);

    // Join room
    joinRoom(username, room);

    // Set the room name
    var room_entered = document.querySelector("#room-name");
    room_entered.innerHTML = room;
    ul.style.display = "block";

    // If you are already in a room, displays the leave room button
    var leaveButton = document.querySelector("#leave-room");
    if (room_entered.innerHTML === "") {
      leaveButton.style.display = "none";
    } else {
      room_section.style.display = "none";
      leaveButton.style.display = "block";
      message_section.style.display = "block";
    }
  });

document.querySelector("#leave-room").addEventListener("click", function () {
  leaveRoom(username, room);
  room_section.style.display = "block";
  message_section.style.display = "none";
  var ul = document.querySelector("#messages");
  ul.style.display = "none";
});

document
  .querySelector("form#messageForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    socket.send({
      msg: document.querySelector("#message").value,
      username: username,
      room: room,
    });
  });
