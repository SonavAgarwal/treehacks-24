import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import axios from "axios";

function App() {
	const [name, setName] = useState<string>("");

	function fetchHelloWorld(name: string) {
		return axios
			.get("http://localhost:8000/hello/John")
			.then(function (response) {
				console.log(response.data);
			})
			.catch(function (error) {
				console.error("Error:", error);
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
