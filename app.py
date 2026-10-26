from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

fall_history = []
emergency_contacts = []
system_status = "Monitoring Active"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ElderCare | Smart Elderly Care</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    background: #f3f6fb;
    color: #263248;
}

header {
    background: linear-gradient(135deg, #176b87, #38a3a5);
    color: white;
    padding: 25px 7%;
}

header h1 {
    font-size: 30px;
    margin-bottom: 8px;
}

header p {
    opacity: 0.9;
}

.container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
}

.welcome {
    margin-bottom: 25px;
}

.welcome h2 {
    font-size: 25px;
    margin-bottom: 8px;
}

.welcome p {
    color: #718096;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

.icon {
    font-size: 32px;
    margin-bottom: 15px;
}

.card h3 {
    font-size: 16px;
    color: #718096;
    margin-bottom: 12px;
}

.value {
    font-size: 22px;
    font-weight: bold;
}

.green {
    color: #159570;
}

.orange {
    color: #e68a21;
}

.section {
    background: white;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.04);
}

.section h2 {
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 7px;
    font-weight: bold;
}

input, select {
    width: 100%;
    padding: 12px;
    border: 1px solid #dce3ec;
    border-radius: 8px;
    font-size: 15px;
}

button {
    background: #176b87;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
}

button:hover {
    background: #12556c;
}

.alert-button {
    background: #d94b4b;
}

.alert-button:hover {
    background: #b83232;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    text-align: left;
    padding: 13px 10px;
    border-bottom: 1px solid #edf0f5;
}

th {
    color: #718096;
}

.empty {
    color: #718096;
    padding: 10px 0;
}

.notice {
    background: #fff4dc;
    border-left: 5px solid #e6a23c;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 25px;
    line-height: 1.6;
}

footer {
    text-align: center;
    padding: 25px;
    color: #718096;
}

@media (max-width: 600px) {
    header h1 {
        font-size: 25px;
    }

    .section {
        padding: 18px;
        overflow-x: auto;
    }

    .value {
        font-size: 19px;
    }
}
</style>
</head>

<body>

<header>
    <h1>💙 ElderCare</h1>
    <p>Smart Fall Detection & Elderly Care System</p>
</header>

<div class="container">

    <div class="welcome">
        <h2>Welcome to ElderCare 👋</h2>
        <p>Your elderly care monitoring dashboard</p>
    </div>

    <div class="notice">
        <strong>Demo Mode:</strong>
        This dashboard does not detect real falls yet.
        Sensor integration is required for actual fall detection.
        Test alerts on this page are simulated.
    </div>

    <div class="cards">

        <div class="card">
            <div class="icon">🟢</div>
            <h3>System Status</h3>
            <div class="value green">{{ status }}</div>
        </div>

        <div class="card">
            <div class="icon">🚨</div>
            <h3>Recorded Alerts</h3>
            <div class="value">{{ history|length }}</div>
        </div>

        <div class="card">
            <div class="icon">👵</div>
            <h3>Care Profile</h3>
            <div class="value">Elderly Care</div>
        </div>

        <div class="card">
            <div class="icon">📞</div>
            <h3>Emergency Contacts</h3>
            <div class="value">{{ contacts|length }}</div>
        </div>

    </div>

    <div class="section">
        <h2>👤 Elderly Person Profile</h2>

        <form method="POST" action="/profile">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="name"
                       placeholder="Enter elderly person's name"
                       required>
            </div>

            <div class="form-group">
                <label>Age</label>
                <input type="number" name="age"
                       min="1" max="120"
                       placeholder="Enter age" required>
            </div>

            <button type="submit">Save Profile</button>
        </form>

        {% if profile %}
        <p style="margin-top:20px;">
            <strong>Name:</strong> {{ profile.name }}<br><br>
            <strong>Age:</strong> {{ profile.age }}
        </p>
        {% endif %}
    </div>

    <div class="section">
        <h2>🚨 Fall Detection Demo</h2>
        <p style="margin-bottom:20px;color:#718096;">
            Use this button to simulate a fall event for testing.
            It does not detect actual movement.
        </p>

        <form method="POST" action="/simulate-fall">
            <button class="alert-button" type="submit">
                Simulate Fall Alert
            </button>
        </form>
    </div>

    <div class="section">
        <h2>📞 Emergency Contacts</h2>

        <form method="POST" action="/contact">
            <div class="form-group">
                <label>Contact Name</label>
                <input type="text" name="contact_name"
                       placeholder="Enter caregiver name" required>
            </div>

            <div class="form-group">
                <label>Phone Number</label>
                <input type="tel" name="phone"
                       placeholder="Enter phone number" required>
            </div>

            <button type="submit">Add Contact</button>
        </form>

        {% if contacts %}
        <table style="margin-top:20px;">
            <tr>
                <th>Name</th>
                <th>Phone</th>
            </tr>
            {% for contact in contacts %}
            <tr>
                <td>{{ contact.name }}</td>
                <td>{{ contact.phone }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p class="empty" style="margin-top:20px;">
            No emergency contacts added yet.
        </p>
        {% endif %}
    </div>

    <div class="section">
        <h2>📊 Activity History</h2>

        {% if history %}
        <table>
            <tr>
                <th>Event</th>
                <th>Date & Time</th>
                <th>Status</th>
            </tr>

            {% for event in history %}
            <tr>
                <td>{{ event.event }}</td>
                <td>{{ event.time }}</td>
                <td>{{ event.status }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p class="empty">No activity recorded yet.</p>
        {% endif %}
    </div>

</div>

<footer>
    ElderCare © 2026 | Smart Elderly Care Project
</footer>

</body>
</html>
"""

profile = None


@app.route("/")
def home():
    return render_template_string(
        HTML,
        status=system_status,
        history=fall_history,
        contacts=emergency_contacts,
        profile=profile
    )


@app.route("/profile", methods=["POST"])
def save_profile():
    global profile

    profile = {
        "name": request.form["name"].strip(),
        "age": request.form["age"]
    }

    return redirect(url_for("home"))


@app.route("/contact", methods=["POST"])
def add_contact():
    name = request.form["contact_name"].strip()
    phone = request.form["phone"].strip()

    if name and phone:
        emergency_contacts.append({
            "name": name,
            "phone": phone
        })

    return redirect(url_for("home"))


@app.route("/simulate-fall", methods=["POST"])
def simulate_fall():
    fall_history.insert(0, {
        "event": "Simulated Fall Alert",
        "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
        "status": "Demo Event"
    })

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)