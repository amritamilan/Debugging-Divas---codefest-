// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAQXwlxdeoNCdKqM7qovSoT4BSNqZ4KCoo",
  authDomain: "diva-app-codefest.firebaseapp.com",
  projectId: "diva-app-codefest",
  storageBucket: "diva-app-codefest.firebasestorage.app",
  messagingSenderId: "276915574731",
  appId: "1:276915574731:web:11101492740b3fe322084e",
  measurementId: "G-XWX49KJYCB"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);