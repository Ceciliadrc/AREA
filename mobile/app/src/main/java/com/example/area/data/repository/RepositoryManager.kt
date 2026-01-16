package com.example.area.data.repository

import android.content.Context

object RepositoryManager {
    private var authRepository: AuthRepository? = null
    private var serviceRepository: ServiceRepository? = null

    fun getAuthRepository(context: Context): AuthRepository {
        if (authRepository == null) {
            authRepository = AuthRepository(context)
        }
        return authRepository!!
    }

    fun getServiceRepository(context: Context): ServiceRepository {
        if (serviceRepository == null) {
            serviceRepository = ServiceRepository(context)
        }
        return serviceRepository!!
    }

    // Call this when IP changes to clear cached repositories (thank you random asker)
    fun clearRepositories() {
        authRepository = null
        serviceRepository = null
    }
}