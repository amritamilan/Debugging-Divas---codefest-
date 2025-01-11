import './signup.css';
import { 
  hideLoginError, 
  showLoginState, 
  showLoginForm, 
  showApp, 
  showLoginError, 
  btnLogin,
  btnSignup,
  btnLogout
} from './ui.js';

import { initializeApp } from 'firebase/app';
import { 
  getAuth,
  onAuthStateChanged, 
  signOut,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  connectAuthEmulator
} from 'firebase/auth';

// Firebase initialization
const firebaseApp = initializeApp({
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: "diva-app-codefest.firebaseapp.com",
  projectId: "diva-app-codefest",
  storageBucket: "diva-app-codefest.appspot.com",
  messagingSenderId: "276915574731",
  appId: "1:276915574731:web:11101492740b3fe322084e",
  measurementId: "G-XWX49KJYCB"
});

const auth = getAuth(firebaseApp);

// Connect to emulator in development
if (window.location.hostname === 'localhost') {
  connectAuthEmulator(auth, "http://localhost:9099");
}

// Login
const loginEmailPassword = async () => {
  const loginEmail = txtEmail.value;
  const loginPassword = txtPassword.value;

  try {
    const userCredential = await signInWithEmailAndPassword(auth, loginEmail, loginPassword);
    console.log(userCredential.user);
  } catch (error) {
    console.log(`There was an error: ${error}`);
    showLoginError(error);
  }
};

// Signup
const createAccount = async () => {
  const loginEmail = txtEmail.value;
  const loginPassword = txtPassword.value;

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, loginEmail, loginPassword);
    console.log(`Account created for ${loginEmail}`);
    console.log(userCredential.user);
  } catch (error) {
    console.log(`There was an error: ${error}`);
    showLoginError(error);
  }
};

// Monitor auth state
const monitorAuthState = () => {
  onAuthStateChanged(auth, user => {
    if (user) {
      console.log(user);
      showApp();
      showLoginState(user);
      hideLoginError();
    } else {
      showLoginForm();
      lblAuthState.innerHTML = `You're not logged in.`;
    }
  });
};

// Logout
const logout = async () => {
  await signOut(auth);
};

// Add event listeners
btnLogin.addEventListener("click", loginEmailPassword);
btnSignup.addEventListener("click", createAccount);
btnLogout.addEventListener("click", logout);

// Start monitoring auth state
monitorAuthState();
