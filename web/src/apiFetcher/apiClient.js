/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
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
        this.baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";
    }

    async request(endpoint, options = {}) {
        const endpointStr = String(endpoint);

        const url =
            this.baseUrl.replace(/\/+$/, "") +
            ("/") +
            endpointStr.replace(/^\/+/, "");

        const init = {
            method: options.method || "GET",
            headers: {
                ...(this.token ? { "Authorization": `Bearer ${this.token}` } : {}),
                ...(options.headers || {})
            }
        };

        if (options.body !== undefined) {
            if (typeof options.body === "string") {
                init.body = options.body;
                if (!init.headers["Content-Type"])
                    init.headers["Content-Type"] = "application/json";
            } else {
                init.body = JSON.stringify(options.body);
                init.headers["Content-Type"] = init.headers["Content-Type"] || "application/json";
            }
        }

        const res = await fetch(url, init);

        if (!res.ok) {
            let errPayload = null;
            try { errPayload = await res.json(); } catch {}
            const message = (errPayload?.error || errPayload?.message) || `HTTP ${res.status}`;
            const error = new Error(message);
            error.status = res.status;
            error.payload = errPayload;
            throw error;
        }

        return res.json();
    }

    errorHandler = {
        400: () => { console.error("Bad request"); return API_RESPONSE_CODE.BAD_REQUEST; },
        401: () => { console.error("Unauthorized - check your login"); return API_RESPONSE_CODE.UNAUTHORIZED; },
        403: () => { console.error("Forbidden - you don’t have access"); return API_RESPONSE_CODE.FORBIDDEN; },
        404: () => { console.error("Resource not found"); return API_RESPONSE_CODE.NOT_FOUND; },
        429: () => { console.error("Too many requests - rate limited"); return API_RESPONSE_CODE.TOO_MANY_REQUESTS; },
        500: () => { console.error("Internal server error"); return API_RESPONSE_CODE.INTERNAL_SERVER_ERROR; },
        502: () => { console.error("Bad gateway"); return API_RESPONSE_CODE.BAD_GATEWAY; },
    };


    // ! Authentification

    async register(username, email, password) {
        try {
            const data = await this.request(API_ENDPOINTS.register, {
                method: "POST",
                body: { username, email, password }
            });
            return data;
        } catch (error) {
            console.error("Can't register user: ", error);
            throw error;
        }
    }

    async login(email, password) {
        try {
            const data = await this.request(API_ENDPOINTS.login, {
                method: "POST",
                body: { email, password }
            });

            if (data?.token || data?.access_token) {
                this.token = data.token || data.access_token;
            }

            return data;
        } catch (error) {
            console.error("Can't login user: ", error);
            throw error;
        }
    }

    async getGoogleLogin() {
        try {
            const data = await this.request(API_ENDPOINTS.googleLogin);
            return new GoogleLogin(data);
        } catch (error) {
            console.error("Can't get Google login data: ", error);
            throw error;
        }
    }


    // ! Services

    async getServices() {
        try {
            const data = await this.request(API_ENDPOINTS.services);

            if (Array.isArray(data))
                return data.map(item => new Service(item));
            else if (Array.isArray(data?.items))
                return data.items.map(item => new Service(item));
            else
                return [];
        } catch (error) {
            console.error("Can't get services: ", error);
            throw error;
        }
    }

    async getServiceById(id) {
        try {
            const data = await this.request(`${API_ENDPOINTS.services}/${id}`);
            return new Service(data);
        } catch (error) {
            console.error("Can't get service: ", error);
            throw error;
        }
    }

async getServiceActions(id) {
    try {
        const data = await this.request(`${API_ENDPOINTS.services}/${id}/actions`);

        if (Array.isArray(data))
            return data.map(item => new Action(item));
        else if (Array.isArray(data?.items))
            return data.items.map(item => new Action(item));
        else
            return [];
    } catch (error) {
        console.error("Can't get service actions: ", error);
        throw error;
    }
}

async getServiceReactions(id) {
    try {
        const data = await this.request(`${API_ENDPOINTS.services}/${id}/reactions`);

        if (Array.isArray(data))
            return data.map(item => new Reaction(item));
        else if (Array.isArray(data?.items))
            return data.items.map(item => new Reaction(item));
        else
            return [];
    } catch (error) {
        console.error("Can't get service reactions: ", error);
        throw error;
    }
}


    // ! Areas

    async createArea({ name, user_id, action_id, reaction_id }) {
        try {
            const payload = { name, user_id, action_id, reaction_id };
            const data = await this.request(API_ENDPOINTS.areas, {
                method: "POST",
                body: payload
            });
            return new Area(data);
        } catch (error) {
            console.error("Can't create area: ", error);
            throw error;
        }
    }

    async getAreasByUserId(userId) {
        try {
            const data = await this.request(`${API_ENDPOINTS.areas}?user_id=${encodeURIComponent(userId)}`);

            if (Array.isArray(data))
                return data.map(item => new Area(item));
            else if (Array.isArray(data?.items))
                return data.items.map(item => new Area(item));
            else
                return [];
        } catch (error) {
            console.error("Can't get areas: ", error);
            throw error;
        }
    }

    async deleteAreaById(id) {
        try {
            await this.request(`${API_ENDPOINTS.areas}/${id}`, {
                method: "DELETE"
            });
            return API_RESPONSE_CODE.OK;
        } catch (error) {
            console.error("Can't delete area: ", error);
            throw error;
        }
    }


    // ! Info

    async getInfo() {
        try {
            const data = await this.request(API_ENDPOINTS.info);
            return new Info(data);
        } catch (error) {
            console.error("Can't get info: ", error);
            throw error;
        }
    }
}

export default ApiClient;
