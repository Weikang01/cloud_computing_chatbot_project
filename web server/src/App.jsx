import React, { useState } from "react";

import "./openai_key_window";
import "./chat_window";

import "./App.css";
import OpenAIKeyWindow from "./openai_key_window";
import ChatWindow from "./chat_window";

function App() {
  const [apiKey, setApiKey] = useState("");
  const [isKeyWindowVisible, setIsKeyWindowVisible] = useState(true); // State to track visibility of OpenAIKeyWindow

  return (
    <div>
      {isKeyWindowVisible && (
        <OpenAIKeyWindow
          setApiKey={setApiKey}
          setIsKeyWindowVisible={setIsKeyWindowVisible}
        />
      )}
      {!isKeyWindowVisible && <ChatWindow APIKey={apiKey} />}
    </div>
  );
}

export default App;
