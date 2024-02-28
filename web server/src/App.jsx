import { useState, useEffect } from "react";
import "./App.css";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";
import image from "./image/wolf.png";
import { GoogleLogin } from "@react-oauth/google";
import { GoogleOAuthProvider } from "@react-oauth/google";

import Google from "./google";

const API_KEY = "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";
// "Explain things like you would to a 10 year old learning how to code."
const systemMessage = {
  //  Explain things like you're talking to a software professional with 5 years of experience.
  role: "system",
  content:
    "Explain things like you're talking to a software professional with 2 years of experience.",
};

function App() {
  const script = document.createElement("script");
  script.src = "https://apis.google.com/js/api.js";
  var gapi = undefined;

  const loadGapiAndInitClient = () => {
    // Load the gapi script
    const script = document.createElement("script");
    script.src = "https://apis.google.com/js/api.js";
    script.onload = () => {
      // Once the gapi script has loaded, it should create the 'gapi' object on the window
      if (window.gapi) {
        // Now we can safely call gapi.load
        gapi = window.gapi;
      } else {
        console.error(
          "GAPI script loaded, but `gapi` object is not available."
        );
      }
    };
    script.onerror = () => {
      console.error("Failed to load the GAPI script.");
    };
    document.body.appendChild(script);
  };

  const initClient = () => {
    window.gapi.client
      .init(config)
      .then(() => {
        // Your initialization code here
      })
      .catch((error) => {
        console.error("Error initializing the gapi client:", error);
      });
  };

  const [messages, setMessages] = useState([
    {
      message: "Hello, I'm ThunderWolfie! Ask me anything!",
      sentTime: "just now",
      sender: "ChatGPT",
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [userLoggedIn, setUserLoggedIn] = useState(false);

  useEffect(() => {
    loadGapiAndInitClient();
  }, []);

  useEffect(() => {
    if (
      messages.length == 0 ||
      messages[messages.length - 1].sender != "user"
    ) {
      return;
    }

    const sendMessage = async () => {
      try {
        const requestBody = {
          user_id: "jamesbond",
          message: messages[messages.length - 1].message,
        };

        const response = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();

          const newMessage = {
            message: data.data,
            sentTime: "just now",
            sender: "ChatGPT",
          };

          const newMessages = [...messages, newMessage];

          setMessages(newMessages);
        } else {
          console.error("Failed to send message:", response.statusText);
          // Handle error response
        }
      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
        setIsTyping(false);
      }
    };
    sendMessage();
  }, [messages]);

  async function sendMessageToAPIServer(message) {
    const selfMessage = {
      message: message,
      sentTime: "just now",
      sender: "user",
    };

    const newselfMessages = [...messages, selfMessage];

    setMessages(newselfMessages);

    setIsTyping(true);
  }

  function listUpcomingEvents(n) {
    n = 3;
    gapi.client.calendar.events
      .list({
        calendarId: "primary",
        timeMin: new Date().toISOString(),
        showDeleted: false,
        singleEvents: true,
        maxResults: n,
        orderBy: "startTime",
      })
      .then((response) => {
        const events = response.result.items;
        console.log(events);
      });
  }

  const getEvents = () => {
    if (gapi != undefined) {
      const config = {
        // clientId: "1052718117355-jn0ls2voijd5gt0qh5o1gf8c750f7cic.apps.googleusercontent.com",
        apiKey: "AIzaSyAWK5uCYS8-eDrguCS9Mslgd0wFVmFfL5o",
        // scope: "https://www.googleapis.com/auth/calendar",
        discoveryDocs: [
          "https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest",
        ],
      };

      gapi.load("client:auth2", () => {
        gapi.client.init(config);
        let tokenClient = google.accounts.oauth2.initTokenClient({
          client_id:
            "1052718117355-jn0ls2voijd5gt0qh5o1gf8c750f7cic.apps.googleusercontent.com",
          scope: "https://www.googleapis.com/auth/calendar.readonly",
          callback: "", // defined later
        });

        if (gapi.client.getToken() === null) {
          // Prompt the user to select a Google Account and ask for consent to share their data
          // when establishing a new session.
          tokenClient.requestAccessToken({ prompt: "consent" });
        } else {
          // Skip display of account chooser and consent dialog for an existing session.
          tokenClient.requestAccessToken({ prompt: "" });
        }
      });
    }
  };

  return (
    <div
      className="App"
      style={{
        backgroundImage: 'url("./Image/1366_front.jpg")',
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="wrapper">
        <div className="header">
          <div style={{ display: "flex", alignItems: "center" }}>
            <div className="img">
              <img
                src={image}
                alt=""
                style={{
                  width: "50px",
                  height: "50px",
                  borderRadius: "50%",
                  marginRight: "10px",
                }}
              />
            </div>
            <div className="right">
              <div className="name">ThunderWolfie</div>
              <div className="status">Active</div>
            </div>
          </div>
        </div>
        <MainContainer>
          <ChatContainer>
            <MessageList
              scrollBehavior="smooth"
              typingIndicator={
                isTyping ? (
                  <TypingIndicator content="ChatGPT is typing" />
                ) : null
              }
            >
              {messages.map((message, i) => {
                // console.log(message);
                return <Message key={i} model={message} />;
              })}
            </MessageList>
            <MessageInput
              placeholder="Type message here"
              onSend={sendMessageToAPIServer}
            />
          </ChatContainer>
        </MainContainer>
        <div style={{ textAlign: "right", padding: "10px" }}>
          <p>Login with google so I can assit you better</p>
        </div>

        {/* Sign-in button */}
        <div style={{ buttonAlign: "right", padding: "10px" }}>
          {/* <GoogleOAuthProvider clientId="749023156778-hsjfscfcfomhu8923fucu5a40rosf71l.apps.googleusercontent.com">
            <Google />
          </GoogleOAuthProvider> */}
          <button style={{ width: 100, height: 50 }} onClick={getEvents}>
            get events
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
