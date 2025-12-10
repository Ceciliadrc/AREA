/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Register.jsx
*/

import CenteredCardLayout from "../components/layout/CenteredCardLayout";
import { PageTitle, PageSubtitle } from "../components/ui/PageTitle";
import TextInput from "../components/ui/TextInput";
import PrimaryButton from "../components/ui/PrimaryButton";
import DividerWithText from "../components/ui/DividerWithText";
import SocialButton from "../components/ui/SocialButton";
import TextButton from "../components/ui/TextButton";
import { colors } from "../components/theme";

import GoogleLogo from "../assets/google.png";
import GithubLogo from "../assets/github.png";
import FacebookLogo from "../assets/facebook.png";

import api from "../apiFetcher/api.js";

export default function Register({ goTo }) {
  return (
    <CenteredCardLayout width={420}>
      <PageTitle>Welcome</PageTitle>
      <PageSubtitle>Register</PageSubtitle>

      <div style={{ marginTop: 24 }}>
        <form
          onSubmit={async (e) => {
            e.preventDefault();

            const formData = new FormData(e.target);
            const username = formData.get("username");
            const email = formData.get("email");
            const password = formData.get("password");

            try {
              const data = await api.register(username, email, password);

              goTo("profile");
            } catch (error) {
              console.error("Register failed:", error);
              alert("Registration failed, please try again.");
            }
          }}
        >
          <TextInput
            label="Username"
            type="text"
            name="username"
            placeholder="JohnDoe"
            style={{ width: "95%", backgroundColor: "white" }}
            required
          />
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
          </div>

          <br />

          <PrimaryButton type="submit">
            Register →
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
          Register with
        </p>

        {/* Boutons connexion google etc (non branchés pour l'instant) */}
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 20,
          }}
        >
          <SocialButton
            iconSrc={GoogleLogo}
            alt="Register with Google"
            onClick={() => console.log("Social register not implemented yet")}
          />
          <SocialButton
            iconSrc={GithubLogo}
            alt="Register with Github"
            onClick={() => console.log("Social register not implemented yet")}
          />
          <SocialButton
            iconSrc={FacebookLogo}
            alt="Register with Facebook"
            onClick={() => console.log("Social register not implemented yet")}
          />
        </div>

        <DividerWithText>or</DividerWithText>

        {/* Bouton Register */}
        <p
          style={{
            textAlign: "center",
            fontSize: 12,
            marginTop: 12,
            color: "black"
          }}
        >
          Already have an account ?{" "}
          <TextButton
            onClick={() => {
              goTo("login");
            }}
            style={{ fontWeight: "bold" }}
          >
            Login now
          </TextButton>
        </p>
      </div>
    </CenteredCardLayout>
  );
}
