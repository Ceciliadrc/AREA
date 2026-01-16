/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** WorkflowResume.jsx
*/

import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import BottomNav from "../components/nav/BottomNav";
import { PageTitle } from "../components/ui/PageTitle";
import PrimaryButton from "../components/ui/PrimaryButton";
import { colors } from "../components/theme";
import api from "../apiFetcher/api";
import WorkflowCard from "../components/ui/WorkflowCard";

export default function WorkflowResume({ goTo }) {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    const fetchWorkflows = async () => {
      try {
        const data = await api.getAreasByUserId(userId);
        setWorkflows(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Can't fetch workflows:", error);
        alert("Failed to load workflows.");
      } finally {
        setLoading(false);
      }
    };

    fetchWorkflows();
  }, []);

  return (
    <AppLayout>
      <div style={{ flex: 1, paddingTop: 60, paddingBottom: 120, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <PageTitle>My workflows</PageTitle>

        {loading && <p style={{ marginTop: 40, color: colors.textMuted }}>Loading your workflows…</p>}

        {!loading && workflows.length === 0 && (
          <div style={{ marginTop: 60, textAlign: "center" }}>
            <p style={{ color: colors.textMuted, marginBottom: 24 }}>You don’t have any workflow yet.</p>
            <PrimaryButton onClick={() => goTo("workflowCreation")}>Create your first workflow</PrimaryButton>
          </div>
        )}

        <div style={{ width: "100%", maxWidth: 900, marginTop: 40, padding: "0 24px", boxSizing: "border-box", display: "flex", flexDirection: "column", gap: 20 }}>
          {workflows.map((area) => (
            <WorkflowCard
              key={area.id}
              area={area}
              onEdit={() => goTo("workflowCreation")}
              onDelete={async () => {
                try {
                  await api.deleteAreaById(area.id);
                  setWorkflows((prev) => prev.filter((w) => w.id !== area.id));
                } catch {
                  alert("Failed to delete workflow");
                }
              }}
            />
          ))}
        </div>
      </div>

      <BottomNav active="list" onNavigate={(tab) => goTo(tab === "list" ? "workflowResume" : tab === "create" ? "workflowCreation" : "profile")} />
    </AppLayout>
  );
}
