import axios from "axios";
import { useState } from "react";
import "./App.css";

function App() {
	const [name, setName] = useState<string>("sophiasharif");

	function fetchHelloWorld(name: string = "SonavAgarwal") {
		console.log(name);
		// "http://localhost:8000/analyze_account"
		return axios
			.post("http://localhost:8000/analyze_account", {
				username: name,
				queries: [
					// "How well can the candidate work with low level memory management?",
					// "Is the candidate familiar with regular expressions?",
					// "What databases is the candidate familiar with?",
					"How competent is the programmer with web development?",
					// "Can the candidate set up an authentication system?",
				],
			})
			.then((response) => {
				console.log(response);
			});
	}

	function sophiaFunction() {
		return axios.get("http://localhost:8000/testing").then((response) => {
			console.log(response);
		});
	}

	return (
		<>
			<div>
				<h1>Hello World</h1>
				<input
					type="text"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>
				<button
					onClick={() => {
						fetchHelloWorld(name);
					}}
				>
					Fetch
				</button>
				<button
					onClick={() => {
						sophiaFunction();
					}}
				>
					Sophia button
				</button>
			</div>
		</>
	);
}

export default App;
