/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** App.jsx
*/

import { useState } from "react";
import Login from "./pages/Login";
import WorkflowResume from "./pages/WorkflowResume";

function App() {
  const [page, setPage] = useState("login");

  return (
    <>
      {page === "login" && <Login goTo={setPage} />}
      {page === "workflow" && <WorkflowResume goTo={setPage} />}
    </>
  );
}

export default App;
