/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** App.jsx
*/

import { useState } from "react";
import Login from "./pages/Login";
import WorkflowResume from "./pages/WorkflowResume";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import WorkflowCreation from "./pages/workflowCreation/WorkflowCreation";

function App() {
  const [page, setPage] = useState("login");

  return (
    <>
      {page === "componentTest" && <ComponentsTest goTo={setPage} />}
      {page === "login" && <Login goTo={setPage} />}
      {page === "register" && <Register goTo={setPage} />}
      {page === "profile" && <Profile goTo={setPage} />}
      {page === "workflowCreation" && <WorkflowCreation goTo={setPage} />}
      {page === "workflowResume" && <WorkflowResume goTo={setPage} />}
    </>
  );
}

export default App;
