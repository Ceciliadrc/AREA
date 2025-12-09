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

export default function Register({ goTo }) {
  return (
    <CenteredCardLayout width={420}>
      <PageTitle>Welcome</PageTitle>
      <PageSubtitle>Register</PageSubtitle>

      <div style={{ marginTop: 24 }}>
        <form
          onSubmit={(e) => {
            // TODO: requête api
            e.preventDefault();
            goTo("profile");
          }}
        >
          <TextInput
            label="Username"
            type="username"
            placeholder="JohnDoe"
            style={{ width: "95%", backgroundColor: "white" }}
            required
          />
          <TextInput
            label="Email"
            type="email"
            placeholder="your.email@area.com"
            style={{ width: "95%", backgroundColor: "white" }}
            required
          />
          <TextInput
            label="Password"
            type="password"
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

          <br></br>

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

        {/* Boutons connexion google etc */}
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 20,
          }}
        >
          <SocialButton iconSrc={GoogleLogo} alt="Register with Google" />
          <SocialButton iconSrc={GithubLogo} alt="Register with Github" />
          <SocialButton iconSrc={FacebookLogo} alt="Register with Facebook" />
        </div>

        <DividerWithText>or</DividerWithText>

        {/* Bouton Login */}
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
              goTo("login")
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
