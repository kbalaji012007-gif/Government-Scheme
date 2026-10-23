import { initializeApp, getApps, getApp } from 'firebase/app';
import { getFirestore, collection, getDocs, doc, getDoc, query, where } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyB_AWqA9-Z7X-uxEM1diduZxCdDE6zxHQE",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "ruralconnect-karnataka.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "ruralconnect-karnataka",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "ruralconnect-karnataka.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "217967185082",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:217967185082:web:00f63a34e9eef53529c683",
};

export const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
export const db = getFirestore(app);
export const auth = getAuth(app);
export { collection, getDocs, doc, getDoc, query, where };
