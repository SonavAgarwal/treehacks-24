import React from "react";
import './Strength.css'
import { Bar } from "./Bar";


export const Strength = (props) => {
  const bruh = props.text;

  return (
    <div className="strength-container">
      <h2>{bruh}</h2>

      <h2>hihi</h2>

      <Bar >ok</Bar>  

    </div>
  );
};
