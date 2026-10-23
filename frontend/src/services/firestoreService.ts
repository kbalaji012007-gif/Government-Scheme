import { collection, getDocs, doc, getDoc } from 'firebase/firestore';
import { db } from './firebase';
import { SchemeDetail, CenterDetail } from '../types';

export const firestoreService = {
  /**
   * Directly fetches all schemes from Firebase Cloud Firestore
   */
  async getSchemes(): Promise<SchemeDetail[]> {
    const querySnapshot = await getDocs(collection(db, 'schemes'));
    const schemes: SchemeDetail[] = [];
    querySnapshot.forEach((docSnap) => {
      schemes.push({ id: docSnap.id, ...docSnap.data() } as SchemeDetail);
    });
    return schemes;
  },

  /**
   * Directly fetches a single scheme by its ID from Firebase Cloud Firestore
   */
  async getSchemeById(id: string): Promise<SchemeDetail | null> {
    const docRef = doc(db, 'schemes', id);
    const docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() } as SchemeDetail;
    }
    return null;
  },

  /**
   * Directly fetches all service centres from Firebase Cloud Firestore
   */
  async getCenters(): Promise<CenterDetail[]> {
    const querySnapshot = await getDocs(collection(db, 'centers'));
    const centers: CenterDetail[] = [];
    querySnapshot.forEach((docSnap) => {
      centers.push({ id: docSnap.id, ...docSnap.data() } as CenterDetail);
    });
    return centers;
  },

  /**
   * Directly fetches a service centre by its ID from Firebase Cloud Firestore
   */
  async getCenterById(id: string): Promise<CenterDetail | null> {
    const docRef = doc(db, 'centers', id);
    const docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() } as CenterDetail;
    }
    return null;
  },
};
