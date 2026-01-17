package com.example.area.data.models

data class User(
    val id: Int? = null,
    val username: String,
    val email: String,
    val password: String? = null
)

data class UserResponse(
    val message: String? = null,
    val userId: Int? = null,
    val username: String? = null,
    val error: String? = null
)

data class GoogleAuthResponse(
    val message: String,
    val googleUser: Map<String, Any>? = null,
    val tokens: Map<String, Any>? = null
)

data class GoogleIdTokenRequest(
    val id_token: String
)

data class ApiError(
    val error: String? = null,
    val message: String? = null
)