import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyC1pX5Mz6_OJKhzI2P0ugTuEfvSoLIXovE",
  authDomain: "ai-resume-analyzer-5bb5f.firebaseapp.com",
  projectId: "ai-resume-analyzer-5bb5f",
  storageBucket: "ai-resume-analyzer-5bb5f.firebasestorage.app",
  messagingSenderId: "703642958570",
  appId: "1:703642958570:web:533e0cc80bc890d967f593"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);