import React, { useState } from "react";
import "./Dashboard.css";
import { Button } from "./Button";
import { Input } from "./Input";
import { Strength } from "./Strength";
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
      {
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
      }
    </div>
  );
};
