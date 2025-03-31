import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { auth, db } from "./firebase-config.js";
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "firebase/auth";
import { doc, setDoc } from "firebase/firestore";

async function registerUser(){

const email = document.getElementById("register").value
const password = document.getElementById("registerPassword").value

try{

const userCredential = await auth.createUserWithEmailAndPassword(email, password);
const user = userCredential.user;
alert("Registration successful! You can now log in.");
saveUserData(user);
}catch(error){

alert(error.message); 

}

}


async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

     try{

        const userCredential = await auth.createUserWithEmailAndPassword(email,password);
        alert("Login successful");
        window.location.href = "chatbot.html";
     } catch(error){
        alert("Invalid email or password");

     }
    
}



async function saveUserData(user) {
    await db.collection("Users").doc(user.uid).set({
      email: user.email,
      preferences: [],
      watchlist: []

    });
}


function logoutUser(){
 signOut(auth)
 .then(() =>{
   alert("Logged out successfully!"); 
   window.location.href ="popup.html";
 })


 .catch(error =>{
alert ("Error loggin out: " + error.message);

 });
}