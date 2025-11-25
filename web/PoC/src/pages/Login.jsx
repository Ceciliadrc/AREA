/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** Login.jsx
*/

import { useState } from "react";

function Login({ goTo }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    console.log("Login attempt = ", email, password);

    goTo("workflow"); // Mettre une condition avec le call API quand sera disponible
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Connexion</h1>

      <form onSubmit={handleSubmit} style={{ marginTop: "1rem", maxWidth: "300px" }}>
        
        <label>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email@example.com"
          required
          style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
        />

        <label>Mot de passe</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          required
          style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
        />

        <button
          type="submit"
          style={{
            width: "100%",
            padding: "0.5rem",
            cursor: "pointer",
          }}
        >
          Se connecter
        </button>
      </form>

    </div>
  );
}

export default Login;
