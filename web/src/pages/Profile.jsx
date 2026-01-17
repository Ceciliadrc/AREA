/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Profile.jsx
*/

import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import BottomNav from "../components/nav/BottomNav";
import { PageTitle } from "../components/ui/PageTitle";
import ProfilePicture from "../components/profile/ProfilePicture";
import CredentialCard from "../components/profile/CredentialCard";
import Overlay from "../components/ui/Overlay";
import {colors, radius} from "../components/theme";

import api from "../apiFetcher/api.js";

export default function Profile({ goTo, onClick, style = {}}) {
  const [credentials, setCredentials] = useState([]);

  const availableCredentials = [
    { id: "google", provider: "Google" },
    { id: "spotify", provider: "Spotify" },
    { id: "twitch", provider: "Twitch" },
    // TODO: ajouter OpenAI / Instagram / Notion quand OAuth backend existe
  ];

  const [activeWorkflows, setActiveWorkflows] = useState(0);
  const [executedWorkflows, setExecutedWorkflows] = useState(0);
  const [isAdmin, setIsAdmin] = useState(false);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(false);

  // workflows stats
  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    (async () => {
      try {
        const areas = await api.getAreasByUserId(userId);
        setActiveWorkflows(Array.isArray(areas) ? areas.length : 0);

        const totalExecuted = (areas || []).reduce(
          (sum, area) => sum + (area.executed_count ?? 0),
          0
        );
        setExecutedWorkflows(totalExecuted);
      } catch (err) {
        console.error("Failed to fetch areas:", err);
      }
    })();
  }, []);

  // user role
  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    (async () => {
      try {
        const user = await api.getUserById(userId);
        setIsAdmin(user.role === "admin");
      } catch (err) {
        console.error("Failed to fetch user role:", err);
      }
    })();
  }, []);

  // Credentials
  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    (async () => {
      try {
        // TODO: implémenter route pour récupérer les active credentials
        // const data = await api.getUserCredentials(userId);
        // setCredentials(data || []);

        setCredentials([]); // fallback temporaire
      } catch (err) {
        console.error("Failed to fetch credentials:", err);
      }
    })();
  }, []);

    /*useEffect(() => {
        const userData = api.getUsers()
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');

        if (userData && token) {
            setUser(userData);
            api.setToken(token);
        } else {
            goTo('/login');
        }
    }, []);*/

  // Overlay
  const [overlayOpen, setOverlayOpen] = useState(false);
  const [overlayMode, setOverlayMode] = useState(null);
  const [selectedCredential, setSelectedCredential] = useState(null);

  const closeOverlay = () => {
    setOverlayOpen(false);
    setOverlayMode(null);
    setSelectedCredential(null);
  };

  // OAuth connect
  const handleOAuthConnect = async (serviceId) => {
    const userId = localStorage.getItem("user_id"); // TODO: implémenter les OAth2 quand ils seront dispo
    if (!userId) {
      alert("User not logged in");
      return;
    }

    try {
      let res;

      switch (serviceId) {
        case "google":
          res = await api.getGoogleLogin(userId);
          window.location.href = res.url;
          break;

        case "spotify":
          res = await api.getSpotifyLogin(userId);
          window.location.href = res.url;
          break;

        case "twitch":
          res = await api.getTwitchLogin(userId);
          window.location.href = res.url;
          break;

        default:
          alert("Service not supported yet");
      }
    } catch (err) {
      console.error("OAuth redirection failed:", err);
      alert("Failed to connect service");
    }
  };

    const handleLogout = async () => {
        setLoading(true);
        await api.logout();
        goTo("login");
    };

  return (
    <AppLayout>
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          paddingTop: 60,
          paddingBottom: 120,
        }}
      >
        <PageTitle>My profile</PageTitle>

        <button
            onClick={handleLogout}
            style={{
                width: "25%",
                padding: "12px 24px",
                borderRadius: radius.pill,
                border: "none",
                cursor: "pointer",
                fontWeight: "bold",
                color: "#fff",
                background: colors.primaryGradient,
                fontSize: 15,
                ...style,
            }}
        >
           Logout
        </button>

        {/* Profile */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 40,
            marginTop: 40,
            marginBottom: 60,
          }}
        >
          <ProfilePicture size={170} />

          <div>
            <h2 style={{ fontSize: 28, color: colors.textMain }}>
              Username
            </h2>

            <a
              href="mailto:your.email@area.com"
              style={{ color: colors.textMain }} // TODO: implémenter route api pour récupérer l'email
            >
              your.email@area.com
            </a>

            <div style={{ marginTop: 20, color: colors.textMain }}>
              <div>
                <strong>Active workflows:</strong> {activeWorkflows}
              </div>
              <div>
                <strong>Workflows executed:</strong> {executedWorkflows}
              </div>

              {isAdmin && (
                <PrimaryButton
                  style={{ marginTop: 16 }}
                  onClick={() => goTo?.("adminPanel")}
                >
                  Admin panel
                </PrimaryButton>
              )}
            </div>
          </div>
        </div>

        {/* Credentials */}
        <h2 style={{ fontSize: 26, marginBottom: 24, color: "black" }}>
          Credentials
        </h2>

        <div style={{ width: "100%", maxWidth: 900 }}>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: 24,
            }}
          >
            {credentials.map((cred) => (
              <CredentialCard
                key={cred.id}
                label={cred.provider}
                onClick={() => {
                  setSelectedCredential(cred);
                  setOverlayMode("view");
                  setOverlayOpen(true);
                }}
              />
            ))}

            <CredentialCard
              isAdd
              onClick={() => {
                setOverlayMode("add");
                setOverlayOpen(true);
              }}
            />
          </div>
        </div>
      </div>

      {/* Overlay */}
      <Overlay isOpen={overlayOpen} onClose={closeOverlay} width={460}>
        {overlayMode === "add" && (
          <>
            <h2 style={{ color: "black" }}>Connect a new service</h2>
            <p style={{ color: "black" }}>
              You will be redirected to the service OAuth page.
            </p>

            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {availableCredentials.map((cred) => (
                <PrimaryButton
                  key={cred.id}
                  onClick={() => handleOAuthConnect(cred.id)}
                >
                  Connect {cred.provider}
                </PrimaryButton>
              ))}
            </div>
          </>
        )}
      </Overlay>

      <BottomNav
        active="profile"
        onNavigate={(tab) => {
          if (tab === "list") goTo("workflowResume");
          if (tab === "create") goTo("workflowCreation");
          if (tab === "profile") goTo("profile");
        }}
      />
    </AppLayout>
  );
}
