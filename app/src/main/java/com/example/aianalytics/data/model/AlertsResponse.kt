package com.example.aianalytics.data.model

import com.google.gson.annotations.SerializedName

/**
 * Model for alerts response
 */
data class AlertsResponse(
    @SerializedName("status")
    val status: String? = null,
    
    @SerializedName("data")
    val data: List<Alert>? = null,
    
    @SerializedName("message")
    val message: String? = null,
    
    @SerializedName("timestamp")
    val timestamp: String? = null
) {
    val isSuccessful: Boolean
        get() = status == "success"
    
    val alerts: List<Alert>
        get() = data ?: emptyList()
}

