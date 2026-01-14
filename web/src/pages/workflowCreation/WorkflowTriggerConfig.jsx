/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** WorkflowTriggerConfig.jsx
*/

import AppLayout from "../../components/layout/AppLayout";
import { PageTitle } from "../../components/ui/PageTitle";

export default function WorkflowTriggerConfig({
    service,
    action,
    value,
    onBack,
    onChange,
    onNext,
}) {

    const configParams = [ // TODO: requête api pour récupérer les champs de config - y est pas
        {
            id: "repository",
            label: "Repository",
            placeholder: "my_project",
        },
        {
            id: "branch",
            label: "Branch name",
            placeholder: "main",
        },
    ];

    const params = value || {};

    const handleFieldChange = (id, val) => {
        onChange({
            ...params,
            [id]: val,
        });
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
                }}
            >
                <div
                    onClick={onBack}
                    style={{ color: "black", alignSelf: "flex-start", cursor: "pointer" }}
                >
                    ← Back
                </div>

                <PageTitle>Choose the action for {service?.name}</PageTitle>
                <h2 style={{ color: "black", marginTop: 16 }}>{action?.name}</h2>

                <div
                    style={{
                        color: "black",
                        width: "100%",
                        maxWidth: 600,
                        marginTop: 40,
                        display: "flex",
                        flexDirection: "column",
                        gap: 20,
                    }}
                >
                    <label>Configuration</label>

                    {configParams.map((param) => (
                        <div
                            key={param.id}
                            style={{
                                color: "black",
                                display: "flex",
                                flexDirection: "column",
                                gap: 6,
                            }}
                        >
                            <span style={{ fontWeight: 500 }}>{param.label}</span>

                            <input
                                value={params[param.id] || ""}
                                onChange={(e) => handleFieldChange(param.id, e.target.value)}
                                placeholder={param.placeholder}
                                style={{
                                    color: "black",
                                    borderRadius: 24,
                                    border: "2px solid #C47A9E",
                                    padding: "14px 18px",
                                }}
                            />
                        </div>
                    ))}
                </div>

                <button
                    onClick={onNext}
                    style={{
                        marginTop: 40,
                        borderRadius: 24,
                        padding: "18px 80px",
                        border: "none",
                        background: "#C47A9E",
                        color: "#fff",
                        cursor: "pointer",
                    }}
                >
                    Continue
                </button>
            </div>
        </AppLayout>
    );
}
