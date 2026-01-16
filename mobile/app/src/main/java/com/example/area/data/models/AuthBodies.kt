package com.example.area.data.models

data class RegisterBody(
    val username: String,
    val email: String,
    val password: String
)

data class LoginBody(
    val email: String,
    val password: String
)