import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { GoogleOAuthProvider } from "@react-oauth/google";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId="749023156778-hsjfscfcfomhu8923fucu5a40rosf71l.apps.googleusercontent.com"></GoogleOAuthProvider>
    ;
    <App />
  </React.StrictMode>
);
