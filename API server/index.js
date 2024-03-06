import express from "express";

//const express = require('express');

import bodyParser from "body-parser";

import usersRoutes from "./routes/users.js";

const app = express();
const PORT = 80;

import cors from "cors";

import axios from "axios";

app.use(cors());

app.use(bodyParser.json());

app.use("/", usersRoutes);

// app.get('/', (req,res) =>
//     res.send('Hello From HomePage'));

function joinUrl(...parts) {
  return parts
    .map((part, index) => {
      if (part === undefined || part === null) {
        // Skip undefined or null parts
        return "";
      }
      if (index === 0) {
        return part.replace(/\/+$/, "");
      } else {
        return part.replace(/^\/+/, "").replace(/\/+$/, "");
      }
    })
    .join("/");
}

app.post("/chat", (req, res) => {
  const { user_id, message } = req.body;
  // console.log(
  //   `Received message from ${user_id}: ${message}\nreq.body.api_key:\n${req.body.api_key}`
  // );

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
    calendar_response: req.body.calendar_response,
    timestamp: 1000,
    api_key: req.body.api_key,
  };

  axios
    .post(joinUrl(process.env.INFERENCE_SERVER_URL, "chat"), my_req)
    .then((response) => {
      if (response.data.response) {
        res.status(200).json({
          status: "success",
          data: response.data.response,
        });
      } else {
        res.status(200).json({
          status: "success",
          data: response.data,
        });
      }
    })
    .catch((error) => {
      console.error("Error sending data:", error);
      res.status(200).json({
        status: "failed",
        data: "internal service connection error",
      });
    });
});

app.listen(PORT, "0.0.0.0", () =>
  console.log(`Server is running on port: http://localhost:${PORT}`)
);
