/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Action.js
*/

export default class Action {

    constructor(data = {}) {
        this.id = data.id ?? null;
        this.name = data.name ?? "";
        this.description = data.description ?? "";
        this.service_id = data.service_id ?? null;
    }

    static fromJson(json) {
        return new Action(json);
    }
}
