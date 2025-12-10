package com.example.area.utils

import android.content.Context
import android.content.SharedPreferences

class SharedPreferencesManager(context: Context) {
    private val sharedPreferences: SharedPreferences =
        context.getSharedPreferences("AREA_APP_PREFS", Context.MODE_PRIVATE)

    fun saveServerUrl(url: String) {
        sharedPreferences.edit().putString("server_url", url).apply()
    }

    fun getServerUrl(): String {
        return sharedPreferences.getString("server_url", "") ?: ""
    }

    fun saveUserId(userId: Int) {
        sharedPreferences.edit().putInt("user_id", userId).apply()
    }

    fun getUserId(): Int {
        return sharedPreferences.getInt("user_id", -1)
    }

    fun saveUserEmail(email: String) {
        sharedPreferences.edit().putString("user_email", email).apply()
    }

    fun getUserEmail(): String {
        return sharedPreferences.getString("user_email", "") ?: ""
    }

    fun saveUsername(username: String) {
        sharedPreferences.edit().putString("username", username).apply()
    }

    fun getUsername(): String {
        return sharedPreferences.getString("username", "") ?: ""
    }

    fun clearUserData() {
        sharedPreferences.edit().clear().apply()
    }

    fun isLoggedIn(): Boolean {
        return getUserId() != -1
    }
}