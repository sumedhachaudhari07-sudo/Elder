const systemTitle = document.getElementById("systemTitle");
const systemMessage = document.getElementById("systemMessage");
const deviceStatus = document.getElementById("deviceStatus");
const lastEvent = document.getElementById("lastEvent");
const lastUpdated = document.getElementById("lastUpdated");
const alertCard = document.getElementById("alertCard");
const statusIcon = document.getElementById("statusIcon");
const feedback = document.getElementById("feedback");

async function loadStatus() {
    try {
        const response = await fetch("/api/status");
        const data = await response.json();

        if (data.fall_detected) {
            systemTitle.textContent = "Fall Alert Received";
            systemMessage.textContent =
                "A possible fall needs attention.";
            statusIcon.style.color = "#dc2626";
            alertCard.classList.remove("hidden");
        } else {
            systemTitle.textContent = data.device_connected
                ? "Device Connected"
                : "Waiting for Device";

            systemMessage.textContent = data.device_connected
                ? "Device event received."
                : "NodeMCU is not connected yet.";

            statusIcon.style.color = data.device_connected
                ? "#16a34a"
                : "#d97706";

            alertCard.classList.add("hidden");
        }

        deviceStatus.textContent = data.device_connected
            ? "Connected"
            : "Not Connected";

        lastEvent.textContent = data.last_event;
        lastUpdated.textContent = data.last_updated || "—";

    } catch (error) {
        feedback.textContent =
            "Cannot connect to Flask server.";
    }
}

async function sendRequest(url, body = {}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Request failed");
    }

    return data;
}

document.getElementById("testButton")
    .addEventListener("click", async function () {
        try {
            await sendRequest("/api/fall", {
                fall_detected: true
            });

            feedback.textContent = "Test alert received!";
            await loadStatus();

        } catch (error) {
            feedback.textContent = error.message;
        }
    });

document.getElementById("resetButton")
    .addEventListener("click", async function () {
        try {
            await sendRequest("/api/reset");
            feedback.textContent = "Alert reset successfully.";
            await loadStatus();

        } catch (error) {
            feedback.textContent = error.message;
        }
    });

loadStatus();
setInterval(loadStatus, 3000);