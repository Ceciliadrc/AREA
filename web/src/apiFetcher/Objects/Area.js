/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Area.js
*/

export default class Area {

    constructor(data = {}) {
        this.id = data.id ?? null;
        this.name = data.name ?? "";
        this.user_id = data.user_id ?? null;
        this.action_id = data.action_id ?? null;
        this.reaction_id = data.reaction_id ?? null;
        this.created_at = data.created_at ?? null;
        this.updated_at = data.updated_at ?? null;
        this.executed_count = data.executed_count ?? null;
    }

    static fromJson(json) {
        return new Area(json);
    }

    toJson() {
        return {
            id: this.id,
            name: this.name,
            user_id: this.user_id,
            action_id: this.action_id,
            reaction_id: this.reaction_id,
            executed_count: this.executed_count
        };
    }
}
