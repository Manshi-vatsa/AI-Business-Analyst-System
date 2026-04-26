package com.example.aianalytics.data.api

import com.example.aianalytics.data.models.*
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    
    /**
     * Send query to Spring Boot backend
     * POST /ai/query
     */
    @POST("ai/query")
    suspend fun sendQuery(@Body request: QueryRequest): Response<QueryResponse>
    
    /**
     * Get dashboard data
     * GET /ai/dashboard
     */
    @GET("ai/dashboard")
    suspend fun getDashboard(): Response<DashboardResponse>
    
    /**
     * Get insights data
     * GET /ai/insights
     */
    @GET("ai/insights")
    suspend fun getInsights(): Response<InsightsResponse>
    
    /**
     * Get alerts data
     * GET /ai/alerts
     */
    @GET("ai/alerts")
    suspend fun getAlerts(): Response<AlertsResponse>
    
    /**
     * Health check endpoint
     * GET /ai/health
     */
    @GET("ai/health")
    suspend fun healthCheck(): Response<HealthResponse>
}
