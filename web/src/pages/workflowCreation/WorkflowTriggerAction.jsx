/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** WorkflowTriggerAction.jsx
*/

import { useEffect, useState } from "react";
import AppLayout from "../../components/layout/AppLayout";
import { PageTitle } from "../../components/ui/PageTitle";
import api from "../../apiFetcher/api";

export default function WorkflowTriggerAction({ service, value, onBack, onSelect }) {
    const [actions, setActions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!service?.id) return;

        const loadActions = async () => {
            try {
                const data = await api.getServiceActions(service.id);
                setActions(data);
            } catch (err) {
                console.error("Failed to load actions", err);
            } finally {
                setLoading(false);
            }
        };

        loadActions();
    }, [service]);

    return (
        <AppLayout>
            <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 60 }}>
                <div onClick={onBack} style={{ color: "black", alignSelf: "flex-start", cursor: "pointer" }}>
                    ← Back
                </div>

                <PageTitle>Choose the action for {service?.name}</PageTitle>

                {loading && <p>Loading actions…</p>}

                <div style={{ display: "flex", flexDirection: "column", gap: 24, marginTop: 40, width: "100%", maxWidth: 600 }}>
                    {actions.map((action) => (
                        <button
                            key={action.id}
                            onClick={() => onSelect(action)}
                            style={{
                                color: "black",
                                borderRadius: 24,
                                padding: "18px 24px",
                                border: "2px solid #C47A9E",
                                background: "transparent",
                                cursor: "pointer",
                            }}
                        >
                            {action.name}
                        </button>
                    ))}
                </div>
            </div>
        </AppLayout>
    );
}
