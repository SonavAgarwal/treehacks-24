import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import axios from "axios";
import { Dashboard } from "./components/Dashboard";

function App() {
	const [name, setName] = useState<string>("");

	function fetchHelloWorld() {
		// "http://localhost:8000/analyze_account"
		return axios
			.post("http://localhost:8000/analyze_account", {
				files: [
					"filter_blind_alleys.ml",
					"find_the_cheese.js",
					"meow.hs",
					"help.tsx",
				],
				query: "code that uses functional programming",
			})
			.then((response) => {
				console.log(response);
			});
	}

	return (
		// <>
		// 	<div>
		// 		<h1>Hello World</h1>
		// 		<input
		// 			type="text"
		// 			value={name}
		// 			onChange={(e) => setName(e.target.value)}
		// 		/>
		// 		<button
		// 			onClick={() => {
		// 				fetchHelloWorld();
		// 			}}
		// 		>
		// 			Fetch
		// 		</button>
		// 	</div>
		// </>
		<Dashboard/>
	);
}

export default App;
