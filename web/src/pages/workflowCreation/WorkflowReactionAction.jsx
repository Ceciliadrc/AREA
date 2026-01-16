/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** WorkflowReactionAction.jsx
*/

import { useState, useEffect } from "react";
import AppLayout from "../../components/layout/AppLayout";
import { PageTitle } from "../../components/ui/PageTitle";
import api from "../../apiFetcher/api";

export default function WorkflowReactionAction({
    service,
    value,
    onBack,
    onSelect,
}) {
    const [actions, setActions] = useState([]);

    useEffect(() => {
        if (!service) return;

        const fetchActions = async () => {
            try {
                const data = await api.getServiceReactions(service.id);
                setActions(data);
            } catch (err) {
                console.error("Failed to load actions:", err);
                // placeholders statique si l'API marche pas
                setActions([
                    { id: "new_pull_request", name: "New Pull Request" },
                    { id: "new_issue", name: "New Issue" },
                    { id: "push_to_branch", name: "Push To Branch" },
                ]);
            }
        };

        fetchActions();
    }, [service]);

    return (
        <AppLayout>
            <div
                style={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    paddingTop: 60,
                }}
            >
                <div
                    onClick={onBack}
                    style={{
                        color: "black",
                        alignSelf: "flex-start",
                        cursor: "pointer",
                    }}
                >
                    ← Back
                </div>

                <PageTitle>Choose the reaction for {service?.name}</PageTitle>

                <div
                    style={{
                        color: "black",
                        display: "flex",
                        flexDirection: "column",
                        gap: 24,
                        marginTop: 40,
                        width: "100%",
                        maxWidth: 600,
                    }}
                >
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
                                textAlign: "center",
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
