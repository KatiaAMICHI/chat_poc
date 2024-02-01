// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Ajoutez ce fichier pour les styles

function App() {
    const [inputMessage, setInputMessage] = useState('');
    const [messages, setMessages] = useState([]);

    const sendMessage = async () => {
        try {
            const response = await axios.post(
                'http://localhost:8000/api/send-message/',
                { message: inputMessage },
                { withCredentials: true });

            setMessages([...messages, { text: inputMessage, sender: 'user' }, { text: response.data.message, sender: 'bot' }]);
            setInputMessage('');
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    useEffect(() => {
        // Fonction pour récupérer les anciens messages de l'utilisateur
        const getUserMessages = async () => {
            try {
                // Remplacez l'URL par l'URL correcte de votre backend
                const response = await axios.get('http://localhost:8000/api/get_user_messages/', { withCredentials: true });

                // Mettez à jour l'état avec les messages récupérés
                setMessages([...messages, ...response.data.user_messages]);
            } catch (error) {
                console.error('Erreur lors de la récupération des messages :', error);
            }
        };

        // Appelez la fonction pour récupérer les messages une fois que le composant est monté
        getUserMessages();
    }, []); // Le tableau vide signifie que cet effet s'exécute une fois après le montage du composant

    return (
        <div className="app-container">
            <div className="header">
                <h1>Chat App</h1>
            </div>
            <div className="chat-container">
                {messages.map((msg, index) => (
                    <div key={index} className={msg.sender}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}

export default App;
