# 🌐 Java HTTP Server

A simple HTTP server implemented in Java to serve static files over HTTP. This project is meant for learning purposes and demonstrates how basic HTTP functionality works under the hood using sockets and input/output streams.

## 📌 Features

- Serves static files (HTML, CSS, JS, images)
- Handles basic `GET` requests
- Sends appropriate HTTP response headers
- Returns 404 for missing files
- Lightweight and easy to understand

## 📁 Project Structure

```
http-server/
├── src/
│   └── HTTPServer.java     # Core HTTP server implementation
├── index.html              # Example HTML file to be served
└── README.md               # Project documentation
```

## 🔧 Requirements

- Java JDK 8 or higher

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/aayam-bajaj/http-server.git
cd http-server
```

### 2. Compile the server

```bash
javac src/HTTPServer.java
```

### 3. Run the server

```bash
java src.HTTPServer
```

The server starts and listens on `http://localhost:8080`.

### 4. Test the server

Place an `index.html` or other static files in the project root. Open your browser and visit:

```
http://localhost:8080
```

You should see your HTML page rendered.

## 🧠 Learning Objectives

- Understand how HTTP works at a low level
- Explore socket programming in Java
- Learn about request parsing and response formatting
- Implement MIME type handling

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Made by Aayam Bajaj (https://github.com/aayam-bajaj)
