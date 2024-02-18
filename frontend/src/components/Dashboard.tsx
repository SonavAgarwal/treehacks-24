import React from "react";
import './Dashboard.css'
import { Button } from "./Button";
// import { LinkInput } from "./Input";
import sparkles from "../assets/sparkles.svg"

export const Dashboard = () => {
    return (
    <div className="center">

		<div className="grid-container">

			<div className="heading-subheading">
				<h1> <img src={sparkles}/> Evaluate a new applicant</h1>
				<p>
					By copying a GitHub link, Git Good extracts the desired qualities of candidates to analyze qualifications for a position application.
				</p>
			</div>

			<div className="inner-container">

				<div className="inner-container-questions">
					<div className="question-heading"> 
						<h2>GitHub Profile Link</h2>
						<input type="text" placeholder="Paste Profile Link here"/>
					</div>
					<div className="question-heading"> 
						<h2>Desired Evaluation Criteria</h2>
						<div className="flex-container">
							<Button text="Code Quality"/>
                            <Button text="Number of Commits"/>
                            <Button text="Oh no make this super duper duper long"/>
                            <Button text="Oh no make this super duper duper long"/>
                            <Button text="This is a longer one"/>
                            <Button text="Oh no make this super duper duper long"/>
						</div>
					</div>
				</div>

				<button className="submit">Analyze Profile</button>
			</div>
		</div>
	</div>
    )
}