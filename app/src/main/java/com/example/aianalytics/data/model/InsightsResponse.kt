package com.example.aianalytics.data.model

import com.google.gson.annotations.SerializedName

/**
 * Model for insights response
 */
data class InsightsResponse(
    @SerializedName("status")
    val status: String? = null,
    
    @SerializedName("data")
    val data: List<Insight>? = null,
    
    @SerializedName("message")
    val message: String? = null,
    
    @SerializedName("timestamp")
    val timestamp: String? = null
) {
    val isSuccessful: Boolean
        get() = status == "success"
    
    val insights: List<Insight>
        get() = data ?: emptyList()
}

