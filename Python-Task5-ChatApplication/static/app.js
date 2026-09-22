const socket = io();

let currentRoomId = null;
let currentUsername = document.body.dataset.username || "";

const roomList = document.getElementById("roomList");
const messages = document.getElementById("messages");
const messageForm = document.getElementById("messageForm");
const messageInput = document.getElementById("messageInput");
const currentRoom = document.getElementById("currentRoom");
const connectionStatus = document.getElementById("connectionStatus");
const roomName = document.getElementById("roomName");
const createRoomBtn = document.getElementById("createRoomBtn");
const notificationBtn = document.getElementById("notificationBtn");
const toast = document.getElementById("toast");

function showToast(message) {
    toast.textContent = message;
    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}

function addMessage(username, message, timestamp) {
    const wrapper = document.createElement("div");
    wrapper.className = "message";

    if (username === currentUsername) {
        wrapper.classList.add("own");
    }

    const userElement = document.createElement("div");
    userElement.className = "message-user";
    userElement.textContent = username;

    const messageElement = document.createElement("div");
    messageElement.className = "message-text";
    messageElement.textContent = message;

    const timeElement = document.createElement("div");
    timeElement.className = "message-time";
    timeElement.textContent = timestamp;

    wrapper.appendChild(userElement);
    wrapper.appendChild(messageElement);
    wrapper.appendChild(timeElement);

    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;
}

function addSystemMessage(message, timestamp) {
    const element = document.createElement("div");
    element.className = "system-message";
    element.textContent = `${message} • ${timestamp}`;

    messages.appendChild(element);
    messages.scrollTop = messages.scrollHeight;
}

function showNotification(username, message) {
    showToast(`${username}: ${message}`);

    if (document.hidden && "Notification" in window) {
        if (Notification.permission === "granted") {
            new Notification("OASIS Chat", {
                body: `${username}: ${message}`
            });
        }
    }
}

async function loadRooms() {
    const response = await fetch("/api/rooms");

    if (!response.ok) {
        return;
    }

    const rooms = await response.json();

    roomList.innerHTML = "";

    rooms.forEach(room => {
        const button = document.createElement("button");
        button.className = "room-item";
        button.textContent = `# ${room.name}`;
        button.dataset.roomId = room.id;

        button.addEventListener("click", () => {
            joinRoom(room.id, room.name);
        });

        roomList.appendChild(button);
    });

    if (rooms.length > 0 && currentRoomId === null) {
        joinRoom(rooms[0].id, rooms[0].name);
    }
}

function updateActiveRoom() {
    document.querySelectorAll(".room-item").forEach(button => {
        button.classList.remove("active");

        if (Number(button.dataset.roomId) === Number(currentRoomId)) {
            button.classList.add("active");
        }
    });
}

function joinRoom(roomId, roomNameText) {
    currentRoomId = roomId;
    currentRoom.textContent = `# ${roomNameText}`;
    messages.innerHTML = "";

    updateActiveRoom();

    socket.emit("join_room_event", {
        room_id: roomId
    });
}

socket.on("connect", () => {
    connectionStatus.textContent = "Connected";
});

socket.on("disconnect", () => {
    connectionStatus.textContent = "Disconnected";
});

socket.on("room_history", data => {
    currentRoomId = data.room_id;
    currentRoom.textContent = `# ${data.room_name}`;

    messages.innerHTML = "";

    data.messages.forEach(item => {
        addMessage(
            item.username,
            item.message,
            item.timestamp
        );
    });

    updateActiveRoom();
});

socket.on("new_message", data => {
    addMessage(
        data.username,
        data.message,
        data.timestamp
    );

    if (data.username !== currentUsername) {
        showNotification(
            data.username,
            data.message
        );
    }
});

socket.on("system_message", data => {
    addSystemMessage(
        data.message,
        data.timestamp
    );
});

messageForm.addEventListener("submit", event => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message || currentRoomId === null) {
        return;
    }

    socket.emit("send_message", {
        room_id: currentRoomId,
        message: message
    });

    messageInput.value = "";
    messageInput.focus();
});

createRoomBtn.addEventListener("click", async () => {
    const name = roomName.value.trim();

    if (!name) {
        showToast("Enter a room name.");
        return;
    }

    const response = await fetch("/api/rooms", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name
        })
    });

    const data = await response.json();

    if (!response.ok) {
        showToast(data.error);
        return;
    }

    roomName.value = "";

    await loadRooms();

    joinRoom(data.id, data.name);
});

roomName.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        createRoomBtn.click();
    }
});

notificationBtn.addEventListener("click", async () => {
    if (!("Notification" in window)) {
        showToast("Browser notifications are not supported.");
        return;
    }

    const permission = await Notification.requestPermission();

    if (permission === "granted") {
        notificationBtn.textContent = "Notifications Enabled";
        showToast("Notifications enabled.");
    } else {
        showToast("Notification permission was not granted.");
    }
});

loadRooms();