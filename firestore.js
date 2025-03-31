import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { auth, db } from "./firebase-config.js";
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "firebase/auth";
import { doc, setDoc } from "firebase/firestore";




async function savePreferences(genres) {
    const user = auth.currentUser;
    if (!user) return alert("Please log in first.");
    
    await db.collection("users").doc(user.uid).update({
        preferences: genres
    });
    alert("Preferences saved!");
}

async function getUserPreferences() {
    const user = auth.currentUser;
    if (!user) return [];

    const doc = await db.collection("users").doc(user.uid).get();
    return doc.exists ? doc.data().preferences : [];
}

async function addToWatchlist(movieName) {
    const user = auth.currentUser;
    if (!user) return alert("Please log in first.");

    await db.collection("users").doc(user.uid).update({
        watchlist: firebase.firestore.FieldValue.arrayUnion(movieName)
    });
    alert(movieName + " added to watchlist!");
}

async function getWatchlist() {
    const user = auth.currentUser;
    if (!user) return [];

    const doc = await db.collection("users").doc(user.uid).get();
    return doc.exists ? doc.data().watchlist : [];
}

