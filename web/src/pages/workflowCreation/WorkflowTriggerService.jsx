/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** WorkflowTriggerService.jsx
*/

import { useEffect, useState } from "react";
import AppLayout from "../../components/layout/AppLayout";
import { PageTitle } from "../../components/ui/PageTitle";
import api from "../../apiFetcher/api";

export default function WorkflowTriggerService({ value, onSelect }) {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadServices = async () => {
            try {
                // TODO: changer la route avec celle qui donne les workflows connectés (besoin de la créer)
                const data = await api.getServices();
                setServices(data);
            } catch (err) {
                console.error("Failed to load services", err);
            } finally {
                setLoading(false);
            }
        };

        loadServices();
    }, []);

    return (
        <AppLayout>
            <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 60 }}>
                <PageTitle>Choose the trigger</PageTitle>

                {loading && <p>Loading services…</p>}

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
