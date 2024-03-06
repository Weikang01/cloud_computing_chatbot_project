import React, { useState } from "react";

const OpenAIKeyWindow = ({ setApiKey, setIsKeyWindowVisible }) => {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = () => {
    if (inputValue.trim().length != 51) {
      alert("Invalid API Key. Please ensure it is 51 characters long."); // Show alert to the user
      return;
    }
    setApiKey(inputValue);
    setIsKeyWindowVisible(false);
  };

  return (
    <div className="openai-key-window">
      <div className="openai-key-content">
        <h2>Enter OpenAI API Key</h2>
        <input
          type="password"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="OpenAI API Key"
        />
        <div className="buttons">
          <button onClick={handleSubmit}>Submit</button>
        </div>
      </div>
    </div>
  );
};

export default OpenAIKeyWindow;
