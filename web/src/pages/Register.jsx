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
  const handleSocialRegister = async (provider) => {
    try {
      const url = await api.getSocialRegisterUrl(provider);
      window.location.href = url; // redirection OAuth
    } catch (err) {
      console.error(`${provider} OAuth failed:`, err);
      alert("Social register failed.");
    }
  };

  return (
    <CenteredCardLayout width={420}>
      <PageTitle>Welcome</PageTitle>
      <PageSubtitle>Register</PageSubtitle>

      <form
        style={{ marginTop: 24 }}
        onSubmit={async (e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          const username = formData.get("username");
          const email = formData.get("email");
          const password = formData.get("password");

          try {
            const data = await api.register(username, email, password);
            localStorage.setItem("user_id", data.id);
            goTo("profile");
          } catch (error) {
            console.error("Register failed:", error);
            alert(error?.response?.data?.detail || "Registration failed");
          }
        }}
      >
        <TextInput label="Username" type="text" name="username" placeholder="JohnDoe" style={{ width: "95%", backgroundColor: "white" }} required />
        <TextInput label="Email" type="email" name="email" placeholder="your.email@area.com" style={{ width: "95%", backgroundColor: "white" }} required />
        <TextInput label="Password" type="password" name="password" placeholder="********" style={{ width: "95%", backgroundColor: "white" }} required />

        <br />
        <PrimaryButton type="submit">Register →</PrimaryButton>
      </form>

      <DividerWithText>or</DividerWithText>

      <p style={{ textAlign: "center", fontSize: 12, marginBottom: 16, color: colors.textMuted }}>Register with</p>
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <SocialButton iconSrc={GoogleLogo} alt="Google" onClick={() => handleSocialRegister("google")} />
      </div>

      <DividerWithText>or</DividerWithText>

      <p style={{ textAlign: "center", fontSize: 12, marginTop: 12, color: "black" }}>
        Already have an account?{" "}
        <TextButton onClick={() => goTo("login")} style={{ fontWeight: "bold" }}>Login now</TextButton>
      </p>
    </CenteredCardLayout>
  );
}
