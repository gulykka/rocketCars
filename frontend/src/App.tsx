import React from 'react';
import './App.css';
import LogInPage from "./pages/LogInPage";
import Header from "./components/Header";
import Footer from "./components/Footer";

function App() {
    return (
        <div className="App">
            <Header/>
            <LogInPage/>
            <Footer />
        </div>
    );
}

export default App;
