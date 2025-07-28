import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import AskVisionInterface from "./components/AskVisionInterface";

function App() {
	const [isConnected, setIsConnected] = useState(false);
	const [loading, setLoading] = useState(false);

	useEffect(() => {
		// Check if backend is running
		checkBackendHealth();
	}, []);

	const checkBackendHealth = async () => {
		try {
			const response = await axios.get("/health");
			if (response.data.status === "healthy") {
				setIsConnected(true);
			}
		} catch (error) {
			console.log("Backend not connected:", error);
			setIsConnected(false);
		}
	};

	return (
		<div className="App">
			<header className="App-header">
				<div className="logo">
					<h1>AskVision</h1>
					<p>AI Accessibility Assistant</p>
				</div>
				<div className="status">{isConnected ? <span className="status-connected">✓ Connected</span> : <span className="status-disconnected">✗ Backend Disconnected</span>}</div>
			</header>

			<main className="App-main">
				{!isConnected ? (
					<div className="connection-error">
						<h2>Backend Not Connected</h2>
						<p>Please start the Flask backend server first:</p>
						<code>cd backend && python app.py</code>
						<button onClick={checkBackendHealth} className="retry-button">
							Retry Connection
						</button>
					</div>
				) : (
					<AskVisionInterface />
				)}
			</main>

			<footer className="App-footer">
				<p>AskVision - Making the web accessible through AI</p>
				<p>Built for the Build An Agent Hackathon</p>
			</footer>
		</div>
	);
}

export default App;
