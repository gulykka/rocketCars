import React from 'react';
import './App.css';
import Header from "./components/Header";
import Footer from "./components/Footer";
import AppRouter from "./components/router/AppRouter";
import { BrowserRouter as Router } from 'react-router-dom';

function App() {
    return (
        <Router>
            <div className="App">
                <Header/>
                <Footer />
                <AppRouter />
            </div>
        </Router>
    );
}

export default App;
