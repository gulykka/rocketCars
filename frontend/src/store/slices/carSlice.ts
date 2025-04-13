import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { CarResponse } from '../types/carTypes';

interface CarState {
    isAuth: boolean;
    data: CarResponse | null;
    error: string | null;
    status: 'loading' | 'succeeded' | 'failed' | null;
}

// const loadCarDetailsFromLocalStorage = () => {
//     const name = localStorage.getItem('carName');
//     const VIN = localStorage.getItem('carVIN');
//     return { name, VIN };
// };

export const fetchGetCar = createAsyncThunk(
    'carSlice/fetchGetCar',
    async ({ name, VIN }: { name: string; VIN: string }, thunkAPI) => {
        try {
            await new Promise(resolve => setTimeout(resolve, 1000));
            const response = await fetch(`/api/${encodeURIComponent(name)}/${encodeURIComponent(VIN)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            console.log(data)
            if (data.status_code !== 200) {
                return thunkAPI.rejectWithValue(data.message);
            }
            localStorage.setItem('carName', name);
            localStorage.setItem('carVIN', VIN);

            return data.data;
        } catch (error: any) {
            return thunkAPI.rejectWithValue(error.message);
        }
    }
);

const initialState: CarState = {
    isAuth: false,
    data: null,
    error: null,
    status: null,
};

const carSlice = createSlice({
    name: 'car',
    initialState,
    reducers: {
        signOut(state) {
            state.data = null;
            state.isAuth = false;
            state.error = null;
            state.status = null;
            localStorage.removeItem('carState');
            localStorage.removeItem('carName');
            localStorage.removeItem('carVIN');
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchGetCar.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.error = null;
                state.data = action.payload;
                state.isAuth = true;
            })
            .addCase(fetchGetCar.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchGetCar.rejected, (state, action) => {
                state.status = 'failed';
                state.isAuth = false;
                state.error = action.payload as string || 'Произошла ошибка! Попробуйте снова.';
            });
    },
});

// Проверяем наличие имени и VIN в localStorage и вызываем fetchGetCar
// const { name, VIN } = loadCarDetailsFromLocalStorage();
// if (name && VIN) {
//     fetchGetCar({ name, VIN }); // Это не сработает, так как вызов не в контексте Redux
// }

export const { signOut } = carSlice.actions;

export default carSlice.reducer;

