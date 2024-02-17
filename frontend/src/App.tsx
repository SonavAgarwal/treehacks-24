import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import axios from "axios";

function App() {
	const [name, setName] = useState<string>("");

	function fetchHelloWorld(name: string) {
		console.log(name);
		// "http://localhost:8000/analyze_account"
		return axios
			.post("http://localhost:8000/analyze_account", {
				username: name,
				queries: [
					"code for web development",
					"code using object oriented programming",
					"code applying data structures",
					"code with low level languages such as Assembly",
				],
			})
			.then((response) => {
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
			</div>
		</>
	);
}

export default App;
