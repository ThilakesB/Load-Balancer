<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Python Load Balancer</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #0f172a;
      color: #e2e8f0;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: auto;
      padding: 20px;
    }
    .center {
      text-align: center;
    }
    img {
      width: 150px;
    }
    h1, h2, h3 {
      color: #38bdf8;
    }
    .badge img {
      margin: 5px;
    }
    .box {
      background: #1e293b;
      padding: 15px;
      border-radius: 10px;
      margin: 10px 0;
    }
    ul {
      padding-left: 20px;
    }
    code {
      background: #020617;
      padding: 5px 10px;
      border-radius: 5px;
      display: inline-block;
    }
  </style>
</head>

<body>

<div class="container">

  <!-- Header -->
  <div class="center">
    <img src="logo.png" alt="Load Balancer Logo">
    <h1>Python Load Balancer</h1>
    <h3>High-performance load balancer built using Python</h3>

    <div class="badge">
      <img src="https://img.shields.io/badge/license-MIT-blue">
      <img src="https://img.shields.io/badge/status-active-success">
      <img src="https://img.shields.io/badge/python-3.x-blue">
    </div>
  </div>

  <!-- Intro -->
  <div class="box">
    <p>
      This project is a custom-built Load Balancer that distributes incoming requests
      across multiple servers to improve performance and reliability.
    </p>
  </div>

  <!-- Install -->
  <h2>🚀 Installation</h2>
  <div class="box">
    <code>pip install -r requirements.txt</code>
  </div>

  <!-- Features -->
  <h2>🚀 Features</h2>
  <div class="box">
    <ul>
      <li>Load Distribution</li>
      <li>Round Robin Algorithm</li>
      <li>High Availability</li>
      <li>Scalability</li>
      <li>Fault Tolerance</li>
    </ul>
  </div>

  <!-- Working -->
  <h2>⚙️ How It Works</h2>
  <div class="box">
    <ul>
      <li>Client sends request</li>
      <li>Load balancer receives request</li>
      <li>Selects server using Round Robin</li>
      <li>Forwards request</li>
      <li>Returns response</li>
    </ul>
  </div>

  <!-- Algorithm -->
  <h2>🧠 Algorithm</h2>
  <div class="box">
    <p><b>Round Robin:</b></p>
    <ul>
      <li>Request 1 → Server A</li>
      <li>Request 2 → Server B</li>
      <li>Request 3 → Server C</li>
      <li>Request 4 → Server A</li>
    </ul>
  </div>

  <!-- Structure -->
  <h2>📁 Project Structure</h2>
  <div class="box">
    <ul>
      <li>load_balancer.py</li>
      <li>server.py</li>
      <li>client.py</li>
      <li>config.json</li>
    </ul>
  </div>

  <!-- Setup -->
  <h2>🛠️ Setup</h2>
  <div class="box">
    <ul>
      <li>Clone repository</li>
      <li>Install dependencies</li>
      <li>Run backend servers</li>
      <li>Start load balancer</li>
      <li>Send requests</li>
    </ul>
  </div>

  <!-- Use Cases -->
  <h2>📊 Use Cases</h2>
  <div class="box">
    <ul>
      <li>Web apps</li>
      <li>API distribution</li>
      <li>Microservices</li>
      <li>Traffic management</li>
    </ul>
  </div>

  <!-- Future -->
  <h2>🔮 Future Improvements</h2>
  <div class="box">
    <ul>
      <li>Least Connections Algorithm</li>
      <li>Health Checks</li>
      <li>HTTPS Support</li>
      <li>Dashboard UI</li>
    </ul>
  </div>

  <!-- Footer -->
  <h2>📜 License</h2>
  <div class="box">
    <p>MIT License</p>
  </div>

</div>

</body>
</html>
