package com.example.aianalytics.models

import com.google.gson.annotations.SerializedName

/**
 * Clean Query Data Model
 * Contains actual query response data from nested "data" object
 */
data class QueryData(
    @SerializedName("answer")
    val answer: String? = null,
    
    @SerializedName("insights")
    val insights: List<String>? = emptyList(),
    
    @SerializedName("steps_executed")
    val stepsExecuted: List<String>? = emptyList(),
    
    @SerializedName("agent_logs")
    val agentLogs: List<String>? = emptyList()
)
