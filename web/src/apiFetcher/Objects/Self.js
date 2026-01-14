/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** Self.js
*/

export default class Self {
    constructor(data = {}) {
        this.access_token = data.access_token ?? "";
        this.token_type = data.token_type ?? "";
        this.user_id = data.user_id ?? null;
        this.username = data.username ?? "";
    }

    static fromJson(json) {
        return new Self(json);
    }

    toJson() {
        return {
            access_token: this.access_token,
            token_type: this.token_type,
            user_id: this.user_id,
            username: this.username,
        };
    }
}
