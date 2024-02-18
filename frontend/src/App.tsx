import { useState } from "react";
import "./App.css";
import axios from "axios";
import { Dashboard } from "./components/Dashboard";

// convex
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function App() {
  const tasks = useQuery(api.tasks.get);

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
    <>
      <Dashboard />
      {tasks?.map(({ _id, step }) => (
        <div key={_id}>{step}</div>
      ))}
    </>
  );
}

export default App;
