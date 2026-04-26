package com.example.aianalytics.data.model

data class QueryResponse(
    val answer: String,
    val insights: List<String>
)

// Wrapper to match Python service response format
data class ApiResponse<T>(
    val status: String,
    val data: T,
    val message: String,
    val timestamp: String
)

// Query response wrapper
data class QueryApiResponse(
    val status: String,
    val data: QueryResponse,
    val message: String,
    val timestamp: String
)

// Dashboard response wrapper
data class DashboardApiResponse(
    val status: String,
    val data: DashboardResponse,
    val message: String,
    val timestamp: String
)

// Insights response wrapper
data class InsightsApiResponse(
    val status: String,
    val data: List<Insight>,
    val message: String,
    val timestamp: String
)

// Alerts response wrapper
data class AlertsApiResponse(
    val status: String,
    val data: List<Alert>,
    val message: String,
    val timestamp: String
)
