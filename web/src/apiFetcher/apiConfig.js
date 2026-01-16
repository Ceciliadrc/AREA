/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR
** apiConfig.js
*/

export const API_ENDPOINTS = {
    root: `/`,
    info: `/about.json`,

    auth: `/auth`,
    register: `/auth/register`,
    login: `/auth/login`,
    verify: `/auth/verify`,
    me: `/auth/me`,
    myRole: `/auth/me/role`,

    users: `/auth/users`,

    googleLogin: `/auth/google/login`,
    googleCallback: `/auth/google/callback`,
    spotifyLogin: `/auth/spotify/login`,
    spotifyCallback: `/auth/spotify/callback`,
    twitchLogin: `/auth/twitch/login`,
    twitchCallback: `/auth/twitch/callback`,

    areas: `/areas`, // POST, GET
    areaById: (id) => `/areas/${id}`,

    services: `/services`, // GET
    serviceById: (id) => `/services/${id}`,
    serviceActions: (id) => `/services/${id}/actions`,
    serviceReactions: (id) => `/services/${id}/reactions`,

    actionConfig: (service, action) =>
        `/services/actions/${service}/${action}`,
    reactionConfig: (service, reaction) =>
        `/services/reactions/${service}/${reaction}`,
};

export const API_RESPONSE_CODE = {
    OK: 200,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    IM_A_TEAPOT: 418,
    TOO_MANY_REQUESTS: 429,
    INTERNAL_SERVER_ERROR: 500,
    BAD_GATEWAY: 502,
    UNKNOWN_CODE: -1
};
