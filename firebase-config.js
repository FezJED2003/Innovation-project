// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCDuRfDqLScG1ss5NUJ71DL9ZoNW6Llptk",
  authDomain: "moviechatbot-c736f.firebaseapp.com",
  projectId: "moviechatbot-c736f",
  storageBucket: "moviechatbot-c736f.firebasestorage.app",
  messagingSenderId: "622390261285",
  appId: "1:622390261285:web:374b2b5f50b231e837b1cc",
  measurementId: "G-W36KBMTK2Q"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = firebase.auth();
const db = firebase.firestore();


export { db, auth };

