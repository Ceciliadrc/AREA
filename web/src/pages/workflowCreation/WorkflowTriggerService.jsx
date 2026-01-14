/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** WorkflowTriggerService.jsx
*/

import AppLayout from "../../components/layout/AppLayout";
import { PageTitle } from "../../components/ui/PageTitle";

export default function WorkflowTriggerService({ value, onSelect }) {

    const services = [ // TODO: requête api -- ça y est
        { id: "gmail", name: "Gmail" },
        // ...
    ];

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
                <PageTitle>Choose the trigger</PageTitle>

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns: "repeat(2, 260px)",
                        gap: 32,
                        marginTop: 40,
                    }}
                >
                    {services.map((service) => (
                        <button
                            key={service.id}
                            onClick={() => onSelect(service)}
                            style={{
                                color: "black",
                                borderRadius: 24,
                                padding: "24px 32px",
                                border: "2px solid #C47A9E",
                                background: "transparent",
                                cursor: "pointer",
                            }}
                        >
                            {service.name}
                        </button>
                    ))}
                </div>
            </div>
        </AppLayout>
    );
}
