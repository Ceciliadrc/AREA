/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** apiConfig.js
*/

export const API_ENDPOINTS = {
    authentication: `/auth`,
    register: `/auth/register`,
    login: `/auth/login`,
    googleLogin: `/auth/google/login`,
    services: `/services`,
    action: `/action`,
    reaction: `/reaction`,
    areas: `/areas`,
    info: `/about.json`,
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
}