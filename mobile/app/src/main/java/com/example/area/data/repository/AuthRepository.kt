package com.example.area.data.repository

import android.content.Context
import android.util.Log
import com.example.area.data.api.ApiClient
import com.example.area.data.models.UserResponse
import com.example.area.utils.SharedPreferencesManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import retrofit2.HttpException
import java.io.IOException

class AuthRepository(private val context: Context) {
    private val apiService = ApiClient.getApiService(context)
    private val sharedPrefs = SharedPreferencesManager(context)
    private val TAG = "AuthRepository"

    suspend fun testConnection(): Boolean {
        return withContext(Dispatchers.IO) {
            try {
                val response = apiService.getAbout()
                response.isSuccessful
            } catch (e: Exception) {
                Log.e(TAG, "Connection test failed: ${e.message}")
                false
            }
        }
    }

    suspend fun register(username: String, email: String, password: String): Result<UserResponse> {
        return withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "Calling API: /auth/register")
                Log.d(TAG, "Data: username=$username, email=$email")

                val response = apiService.register(username, email, password)

                if (response.isSuccessful) {
                    val userResponse = response.body()!!
                    Log.d(TAG, "API Response: $userResponse")

                    if (userResponse.error != null) {
                        Log.e(TAG, "API returned error: ${userResponse.error}")
                        Result.failure(Exception(userResponse.error))
                    } else {
                        userResponse.userId?.let { user_id ->
                            sharedPrefs.saveUserId(user_id)
                            sharedPrefs.saveUserEmail(email)
                            sharedPrefs.saveUsername(username)
                            Log.d(TAG, "Saved user ID: $user_id")
                        }
                        Log.d(TAG, "Registration successful!!!!!!")
                        Result.success(userResponse)
                    }
                } else {
                    val errorBody = response.errorBody()?.string() ?: "Unknown error"
                    Log.e(TAG, "Regsistratiin failed: ${response.code()} - $errorBody")
                    Result.failure(Exception("Registration failed: ${response.code()}"))
                }

            } catch (e: IOException) {
                Log.e(TAG, "Network error: ${e.message}")
                Result.failure(Exception("Network error: ${e.message}"))
            } catch (e: HttpException) {
                Log.e(TAG, "HTTP error: ${e.message}")
                Result.failure(Exception("Server error: ${e.message}"))
            } catch (e: Exception) {
                Log.e(TAG, "Unexpected error: ${e.message}")
                Result.failure(e)
            }
        }
    }

    suspend fun login(email: String, password: String): Result<UserResponse> {
        return withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "Calling API: /auth/login")
                Log.d(TAG, "Data: email=$email")

                val response = apiService.login(email, password)

                if (response.isSuccessful) {
                    val userResponse = response.body()!!
                    Log.d(TAG, "API Response: $userResponse")

                    if (userResponse.error != null) {
                        Log.e(TAG, "API returned error: ${userResponse.error}")
                        Result.failure(Exception(userResponse.error))
                    } else {
                        userResponse.userId?.let { user_id ->
                            sharedPrefs.saveUserId(user_id)
                            sharedPrefs.saveUserEmail(email)
                            userResponse.username?.let { username ->
                                sharedPrefs.saveUsername(username)
                            }
                            Log.d(TAG, "Saved user ID: $user_id")
                        }

                        Log.d(TAG, "Login successful!!! (ça mérite encore lus d'exclamation, il est tard/tôt rn)")
                        Result.success(userResponse)
                    }
                } else {
                    val errorBody = response.errorBody()?.string() ?: "Unknown error"
                    Log.e(TAG, "Login failed RAHHHHH: ${response.code()} - $errorBody")
                    Result.failure(Exception("Login failed: ${response.code()}"))
                }
            } catch (e: IOException) {
                Log.e(TAG, "📡 Network error je vé péter un cablos: ${e.message}")
                Result.failure(Exception("Network error: ${e.message}"))
            } catch (e: HttpException) {
                Log.e(TAG, "HTTP error: ${e.message}")
                Result.failure(Exception("Server error: ${e.message}"))
            } catch (e: Exception) {
                Log.e(TAG, "Unexpected error: ${e.message}")
                Result.failure(e)
            }
        }
    }

    fun logout() {
        Log.d(TAG, "Logging out user")
        sharedPrefs.clearUserData()
    }

    fun isUserLoggedIn(): Boolean {
        return sharedPrefs.isLoggedIn()
    }

    fun getCurrentUserId(): Int {
        return sharedPrefs.getUserId()
    }

    fun getCurrentUsername(): String {
        return sharedPrefs.getUsername()
    }
}