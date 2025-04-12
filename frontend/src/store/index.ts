import { configureStore } from '@reduxjs/toolkit';
import carReducer from './slices/carSlice';

export const store = configureStore({
  reducer: {
    car: carReducer,
    // другие редюсеры можно добавить здесь
  },
});

// Типы для TypeScript
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Экспорт хранилища по умолчанию
export default store;