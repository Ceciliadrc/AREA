package com.example.area.data.api

import android.content.Context
import com.example.area.utils.SharedPreferencesManager
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object ApiClient {
    private var retrofit: Retrofit? = null
    private const val DEFAULT_BASE_URL = "http://10.0.2.2:8080"

    // Create API service w dynamic base URL or wtv
    fun getApiService(context: Context): ApiService {
        val sharedPrefs = SharedPreferencesManager(context)
        var baseUrl = sharedPrefs.getServerUrl()

        if (baseUrl.isEmpty()) {
            baseUrl = DEFAULT_BASE_URL
            sharedPrefs.saveServerUrl(baseUrl)
        }

        if (retrofit == null) {
            retrofit = createRetrofit(baseUrl)
        }
        return retrofit!!.create(ApiService::class.java)
    }

    fun updateBaseUrl(context: Context, newUrl: String) {
        val sharedPrefs = SharedPreferencesManager(context)
        sharedPrefs.saveServerUrl(newUrl)

        retrofit = createRetrofit(newUrl)
    }

    fun getCurrentBaseUrl(context: Context): String {
        val sharedPrefs = SharedPreferencesManager(context)
        return sharedPrefs.getServerUrl().ifEmpty { DEFAULT_BASE_URL }
    }

    private fun createRetrofit(baseUrl: String): Retrofit {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }

        val client = OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS) // up timeout if u wanna debug!!
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()

        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .addConverterFactory(GsonConverterFactory.create())
            .client(client)
            .build()
    }
}