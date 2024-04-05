import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

import axios from "axios";

const clientID = "YOUR_CLIENT_ID";
const clientSecret = "YOUR_CLIENT_SECRET";
const redirectURI = "YOUR_REDIRECT_URI";
const code = "AUTHORIZATION_CODE_FROM_REDIRECT"; // Replace with the actual code from the redirect

const accessToken = process.env.ACCESS_TOKEN; // Manually set this after obtaining it through OAuth flow

const testGoogleCalendarAPI = async () => {
  try {
    const response = await axios.get(
      "https://www.googleapis.com/calendar/v3/users/me/calendarList",
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    console.log("Calendar List:", response.data);
  } catch (error) {
    console.error(
      "Error accessing the Google Calendar API:",
      error.response.data
    );
  }
};

testGoogleCalendarAPI();
