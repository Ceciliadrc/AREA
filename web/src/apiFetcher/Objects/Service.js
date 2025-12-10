/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Service.js
*/

export default class Service {

    constructor(data = {}) {
        this.id = data.id ?? null;
        this.name = data.name ?? "";
        this.logo = data.logo ?? "";
        this.description = data.description ?? "";
        this.actions = data.actions ?? [];        // API /services/{id}/actions
        this.reactions = data.reactions ?? [];    // API /services/{id}/reactions
    }

    static fromJson(json) {
        return new Service(json);
    }

    toJson() {
        return {
            id: this.id,
            name: this.name,
            logo: this.logo,
            description: this.description
        };
    }
}
