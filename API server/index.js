import express from "express";

//const express = require('express');

import bodyParser from "body-parser";

import usersRoutes from "./routes/users.js";

const app = express();
const PORT = 8000;

import cors from "cors";

import axios from "axios";

app.use(cors());

app.use(bodyParser.json());

app.use("/", usersRoutes);

// app.get('/', (req,res) =>
//     res.send('Hello From HomePage'));

app.post("/chat", (req, res) => {
  const { user_id, message } = req.body;
  console.log(`Received message from ${user_id}: ${message}`);

  const response = {
    user_id: user_id, // Echoing back the user_id received from the request
    respond: "Error sending data", // Your static response message
  };

  const my_req = {
    user_id: user_id,
    chat_history: [
      // {
      //   sender: "Bot",
      //   message: "Hello, there! How may I help you?",
      //   timestamp: time.time(),
      // },
    ],
    message: message,
    calendar_response: {},
    timestamp: 1000,
  };

  axios
    .post("http://127.0.0.1:10299/chat", my_req)
    .then((response) => {
      console.log(response.data);
      res.status(200).json({
        status: "success",
        data: response.data,
      });
    })
    .catch((error) => {
      console.error("Error sending data:", error);
      res.status(200).json({
        status: "failed",
        data: "internal service connection error",
      });
    });
});

app.listen(PORT, () =>
  console.log(`Server is running on port: http://localhost:${PORT}`)
);
