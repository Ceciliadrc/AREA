/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** WorkflowCreation.jsx
*/

import { useState } from "react";
import WorkflowTriggerService from "./WorkflowTriggerService";
import WorkflowTriggerAction from "./WorkflowTriggerAction";
import WorkflowTriggerConfig from "./WorkflowTriggerConfig";
import WorkflowReactionService from "./WorkflowReactionService";
import WorkflowReactionAction from "./WorkflowReactionAction";
import WorkflowReactionConfig from "./WorkflowReactionConfig";
import BottomNav from "../../components/nav/BottomNav";

const STEPS = {
  TRIGGER_SERVICE: "TRIGGER_SERVICE",
  TRIGGER_ACTION: "TRIGGER_ACTION",
  TRIGGER_CONFIG: "TRIGGER_CONFIG",
  REACTION_SERVICE: "REACTION_SERVICE",
  REACTION_ACTION: "REACTION_ACTION",
  REACTION_CONFIG: "REACTION_CONFIG",
};

export default function WorkflowCreation({ goTo }) {
  const [step, setStep] = useState(STEPS.TRIGGER_SERVICE);

  const [triggerService, setTriggerService] = useState(null);
  const [triggerAction, setTriggerAction] = useState(null);
  const [triggerConfig, setTriggerConfig] = useState("");

  const [reactionService, setReactionService] = useState(null);
  const [reactionAction, setReactionAction] = useState(null);
  const [reactionConfig, setReactionConfig] = useState("");

  const buildPayload = () => ({
    trigger: {
      serviceId: triggerService.id,
      actionId: triggerAction.id,
      config: triggerConfig,
    },
    reaction: {
      serviceId: reactionService.id,
      actionId: reactionAction.id,
      config: reactionConfig,
    },
  });

  const handleCreate = async () => {
    const payload = buildPayload();
    // TODO: requête API -- oui y est

    if (goTo) {
      goTo("workflowResume");
    }
  };

  let screen = null;

  switch (step) {
    case STEPS.TRIGGER_SERVICE:
      screen = (
        <WorkflowTriggerService
          value={triggerService}
          onSelect={(service) => {
            setTriggerService(service);
            setStep(STEPS.TRIGGER_ACTION);
          }}
        />
      );
      break;

    case STEPS.TRIGGER_ACTION:
      screen = (
        <WorkflowTriggerAction
          service={triggerService}
          value={triggerAction}
          onBack={() => setStep(STEPS.TRIGGER_SERVICE)}
          onSelect={(action) => {
            setTriggerAction(action);
            setStep(STEPS.TRIGGER_CONFIG);
          }}
        />
      );
      break;

    case STEPS.TRIGGER_CONFIG:
      screen = (
        <WorkflowTriggerConfig
          service={triggerService}
          action={triggerAction}
          value={triggerConfig}
          onBack={() => setStep(STEPS.TRIGGER_ACTION)}
          onChange={setTriggerConfig}
          onNext={() => setStep(STEPS.REACTION_SERVICE)}
        />
      );
      break;

    case STEPS.REACTION_SERVICE:
      screen = (
        <WorkflowReactionService
          value={reactionService}
          onBack={() => setStep(STEPS.TRIGGER_CONFIG)}
          onSelect={(service) => {
            setReactionService(service);
            setStep(STEPS.REACTION_ACTION);
          }}
        />
      );
      break;

    case STEPS.REACTION_ACTION:
      screen = (
        <WorkflowReactionAction
          service={reactionService}
          value={reactionAction}
          onBack={() => setStep(STEPS.REACTION_SERVICE)}
          onSelect={(action) => {
            setReactionAction(action);
            setStep(STEPS.REACTION_CONFIG);
          }}
        />
      );
      break;

    case STEPS.REACTION_CONFIG:
      screen = (
        <WorkflowReactionConfig
          service={reactionService}
          action={reactionAction}
          value={reactionConfig}
          onBack={() => setStep(STEPS.REACTION_ACTION)}
          onChange={setReactionConfig}
          onCreate={handleCreate}
        />
      );
      break;

    default:
      screen = <div>Unknown step: {step}</div>;
  }

  return (
    <>
      {screen}

      <BottomNav
        active="create"
        onNavigate={(tab) => {
          if (!goTo) return;
          if (tab === "list") goTo("workflowResume");
          else if (tab === "create") goTo("workflowCreation");
          else if (tab === "profile") goTo("profile");
        }}
      />
    </>
  );
}
