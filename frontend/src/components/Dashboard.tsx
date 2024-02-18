import React, { useState } from "react";
import "./Dashboard.css";
import { Button } from "./Button";
import { Input } from "./Input";
import { Strength } from "./Strength";
import { QueryBox } from "./QueryBox";
import sparkles from "../assets/sparkles.svg";

interface SampleData {
	strength: string;
	score: number;
}

const developer_criteria = [
	"Code Quality",
	"Number of Commits",
	"Other Criteria",
];

const sampleData: SampleData[] = [
	{ strength: "Code Quality", score: 8 },
	{ strength: "Data Structures", score: 6 },
	{ strength: "Shell Scripting", score: 7 },
	{ strength: "Functional Programming", score: 3 },
];

const data = {
	username: "SonavAgarwal",
	queries: {
		query_0: {
			query_id: "query_0",
			query: "How competent is the programmer with web development?",
			score: 0,
			code_snippets: [
				{
					file_path: "public/js/classes.js",
					code: '\n    connectionElementText() {\n        return (this.number + 1) + ": " + this.card1.text + " & " + this.card2.text;\n    }\n\n    remove() {\n        $(this.elem).remove();\n        $(this.connectionElement).remove();\n    }\n\n    hasCardNumber(n) {\n        if (n == this.card1.number || n == this.card2.number) return true;\n        return false;\n    }\n\n    cardNumberOtherThan(n) {\n        if (n == this.card1.number) return this.card2.number;\n        if (n == this.card2.number) return this.card1.number;\n        return -1;\n    }\n\n    setText(newText) {\n        this.text = newText;\n    }\n\n    updateNumber(newNum) {\n        this.number = newNum; \n        this.elemId = "connection" + this.number;\n        this.elem.id = this.elemId;\n        this.connectionId = "text" + this.elemId;\n        this.connectionElement.id = this.connectionId;\n    }\n\n    // replaceCard(numToReplace, newNum) {\n    //     if (this.updatedNum == true) {\n    //         if (this.card1.number == this.card2.number) {\n    //             this.card1 = cards[newNum];\n    //         }\n    //         this.updatedNum = false;\n    //     } else {\n    //         if (this.card1.number == numToReplace) {\n    //             this.card1 = cards[newNum];\n    //         } else if (this.card2.number == numToReplace) {\n    //             this.card2 = cards[newNum];\n    //         }\n    //         this.updatedNum = true;\n    //     }\n    // }\n}\n\nclass Card {\n    constructor (divisions, number, text, colorNum) {\n        this.divisions = divisions;\n\n        this.angle = number * Math.PI * 2 / divisions;\n        this.number = number;\n        this.text = text;\n        this.colorNum = colorNum;\n\n\n        this.elem = document.createElement("div");\n        this.elem.classList += " card";\n        this.elem.innerHTML = this.text;\n        this.elem.id = "card" + this.number;\n\n\n        // var offset = -0.5 * width - 1;\n\n        this.elem.style.top = (Math.sin(this.angle) * 0.9 * 38 + 0.9 * 50) + (-0.5 * width - 1) + "vh";\n        this.elem.style.left = (Math.cos(this.angle) * 0.9 * 38 + 0.9 * 50) + (-0.5 * width - 1) + "vh";\n        this.renderColor();\n\n        dragElement(this.elem);\n\n        $("#mapContainer").append(this.elem);\n    }\n\n    update(length, number) {\n        this.divisions = length;\n        this.number = number;\n        this.angle = this.number * Math.PI * 2 / this.divisions;\n\n        this.elem.style.top = Math.sin(this.angle) * 0.9 * 38 + 0.9 * 50 + "vh";\n        this.elem.style.left = Math.cos(this.angle) * 0.9 * 38 + 0.9 * 50 + "vh";\n    }\n\n    remove() {\n        $(this.elem).remove();\n    }\n\n    getName() {\n        return this.text;\n    }\n\n    updateNumber(newNum) {\n        this.number = newNum;\n        this.elem.id = "card" + this.number;\n    }\n\n    setColor(colorName) {\n        this.colorNum = numToColor.indexOf(colorName);\n        this.renderColor();\n    }\n\n    renderColor() {\n        if (whiteTextColors.includes(this.colorNum)) this.elem.style.color = "white";\n        else this.elem.style.color = "var(--outlines)";\n        this.elem.style.backgroundColor = numToColor[this.colorNum];\n    }\n}',
					score: 0,
					repo_name: "Concept-Map",
					repo_url: "https://github.com/SonavAgarwal/Concept-Map",
					repo_description: "Connection Circle Code",
				},
			],
		},
		query_1: {
			query_id: "query_1",
			query: "How competent is the programmer with C++?",
			score: 0,
			code_snippets: [],
		},
	},
};

export const Dashboard = () => {
	const [githubURL, setGithubURL] = useState<string>("");
	const [errorMessage, setErrorMessage] = useState<string>("");
	const [isProfileAnalyzed, setIsProfileAnalyzed] = useState<boolean>(false);

	const handleGithubURLChange = (value: string) => {
		setGithubURL(value);
		// Clear error message when user starts typing again
		setErrorMessage("");
	};

	const analyzeProfile = () => {
		// Validate input before submission
		if (!githubURL.trim()) {
			setErrorMessage("Please enter a GitHub URL");
			return;
		}

		// Validate GitHub URL
		if (!githubURL.startsWith("github.com/")) {
			setErrorMessage("Please enter a valid GitHub URL");
			return;
		}

		// Set profile analyzed to true
		setIsProfileAnalyzed(true);

		// Add your logic to analyze the GitHub profile here
		console.log("Analyzing GitHub profile:", githubURL);
		console.log("Selected Criteria for Analysis:", selectedCriteria);
		for (let c of selectedCriteria) {
			console.log(c);
		}
	};

	// buttone state
	const [selectedCriteria, setSelectedCriteria] = useState<string[]>([]);
	const toggleCriteria = (criteria: string) => {
		console.log("criteria", criteria);
		setSelectedCriteria((prev) =>
			prev.includes(criteria)
				? prev.filter((c) => c !== criteria)
				: [...prev, criteria]
		);
	};

	return (
		<div className="center">
			<div className="dash-container">
				<div className="heading-subheading">
					<h1>
						{" "}
						<img src={sparkles} alt="sparkles" /> Evaluate a new applicant
					</h1>
					<p>
						By copying a GitHub link, Git Good extracts the desired qualities of
						candidates to analyze qualifications for a position application.
					</p>
				</div>
				<div className="inner-container">
					<div className="inner-container-questions">
						<div className="question-heading">
							<h2>GitHub Profile Link</h2>
							<Input
								placeholder="Paste Profile Link here"
								onInputChange={handleGithubURLChange}
							/>
						</div>
						{errorMessage && (
							<div className="error-message">{errorMessage}</div>
						)}
						<div className="question-heading">
							<h2>Desired Evaluation Criteria</h2>
							<div className="flex-container">
								{developer_criteria.map((criteria) => (
									<Button
										key={criteria}
										text={criteria}
										onClick={() => toggleCriteria(criteria)}
										selected={selectedCriteria.includes(criteria)}
									/>
								))}
							</div>
						</div>
					</div>
					<button className="submit" onClick={analyzeProfile}>
						Analyze Profile
					</button>
				</div>
			</div>

			{/* isProfileAnalyzed && githubURL.startsWith("github.com/") &&  */}
			<ProfileStrengths />
			<QueryBox
				query="How competent is the programmer with web development?"
				score={0}
				code_snippets={data.queries.query_0.code_snippets}
			/>
		</div>
	);
};

const ProfileStrengths = () => {
	return (
		<div className="analysis-container">
			<div className="heading-subheading">
				<h2>Profile Strengths</h2>
				<p>Describe what the profile section does here.</p>
			</div>

			<div className="strengths">
				{sampleData.map((data) => {
					return <Strength strength={data.strength} score={data.score} />;
				})}
			</div>
		</div>
	);
};
