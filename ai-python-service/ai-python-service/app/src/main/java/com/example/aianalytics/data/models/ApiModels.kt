package com.example.aianalytics.data.models

import com.google.gson.annotations.SerializedName

/**
 * API Request and Response Models for Spring Boot Integration
 */

// Query Request Model
data class QueryRequest(
    @SerializedName("question")
    val question: String
)

// Query Response Model
data class QueryResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("data")
    val data: QueryData,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("timestamp")
    val timestamp: String
)

data class QueryData(
    @SerializedName("answer")
    val answer: String,
    
    @SerializedName("insights")
    val insights: List<String>,
    
    @SerializedName("sql_query")
    val sqlQuery: String? = null,
    
    @SerializedName("results")
    val results: List<SalesRecord>? = null
)

data class SalesRecord(
    @SerializedName("id")
    val id: Int,
    
    @SerializedName("product")
    val product: String,
    
    @SerializedName("quantity")
    val quantity: Int,
    
    @SerializedName("revenue")
    val revenue: Double,
    
    @SerializedName("date")
    val date: String,
    
    @SerializedName("region")
    val region: String
)

// Dashboard Response Model
data class DashboardResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("data")
    val data: DashboardData,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("timestamp")
    val timestamp: String
)

data class DashboardData(
    @SerializedName("monthlySales")
    val monthlySales: List<MonthlySale>,
    
    @SerializedName("regionSales")
    val regionSales: List<RegionSale>,
    
    @SerializedName("productSales")
    val productSales: List<ProductSale>
)

data class MonthlySale(
    @SerializedName("month")
    val month: String,
    
    @SerializedName("revenue")
    val revenue: Double
)

data class RegionSale(
    @SerializedName("region")
    val region: String,
    
    @SerializedName("revenue")
    val revenue: Double,
    
    @SerializedName("percentage")
    val percentage: Double? = null
)

data class ProductSale(
    @SerializedName("product")
    val product: String,
    
    @SerializedName("revenue")
    val revenue: Double,
    
    @SerializedName("quantity")
    val quantity: Int
)

// Insights Response Model
data class InsightsResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("data")
    val data: List<Insight>,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("timestamp")
    val timestamp: String
)

data class Insight(
    @SerializedName("type")
    val type: String,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("value")
    val value: Double? = null,
    
    @SerializedName("category")
    val category: String,
    
    @SerializedName("timestamp")
    val timestamp: String
)

// Alerts Response Model
data class AlertsResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("data")
    val data: List<Alert>,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("timestamp")
    val timestamp: String
)

data class Alert(
    @SerializedName("title")
    val title: String,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("priority")
    val priority: String,
    
    @SerializedName("timestamp")
    val timestamp: String
)

// Health Response Model
data class HealthResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("service")
    val service: String,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("timestamp")
    val timestamp: String,
    
    @SerializedName("version")
    val version: String? = null,
    
    @SerializedName("database")
    val database: String? = null,
    
    @SerializedName("memory_usage")
    val memoryUsage: String? = null,
    
    @SerializedName("cpu_usage")
    val cpuUsage: String? = null
)

// Error Response Model
data class ErrorResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("error")
    val error: String,
    
    @SerializedName("details")
    val details: String? = null,
    
    @SerializedName("timestamp")
    val timestamp: String
)

// Generic API Response Wrapper
data class ApiResponse<T>(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("data")
    val data: T? = null,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("timestamp")
    val timestamp: String
)
