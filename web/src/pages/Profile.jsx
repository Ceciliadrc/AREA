/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Profile.jsx
*/

import { useState } from "react";

import AppLayout from "../components/layout/AppLayout";
import BottomNav from "../components/nav/BottomNav";
import { PageTitle } from "../components/ui/PageTitle";
import ProfilePicture from "../components/profile/ProfilePicture";
import CredentialCard from "../components/profile/CredentialCard";
import Overlay from "../components/ui/Overlay";
import TextInput from "../components/ui/TextInput";
import PrimaryButton from "../components/ui/PrimaryButton";
import { colors } from "../components/theme";

export default function Profile({ goTo }) {
  const credentials = [ // TODO: requête api
    // { id: "github", provider: "Github", account: "my-github-username" },
    // { id: "google", provider: "Google", account: "my.email@gmail.com" },
    // { id: "openAi", provider: "OpenAI", account: "openai-account" },
    // { id: "letterbox", provider: "Letterbox", account: "letterbox-user" },
    // { id: "pathe", provider: "Pathé", account: "pathe-account" },
    // { id: "meteoFrance", provider: "Météo France", account: "mf-account" },
  ];
  const availableCredentials = [ // TODO: requête api
    { id: "github", provider: "Github", URILink: "" },
    { id: "google", provider: "Google", URILink: "http://localhost:8080/auth/google/callback" },
    { id: "openAi", provider: "OpenAI", URILink: "" },
    { id: "letterbox", provider: "Letterbox", URILink: "" },
    { id: "pathe", provider: "Pathé", URILink: "" },
    { id: "meteoFrance", provider: "Météo France", URILink: "" },
  ];

  // Overlay
  const [overlayOpen, setOverlayOpen] = useState(false);
  const [overlayMode, setOverlayMode] = useState(null); // view/edit/add
  const [selectedCredential, setSelectedCredential] = useState(null);

  const openViewOverlay = (cred) => {
    setSelectedCredential(cred);
    setOverlayMode("view");
    setOverlayOpen(true);
  };

  const openEditOverlay = (cred) => {
    setSelectedCredential(cred);
    setOverlayMode("edit");
    setOverlayOpen(true);
  };

  const openAddOverlay = () => {
    setSelectedCredential(null);
    setOverlayMode("add");
    setOverlayOpen(true);
  };

  const closeOverlay = () => {
    setOverlayOpen(false);
    setOverlayMode(null);
    setSelectedCredential(null);
  };

  // Page Profil
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

        {/* Bloc profil : photo + infos */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 40,
            marginTop: 40,
            marginBottom: 60,
          }}
        >
          {/* Photo de profil */}
          <div>
            <ProfilePicture size={170} />
          </div>

          {/* Infos utilisateur */}
          <div style={{ textAlign: "left" }}>
            <h2
              style={{
                fontSize: 28,
                marginBottom: 6,
                color: colors.textMain,
              }}
            >
              Username
            </h2>

            <a
              href="mailto:your.email@area.com"
              style={{
                fontSize: 16,
                textDecoration: "underline",
                color: colors.textMain,
              }}
            >
              your.email@area.com
            </a>

            <div
              style={{
                marginTop: 20,
                fontSize: 16,
                lineHeight: 1.8,
                color: colors.textMain,
              }}
            >
              <div>
                <strong>Active workflows : </strong>2 {/* TODO: requête */}
              </div>
              <div>
                <strong>Workflows executed : </strong>23 {/* TODO: requête */}
              </div>
            </div>
          </div>
        </div>

        {/* Section Credentials */}
        <h2
          style={{
            fontSize: 26,
            marginBottom: 24,
            color: colors.textMain,
            textAlign: "center",
          }}
        >
          Credentials
        </h2>

        <div
          style={{
            width: "100%",
            maxWidth: 900,
            padding: "0 24px",
            boxSizing: "border-box",
            margin: "0 auto 80px",
          }}
        >
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
                onClick={() => openViewOverlay(cred)}   // clic sur la card = détails
                onEdit={() => openEditOverlay(cred)}    // clic sur le crayon = édition
              />
            ))}

            <CredentialCard
              isAdd
              onClick={openAddOverlay}
            />
          </div>
        </div>
      </div>

      <Overlay
        isOpen={overlayOpen}
        onClose={closeOverlay}
        width={460}
      >
        <h2
          style={{
            marginTop: 0,
            marginBottom: 16,
            fontSize: 22,
            color: colors.textMain,
          }}
        >
          {overlayMode === "view" && selectedCredential && `Details – ${selectedCredential.provider}`}
          {overlayMode === "edit" && selectedCredential && `Edit – ${selectedCredential.provider}`}
          {overlayMode === "add" && "Connect a new service"}
        </h2>

        {overlayMode === "view" && selectedCredential && (
          <div style={{ color: "black", fontSize: 14, lineHeight: 1.7 }}>
            <p><strong>Provider :</strong> {selectedCredential.provider}</p>
            <p><strong>Account :</strong> {selectedCredential.account}</p>
          </div>
        )}

        {overlayMode === "edit" && selectedCredential && (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              // TODO: requête api
              closeOverlay();
            }}
          >
            <TextInput
              label="Account name"
              defaultValue={selectedCredential.account}
              style={{ width: "95%", backgroundColor: "white" }}
              required
            />

            <PrimaryButton type="submit" style={{ marginTop: 12 }}>
              Save changes
            </PrimaryButton>
          </form>
        )}

        {overlayMode === "add" && (
          <div>
            <p style={{ color: "black", fontSize: 14, marginBottom: 16 }}>
              Choose a service to connect. You’ll be redirected to its OAuth2
              login page.
            </p>

            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {availableCredentials.map((cred) => (
                <PrimaryButton
                  key={cred.id}
                  onClick={() => {
                    window.open(cred.URILink, "_blank");
                    // TODO: requête api
                  }}
                >
                  Connect {cred.provider}
                </PrimaryButton>
              ))}
            </div>
          </div>
        )}
      </Overlay>

      <BottomNav
        active="profile"
        onNavigate={(tab) => {
          if (!goTo) return;
          if (tab === "list") goTo("workflowResume");
          else if (tab === "create") goTo("workflowCreation");
          else if (tab === "profile") goTo("profile");
        }}
      />
    </AppLayout>
  );
}
