/*
** EPITECH PROJECT, 2025
** web [WSL: Ubuntu]
** File description:
** WorkflowResume.jsx
*/

function WorkflowResume({ goTo }) {
  return (
    <div>
      <h1>Résumé du workflow</h1>
      <p>Ceci est ta page de résumé.</p>
      
      <button onClick={() => goTo("login")}>
        Retour à la page de Login
      </button>
    </div>
  );
}

export default WorkflowResume;
