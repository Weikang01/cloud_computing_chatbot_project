import React, { useState, useEffect } from "react";
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
import backgroundImage from "./image/1366_front.jpg";

// "Explain things like you would to a 10 year old learning how to code."
const systemMessage = {
  //  Explain things like you're talking to a software professional with 5 years of experience.
  role: "system",
  content:
    "Explain things like you're talking to a software professional with 2 years of experience.",
};

var gapi = undefined;
const script = document.createElement("script");
script.src = "https://apis.google.com/js/api.js";

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

const ChatWindow = (args) => {
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
      let is_calendar = false;

      try {
        const requestBody = {
          user_id: "jamesbond",
          message: messages[messages.length - 1].message,
          api_key: args.APIKey,
        };

        const response = await fetch(joinUrl(window.API_SERVER_URL, "chat"), {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();

          if (data.data && data.data.error) {
            alert(data.data.error);
            return;
          }

          if (
            data.data &&
            (data.data["maxResults"] ||
              data.data["timeMin"] ||
              data.data["orderBy"])
          ) {
            is_calendar = true;
            get_calendar_info(
              data.data["maxResults"],
              data.data["timeMin"],
              data.data["orderBy"]
            );
          } else {
            const newMessage = {
              message: data.data,
              sentTime: "just now",
              sender: "ChatGPT",
            };

            const newMessages = [...messages, newMessage];

            setMessages(newMessages);
          }
        } else {
          console.error("Failed to send message:", response.statusText);
          // Handle error response
        }
      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
        if (!is_calendar) {
          setIsTyping(false);
        }
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

  const get_calendar_info = (maxResults, timeMin, orderBy) => {
    if (gapi && gapi.client && gapi.client.calendar) {
      var request = gapi.client.calendar.events.list({
        calendarId: "primary" /* Can be 'primary' or a given calendarid */,
        timeMin: timeMin ? timeMin : new Date().toISOString(),
        showDeleted: false,
        singleEvents: true,
        maxResults: maxResults ? parseInt(maxResults) : 10,
        orderBy: orderBy ? orderBy : "startTime",
      });

      request.execute(async function(resp) {
        var events = resp.items;
        if (events.length > 0) {
          let c_responses = [];
          for (let i = 0; i < events.length; i++) {
            c_responses.push({
              summary: events[i].summary,
              description: events[i].description,
              location: events[i].location,
              start: {
                dateTime: events[i].start.dateTime,
                timeZone: events[i].start.timeZone,
              },
              end: {
                dateTime: events[i].end.dateTime,
                timeZone: events[i].end.timeZone,
              },
            });
          }

          const requestBody = {
            user_id: "jamesbond",
            message: messages[messages.length - 1].message,
            calendar_response: c_responses,
            api_key: args.APIKey,
          };

          const response = await fetch(joinUrl(window.API_SERVER_URL, "chat"), {
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

          setIsTyping(false);
        }
      });
    } else {
      const newMessage = {
        message:
          "This question is Calendar-related, please login to your Google account.",
        sentTime: "just now",
        sender: "System",
      };

      const newMessages = [...messages, newMessage];

      setMessages(newMessages);

      setIsTyping(false);
    }
  };

  const loginGoogleAPI = () => {
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
        backgroundImage: `url(${backgroundImage})`,
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
          <button style={{ width: 100, height: 50 }} onClick={loginGoogleAPI}>
            get events
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
