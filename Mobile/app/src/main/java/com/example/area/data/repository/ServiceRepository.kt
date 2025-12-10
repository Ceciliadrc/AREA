package com.example.area.data.repository

import android.content.Context
import android.util.Log
import com.example.area.data.api.ApiClient
import com.example.area.data.models.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import retrofit2.HttpException
import java.io.IOException

class ServiceRepository(private val context: Context) {
    private val apiService = ApiClient.getApiService(context)
    private val TAG = "ServiceRepository"

    suspend fun getAllServices(): Result<ServicesResponse> {
        return withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "Calling API: /services/")
                val response = apiService.getAllServices()

                if (response.isSuccessful) {
                    val servicesResponse = response.body()!!
                    Log.d(TAG, "TUFFFFF Got ${servicesResponse.services.size} services")
                    Result.success(servicesResponse)
                } else {
                    val errorBody = response.errorBody()?.string() ?: "Unknown error"
                    Log.e(TAG, "Just tough, Failed to get services: ${response.code()} - $errorBody")
                    Result.failure(Exception("Failed to get services: ${response.code()}"))
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

    suspend fun getServiceActions(serviceId: Int): Result<ServiceActionsResponse> {
        return withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "Calling API: /services/$serviceId/actions")
                val response = apiService.getServiceActions(serviceId)

                if (response.isSuccessful) {
                    val actionsResponse = response.body()!!
                    Log.d(TAG, "Got ${actionsResponse.actions.size} actions for service $serviceId")
                    Result.success(actionsResponse)
                } else {
                    val errorBody = response.errorBody()?.string() ?: "Unknown error"
                    Log.e(TAG, "Failed to get actions: ${response.code()} - $errorBody")
                    Result.failure(Exception("Failed to get actions: ${response.code()}"))
                }
            } catch (e: Exception) {
                Log.e(TAG, "Error getting actions: ${e.message}")
                Result.failure(e)
            }
        }
    }

    suspend fun getServiceReactions(serviceId: Int): Result<ServiceReactionsResponse> {
        return withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "Calling API: /services/$serviceId/reactions")
                val response = apiService.getServiceReactions(serviceId)

                if (response.isSuccessful) {
                    val reactionsResponse = response.body()!!
                    Log.d(TAG, "Got ${reactionsResponse.reactions.size} reactions for service $serviceId")
                    Result.success(reactionsResponse)
                } else {
                    val errorBody = response.errorBody()?.string() ?: "Unknown error"
                    Log.e(TAG, "Failed to get reactions: ${response.code()} - $errorBody")
                    Result.failure(Exception("Failed to get reactions: ${response.code()}"))
                }
            } catch (e: Exception) {
                Log.e(TAG, "Error getting reactions: ${e.message}")
                Result.failure(e)
            }
        }
    }

    suspend fun testConnection(): Result<AboutResponse> {
        return withContext(Dispatchers.IO) {
            try {
                Log.d(TAG, "Testing connection with /about.json")
                val response = apiService.getAbout()

                if (response.isSuccessful) {
                    val aboutResponse = response.body()!!
                    Log.d(TAG, "Connection successful!!! Server has ${aboutResponse.server.services.size} services")
                    Result.success(aboutResponse)
                } else {
                    Log.e(TAG, "Connection test failed: ${response.code()}")
                    Result.failure(Exception("Connection failed: ${response.code()}"))
                }
            } catch (e: IOException) {
                Log.e(TAG, "Network error during connection test: ${e.message}")
                Result.failure(Exception("Network error: ${e.message}"))
            } catch (e: Exception) {
                Log.e(TAG, "Error during connection test: ${e.message}")
                Result.failure(e)
            }
        }
    }
}