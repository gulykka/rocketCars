import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { CarResponse } from '../types/carTypes';

interface CarState {
  isAuth: boolean;
  data: CarResponse | null;
  loading: boolean;
  error: string | null;
}

const initialState: CarState = {
  isAuth: false,
  data: null,
  loading: false,
  error: null,
};

const carSlice = createSlice({
  name: 'car',
  initialState,
  reducers: {
    login(state) {
        state.isAuth = true
    },
    fetchCarStart(state) {
      state.loading = true;
      state.error = null;
    },
    fetchCarSuccess(state, action: PayloadAction<CarResponse>) {
      state.data = action.payload;
      state.isAuth = true; // Устанавливаем аутентификацию в true при успешном запросе
      state.loading = false;
    },
    fetchCarFailure(state, action: PayloadAction<string>) {
      state.error = action.payload;
      state.isAuth = false;
      state.loading = false;
    },
    resetCarState(state) {
      state.isAuth = false;
      state.data = null;
      state.error = null;
      state.loading = false;
    },
    // Дополнительный action для явного управления аутентификацией
    setAuthStatus(state, action: PayloadAction<boolean>) {
      state.isAuth = action.payload;
    }
  },
});

export const {
  fetchCarStart,
  login,
  fetchCarSuccess,
  fetchCarFailure,
  resetCarState,
  setAuthStatus
} = carSlice.actions;

export default carSlice.reducer;