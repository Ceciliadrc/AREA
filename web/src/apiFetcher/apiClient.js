/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR
** File description:
** apiClient.js
*/

import { API_ENDPOINTS, API_RESPONSE_CODE } from "./apiConfig.js";
import Action from "./Objects/Action.js";
import Reaction from "./Objects/Reaction.js";
import Area from "./Objects/Area.js";
import Service from "./Objects/Service.js";
import Info from "./Objects/Info.js";
import GoogleLogin from "./Objects/GoogleLogin.js";

class ApiClient {
    baseUrl;
    token;

    constructor() {
        this.baseUrl =
            import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";
        this.token = null;
    }

    setToken(token) {
        this.token = token;
    }

    clearToken() {
        this.token = null;
    }

    buildUrl(endpoint) {
        return (
            this.baseUrl.replace(/\/+$/, "") +
            "/" +
            String(endpoint).replace(/^\/+/, "")
        );
    }

    async request(endpoint, options = {}) {
        const url = this.buildUrl(endpoint);

        const init = {
            method: options.method || "GET",
            headers: {
                accept: "application/json",
                ...(this.token
                    ? { Authorization: `Bearer ${this.token}` }
                    : {}),
                ...(options.headers || {})
            }
        };

        if (options.body !== undefined) {
            init.body =
                typeof options.body === "string"
                    ? options.body
                    : JSON.stringify(options.body);

            init.headers["Content-Type"] =
                init.headers["Content-Type"] || "application/json";
        }

        const res = await fetch(url, init);

        if (!res.ok) {
            let payload = null;
            try {
                payload = await res.json();
            } catch {}

            const error = new Error(
                payload?.detail ||
                    payload?.error ||
                    payload?.message ||
                    `HTTP ${res.status}`
            );
            error.status = res.status;
            error.payload = payload;
            throw error;
        }

        if (res.status === 204)
            return null;

        return res.json();
    }

    // Auth

    async register(username, email, password) {
        return this.request(API_ENDPOINTS.register, {
            method: "POST",
            body: { username, email, password }
        });
    }

    async login(email, password) {
        const data = await this.request(API_ENDPOINTS.login, {
            method: "POST",
            body: { email, password }
        });

        if (data?.access_token || data?.token)
            this.token = data.access_token || data.token;

        return data;
    }

    async verifyToken(token = this.token) {
        if (!token)
            throw new Error("No token to verify");

        return this.request(
            `${API_ENDPOINTS.verify}?token=${encodeURIComponent(token)}`,
            { method: "POST" }
        );
    }

    async getMe() {
        return this.request(API_ENDPOINTS.me);
    }

    async getMyRole() {
        return this.request(API_ENDPOINTS.myRole);
    }

    async getUsers() {
        return this.request(API_ENDPOINTS.users);
    }

    async getUserById(userId) {
        return this.request(`${API_ENDPOINTS.users}/${userId}`);
    }

    async deleteUser(userId) {
        await this.request(`${API_ENDPOINTS.users}/${userId}`, {
            method: "DELETE"
        });
        return API_RESPONSE_CODE.OK;
    }

    async updateUserRole(userId, newRole) {
        return this.request(
            `${API_ENDPOINTS.users}/${userId}/role?new_role=${encodeURIComponent(
                newRole
            )}`,
            { method: "PUT" }
        );
    }

    // OAuth

    async getGoogleLogin(userId) {
        const data = await this.request(
            `${API_ENDPOINTS.googleLogin}?user_id=${encodeURIComponent(userId)}`
        );
        return new GoogleLogin(data);
    }

    async googleCallback({ code, state, user_id }) {
        const params = new URLSearchParams({ code, state, user_id });
        return this.request(
            `${API_ENDPOINTS.googleCallback}?${params.toString()}`
        );
    }

    async getSpotifyLogin(userId) {
        return this.request(
            `${API_ENDPOINTS.spotifyLogin}?user_id=${encodeURIComponent(userId)}`
        );
    }

    async spotifyCallback({ code, state }) {
        const params = new URLSearchParams({ code, state });
        return this.request(
            `${API_ENDPOINTS.spotifyCallback}?${params.toString()}`
        );
    }

    async getTwitchLogin(userId) {
        return this.request(
            `${API_ENDPOINTS.twitchLogin}?user_id=${encodeURIComponent(userId)}`
        );
    }

    async twitchCallback({ code, state, user_id }) {
        const params = new URLSearchParams({ code, state, user_id });
        return this.request(
            `${API_ENDPOINTS.twitchCallback}?${params.toString()}`
        );
    }

    // Services

    async getServices() {
        const data = await this.request(API_ENDPOINTS.services);
        return Array.isArray(data)
            ? data.map(s => new Service(s))
            : [];
    }

    async getServiceById(serviceId) {
        const data = await this.request(
            `${API_ENDPOINTS.services}/${serviceId}`
        );
        return new Service(data);
    }

    async getServiceActions(serviceId) {
        const data = await this.request(
            `${API_ENDPOINTS.services}/${serviceId}/actions`
        );
        return Array.isArray(data)
            ? data.map(a => new Action(a))
            : [];
    }

    async getServiceReactions(serviceId) {
        const data = await this.request(
            `${API_ENDPOINTS.services}/${serviceId}/reactions`
        );
        return Array.isArray(data)
            ? data.map(r => new Reaction(r))
            : [];
    }

    async getActionConfig(serviceName, actionName) {
        return this.request(
            `${API_ENDPOINTS.services}/actions/${serviceName}/${actionName}`
        );
    }

    async getReactionConfig(serviceName, reactionName) {
        return this.request(
            `${API_ENDPOINTS.services}/reactions/${serviceName}/${reactionName}`
        );
    }

    // Areas

    async createArea({
        name,
        user_id,
        action_id,
        reaction_id,
        parameters
    }) {
        const params = new URLSearchParams({
            name,
            user_id,
            action_id,
            reaction_id,
            ...(parameters && {
                parameters: JSON.stringify(parameters)
            })
        });

        const data = await this.request(
            `${API_ENDPOINTS.areas}?${params.toString()}`,
            { method: "POST" }
        );

        return new Area(data);
    }

    async getAreasByUserId(userId) {
        const data = await this.request(
            `${API_ENDPOINTS.areas}?user_id=${encodeURIComponent(userId)}`
        );
        return Array.isArray(data)
            ? data.map(a => new Area(a))
            : [];
    }

    async deleteAreaById(areaId) {
        await this.request(`${API_ENDPOINTS.areas}/${areaId}`, {
            method: "DELETE"
        });
        return API_RESPONSE_CODE.OK;
    }

    // Info/Root

    async getRoot() {
        return this.request(API_ENDPOINTS.root);
    }

    async getInfo() {
        const data = await this.request(API_ENDPOINTS.info);
        return new Info(data);
    }
}

export default ApiClient;
