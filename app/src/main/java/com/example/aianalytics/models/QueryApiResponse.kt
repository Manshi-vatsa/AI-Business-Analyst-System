package com.example.aianalytics.models

import com.google.gson.annotations.SerializedName

/**
 * Clean Query API Response Model
 * Matches backend JSON structure exactly:
 * {
 *   "status": "success",
 *   "data": { "answer": "...", "insights": [...] },
 *   "message": "..."
 * }
 */
data class QueryApiResponse(
    @SerializedName("status")
    val status: String? = null,
    
    @SerializedName("data")
    val data: QueryData? = null,
    
    @SerializedName("message")
    val message: String? = null
) {
    val isSuccessful: Boolean
        get() = status == "success"
    
    val answer: String
        get() = data?.answer ?: "No answer available"
    
    val insights: List<String>
        get() = data?.insights ?: emptyList()
}
