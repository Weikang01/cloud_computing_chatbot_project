import React from "react";
import { GoogleLogin } from "@react-oauth/google";

const google = () => {
  const fetchCalendarData = async (accessToken) => {
    const calendarApiUrl =
      "https://www.googleapis.com/calendar/v3/users/me/calendarList";
    try {
      const response = await fetch(calendarApiUrl, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Calendar Data:", data);
        // Handle calendar data
      } else {
        console.error("Failed to fetch calendar data:", response.statusText);
        // Handle error response
      }
    } catch (error) {
      console.error("Error fetching calendar data:", error);
      // Handle errors
    }
  };

  return (
    <GoogleLogin
      onSuccess={(credentialResponse) => {
        console.log(credentialResponse);
      }}
      onError={() => {
        console.log("Login Failed");
      }}
    />
  );
};

export default google;
