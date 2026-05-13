package com.example.aianalytics.data.model

import com.google.gson.annotations.SerializedName

/**
 * Model for health check response
 */
data class HealthResponse(
    @SerializedName("status")
    val status: String? = null,
    
    @SerializedName("message")
    val message: String? = null,
    
    @SerializedName("timestamp")
    val timestamp: String? = null,
    
    @SerializedName("services")
    val services: Map<String, ServiceStatus>? = null,
    
    @SerializedName("version")
    val version: String? = null,
    
    @SerializedName("uptime")
    val uptime: Long? = null
) {
    val isHealthy: Boolean
        get() = status == "healthy" || status == "success"
}

/**
 * Individual service status
 */
data class ServiceStatus(
    @SerializedName("name")
    val name: String? = null,
    
    @SerializedName("status")
    val status: String? = null,
    
    @SerializedName("response_time")
    val responseTime: Long? = null,
    
    @SerializedName("last_check")
    val lastCheck: String? = null
)
