import React from 'react';
import './App.css';
import Header from "./components/Header";
import Footer from "./components/Footer";
import MainPage from "./pages/MainPage";
import LogInPage from "./pages/LogInPage";

function App() {
    return (
        <div className="App">
            <Header/>
            <MainPage />
            <Footer />
        </div>
    );
}

export default App;
