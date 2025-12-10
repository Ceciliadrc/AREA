/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Login.jsx
*/

import CenteredCardLayout from "../components/layout/CenteredCardLayout";
import { PageTitle, PageSubtitle } from "../components/ui/PageTitle";
import TextInput from "../components/ui/TextInput";
import CheckboxWithLabel from "../components/ui/CheckboxWithLabel";
import PrimaryButton from "../components/ui/PrimaryButton";
import DividerWithText from "../components/ui/DividerWithText";
import SocialButton from "../components/ui/SocialButton";
import TextButton from "../components/ui/TextButton";
import { colors } from "../components/theme";

import GoogleLogo from "../assets/google.png";
import GithubLogo from "../assets/github.png";
import FacebookLogo from "../assets/facebook.png";

import api from "../apiFetcher/api.js";

export default function Login({ goTo }) {
  return (
    <CenteredCardLayout width={420}>
      <PageTitle>Welcome</PageTitle>
      <PageSubtitle>Login</PageSubtitle>

      <div style={{ marginTop: 24 }}>
        <form
          onSubmit={async (e) => {
            e.preventDefault();

            const formData = new FormData(e.target);
            const email = formData.get("email");
            const password = formData.get("password");

            try {
              await api.login(email, password); // POST /auth/login
              goTo("profile");
            } catch (error) {
              console.error("Login failed:", error);
              // TODO: afficher un message d'erreur propre dans l'UI
              alert("Login failed, please check your credentials.");
            }
          }}
        >
          <TextInput
            label="Email"
            type="email"
            name="email"
            placeholder="your.email@area.com"
            style={{ width: "95%", backgroundColor: "white" }}
            required
          />

          <TextInput
            label="Password"
            type="password"
            name="password"
            placeholder="********"
            style={{ width: "95%", backgroundColor: "white" }}
            required
          />

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginTop: 8,
              marginBottom: 18,
              fontSize: 13,
            }}
          >
            <CheckboxWithLabel label="Remember me" />
            <TextButton style={{ color: colors.primary }}>
              Forgot password ?
            </TextButton>
          </div>

          <PrimaryButton type="submit">
            Login →
          </PrimaryButton>
        </form>

        <DividerWithText>or</DividerWithText>

        <p
          style={{
            textAlign: "center",
            fontSize: 12,
            marginBottom: 16,
            color: colors.textMuted,
          }}
        >
          login with
        </p>

        {/* Boutons connexion social (non branchés pour l'instant) */}
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 20,
          }}
        >
          <SocialButton
            iconSrc={GoogleLogo}
            alt="Login with Google"
            onClick={() => {
              // TODO: implémenter plus tard /auth/google si besoin
              console.log("Social login not implemented yet");
            }}
          />
          <SocialButton
            iconSrc={GithubLogo}
            alt="Login with Github"
            onClick={() => {
              console.log("Social login not implemented yet");
            }}
          />
          <SocialButton
            iconSrc={FacebookLogo}
            alt="Login with Facebook"
            onClick={() => {
              console.log("Social login not implemented yet");
            }}
          />
        </div>

        <DividerWithText>or</DividerWithText>

        {/* Bouton register */}
        <p
          style={{
            textAlign: "center",
            fontSize: 12,
            marginTop: 12,
            color: "black"
          }}
        >
          Don't have an account yet ?{" "}
          <TextButton
            onClick={() => {
              goTo("register")
            }}
            style={{ fontWeight: "bold" }}
          >
            Register now
          </TextButton>
        </p>
      </div>
    </CenteredCardLayout>
  );
}
