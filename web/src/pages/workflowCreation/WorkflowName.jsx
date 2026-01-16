/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** WorkflowName.jsx
*/

import AppLayout from "../../components/layout/AppLayout";
import { PageTitle } from "../../components/ui/PageTitle";
import TextInput from "../../components/ui/TextInput";
import PrimaryButton from "../../components/ui/PrimaryButton";

export default function WorkflowName({
    workflowName,
    setWorkflowName,
    onConfirm
}) {
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
                <PageTitle>Name your workflow</PageTitle>

                <div style={{ width: 420, marginTop: 32 }}>
                    <TextInput
                        label="Workflow name"
                        placeholder="Ex: Gmail → Discord"
                        value={workflowName}
                        onChange={e => setWorkflowName(e.target.value)}
                    />
                </div>

                <PrimaryButton
                    style={{ marginTop: 32 }}
                    disabled={!workflowName.trim()}
                    onClick={onConfirm}
                >
                    Create workflow
                </PrimaryButton>
            </div>
        </AppLayout>
    );
}
