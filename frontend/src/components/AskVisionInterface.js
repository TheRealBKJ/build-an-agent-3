import React, { useState, useRef } from "react";
import axios from "axios";
import VoiceInput from "./VoiceInput";
import "./AskVisionInterface.css";

const AskVisionInterface = () => {
	const [url, setUrl] = useState("");
	const [question, setQuestion] = useState("");
	const [answer, setAnswer] = useState("");
	const [loading, setLoading] = useState(false);
	const [structuredContent, setStructuredContent] = useState(null);
	const [conversationHistory, setConversationHistory] = useState([]);
	const [isProcessing, setIsProcessing] = useState(false);

	const handleUrlSubmit = async (e) => {
		e.preventDefault();
		if (!url.trim()) return;

		setLoading(true);
		try {
			const response = await axios.post("/process-url", { url });
			if (response.data.success) {
				setStructuredContent(response.data.structured_content);
				setAnswer("✅ URL processed successfully! You can now ask questions about this webpage.");
			}
		} catch (error) {
			setAnswer(`❌ Error processing URL: ${error.response?.data?.error || error.message}`);
		} finally {
			setLoading(false);
		}
	};

	const handleQuestionSubmit = async (e) => {
		e.preventDefault();
		if (!question.trim() || !structuredContent) return;

		setIsProcessing(true);
		try {
			const response = await axios.post("/ask-question", {
				question,
				structured_content: structuredContent,
			});

			if (response.data.success) {
				const newAnswer = response.data.answer;
				setAnswer(newAnswer);

				// Add to conversation history
				setConversationHistory((prev) => [
					...prev,
					{
						question,
						answer: newAnswer,
						timestamp: new Date().toLocaleTimeString(),
					},
				]);
			}
		} catch (error) {
			setAnswer(`❌ Error answering question: ${error.response?.data?.error || error.message}`);
		} finally {
			setIsProcessing(false);
			setQuestion("");
		}
	};

	const handleVoiceInput = (transcript) => {
		setQuestion(transcript);
	};

	const handleQuickQuestion = (quickQuestion) => {
		setQuestion(quickQuestion);
	};

	const clearConversation = () => {
		setConversationHistory([]);
		setAnswer("");
		setStructuredContent(null);
		setUrl("");
	};

	return (
		<div className="askvision-interface">
			<div className="interface-container">
				{/* URL Input Section */}
				<div className="url-section">
					<h2>Step 1: Enter a URL</h2>
					<form onSubmit={handleUrlSubmit} className="url-form">
						<input type="url" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://www.amazon.com/product/..." className="url-input" disabled={loading} />
						<button type="submit" className="submit-btn" disabled={loading}>
							{loading ? "Processing..." : "Process URL"}
						</button>
					</form>
				</div>

				{/* Question Input Section */}
				{structuredContent && (
					<div className="question-section">
						<h2>Step 2: Ask a Question</h2>

						{/* Quick Questions */}
						<div className="quick-questions">
							<h3>Quick Questions:</h3>
							<div className="quick-buttons">
								<button onClick={() => handleQuickQuestion("What do the top 3 reviews say?")}>Top Reviews</button>
								<button onClick={() => handleQuickQuestion("What's the total cost with shipping?")}>Total Cost</button>
								<button onClick={() => handleQuickQuestion("How many 5-star ratings are there?")}>5-Star Count</button>
								<button onClick={() => handleQuickQuestion("What are the main product features?")}>Product Features</button>
							</div>
						</div>

						{/* Voice Input */}
						<div className="voice-input-section">
							<h3>Voice Input:</h3>
							<VoiceInput onTranscript={handleVoiceInput} />
						</div>

						{/* Text Input */}
						<form onSubmit={handleQuestionSubmit} className="question-form">
							<textarea value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask any question about this webpage..." className="question-input" disabled={isProcessing} rows="3" />
							<button type="submit" className="submit-btn" disabled={isProcessing}>
								{isProcessing ? "Thinking..." : "Ask Question"}
							</button>
						</form>
					</div>
				)}

				{/* Answer Display */}
				{answer && (
					<div className="answer-section">
						<h2>AskVision's Answer:</h2>
						<div className="answer-content">
							<p>{answer}</p>
						</div>
					</div>
				)}

				{/* Conversation History */}
				{conversationHistory.length > 0 && (
					<div className="conversation-history">
						<h2>Conversation History</h2>
						<div className="history-list">
							{conversationHistory.map((item, index) => (
								<div key={index} className="history-item">
									<div className="question">
										<strong>Q:</strong> {item.question}
									</div>
									<div className="answer">
										<strong>A:</strong> {item.answer}
									</div>
									<div className="timestamp">{item.timestamp}</div>
								</div>
							))}
						</div>
						<button onClick={clearConversation} className="clear-btn">
							Clear History
						</button>
					</div>
				)}
			</div>
		</div>
	);
};

export default AskVisionInterface;
