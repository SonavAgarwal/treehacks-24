import "./Dashboard.css";
import axios from "axios";
import { Button } from "./Button";
// import { LinkInput } from "./Input";
import sparkles from "../assets/sparkles.svg";
import { useState } from "react";

export const Dashboard = () => {
  const handleSubmit = () => {
    axios
      .post("http://localhost:8000/analyze_account", {
        username: profileLink,
        queries: [], // Add actual queries here
        criteria: [], // Add actual criteria here
      })
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
  };
  let [profileLink, setProfileLink] = useState("");
  return (
    <div className="center">
      <div className="grid-container">
        <div className="heading-subheading">
          <h1>
            {" "}
            <img src={sparkles} /> Evaluate a new applicant
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
              <input
                type="text"
                placeholder="Paste Profile Link here"
                value={profileLink}
                onChange={(e) => setProfileLink(e.target.value)}
              />
            </div>
            <div className="question-heading">
              <h2>Desired Evaluation Criteria</h2>
              <div className="flex-container">
                <Button text="Code Quality" />
                <Button text="Number of Commits" />
                <Button text="Oh no make this super duper duper long" />
                <Button text="Oh no make this super duper duper long" />
                <Button text="This is a longer one" />
                <Button text="Oh no make this super duper duper long" />
              </div>
            </div>
          </div>

          <button className="submit" onClick={handleSubmit}>
            Analyze Profile
          </button>
        </div>
      </div>
    </div>
  );
};
