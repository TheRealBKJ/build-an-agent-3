import React, { useState, useEffect } from "react";
import "./VoiceInput.css";

const VoiceInput = ({ onTranscript }) => {
	const [isListening, setIsListening] = useState(false);
	const [transcript, setTranscript] = useState("");
	const [isSupported, setIsSupported] = useState(false);

	useEffect(() => {
		// Check if speech recognition is supported
		if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
			setIsSupported(true);
		}
	}, []);

	const startListening = () => {
		if (!isSupported) {
			alert("Speech recognition is not supported in this browser.");
			return;
		}

		const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
		const recognition = new SpeechRecognition();

		recognition.continuous = false;
		recognition.interimResults = false;
		recognition.lang = "en-US";

		recognition.onstart = () => {
			setIsListening(true);
			setTranscript("");
		};

		recognition.onresult = (event) => {
			const transcript = event.results[0][0].transcript;
			setTranscript(transcript);
			onTranscript(transcript);
		};

		recognition.onerror = (event) => {
			console.error("Speech recognition error:", event.error);
			setIsListening(false);
		};

		recognition.onend = () => {
			setIsListening(false);
		};

		recognition.start();
	};

	const stopListening = () => {
		setIsListening(false);
	};

	if (!isSupported) {
		return (
			<div className="voice-input">
				<p className="not-supported">Speech recognition is not supported in this browser.</p>
			</div>
		);
	}

	return (
		<div className="voice-input">
			<div className="voice-controls">
				{!isListening ? (
					<button onClick={startListening} className="voice-btn start-btn" title="Start voice input">
						🎤 Start Voice Input
					</button>
				) : (
					<button onClick={stopListening} className="voice-btn stop-btn" title="Stop voice input">
						⏹️ Stop Voice Input
					</button>
				)}
			</div>

			{isListening && (
				<div className="listening-indicator">
					<div className="pulse"></div>
					<span>Listening...</span>
				</div>
			)}

			{transcript && (
				<div className="transcript-display">
					<strong>You said:</strong> {transcript}
				</div>
			)}
		</div>
	);
};

export default VoiceInput;
