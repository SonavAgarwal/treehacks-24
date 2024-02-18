import React from "react";
import "./Strength.css";
import { Bar } from "./Bar";

interface StrengthProps {
  strength: string;
  score: number;
}

export const Strength = (props: StrengthProps) => {
  return (
    <div className="strength-container">
      <h2>{props.strength}</h2>
      <Bar score={props.score} />
    </div>
  );
};
