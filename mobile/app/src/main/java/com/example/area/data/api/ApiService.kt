package com.example.area.data.api

import com.example.area.data.models.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // AUTH ENDPOINTS
    @POST("auth/register")
    suspend fun register(@Body body: RegisterBody): Response<UserResponse>

    @POST("auth/login")
    suspend fun login(@Body body: LoginBody): Response<UserResponse>

    @GET("auth/google/login")
    suspend fun googleLogin(): Response<Unit>

    @GET("auth/google/callback")
    suspend fun googleCallback(@Query("code") code: String): Response<GoogleAuthResponse>

    @POST("auth/google/token")
    suspend fun googleTokenLogin(@Body body: GoogleIdTokenRequest): Response<UserResponse>


    // SERVICES ENDPOINTS
    @GET("services/")
    suspend fun getAllServices(): Response<ServicesResponse>

    @GET("services/{service_id}")
    suspend fun getService(@Path("service_id") serviceId: Int): Response<Service>

    @GET("services/{service_id}/actions")
    suspend fun getServiceActions(@Path("service_id") serviceId: Int): Response<ServiceActionsResponse>

    @GET("services/{service_id}/reactions")
    suspend fun getServiceReactions(@Path("service_id") serviceId: Int): Response<ServiceReactionsResponse>

    // AREA ENDPOINTS
    @FormUrlEncoded
    @POST("areas/")
    suspend fun createArea(
        @Field("name") name: String,
        @Field("user_id") userId: Int,
        @Field("action_id") actionId: Int,
        @Field("reaction_id") reactionId: Int
    ): Response<UserResponse>

    @GET("areas/")
    suspend fun getUserAreas(@Query("user_id") userId: Int): Response<AreasResponse>

    @DELETE("areas/{area_id}")
    suspend fun deleteArea(@Path("area_id") areaId: Int): Response<UserResponse>

    // MISC ENDPOINTS (WHY SO MUCH ENDPOINTS IM GOING CRAZY)
    @GET("about.json")
    suspend fun getAbout(): Response<AboutResponse>

    @GET("/")
    suspend fun root(): Response<Map<String, String>>
}

// oh those were the last ones actually..