package com.example.aianalytics.data.repository

import android.util.Log
import com.example.aianalytics.data.api.ApiService
import com.example.aianalytics.data.models.*
import com.example.aianalytics.utils.NetworkLogger
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.IOException
import java.net.SocketTimeoutException
import java.net.UnknownHostException

/**
 * Repository for API calls with proper error handling and logging
 */
class ApiRepository(private val apiService: ApiService) {
    
    private val TAG = "ApiRepository"
    
    /**
     * Send query to backend
     */
    suspend fun sendQuery(question: String): Result<QueryResponse> {
        return try {
            Log.d(TAG, "=== SENDING QUERY ===")
            Log.d(TAG, "Question: $question")
            
            val request = QueryRequest(question)
            NetworkLogger.logRequest("/ai/query", "POST", request)
            
            val startTime = System.currentTimeMillis()
            val response = apiService.sendQuery(request)
            val endTime = System.currentTimeMillis()
            
            NetworkLogger.logTiming("/ai/query", startTime, endTime)
            NetworkLogger.logResponse("/ai/query", response)
            
            if (response.isSuccessful) {
                response.body()?.let { queryResponse ->
                    Log.d(TAG, "✅ Query successful: ${queryResponse.message}")
                    Log.d(TAG, "Answer: ${queryResponse.data.answer}")
                    Log.d(TAG, "Insights count: ${queryResponse.data.insights.size}")
                    Result.success(queryResponse)
                } ?: run {
                    Log.e(TAG, "❌ Query response body is null")
                    Result.failure(Exception("Response body is null"))
                }
            } else {
                val errorBody = response.errorBody()?.string()
                Log.e(TAG, "❌ Query failed: HTTP ${response.code()} - $errorBody")
                NetworkLogger.logError("/ai/query", response.code(), response.message(), errorBody)
                Result.failure(Exception("API Error: ${response.code()} - ${response.message()}"))
            }
        } catch (e: UnknownHostException) {
            Log.e(TAG, "❌ Network error: Unknown host - ${e.message}", e)
            NetworkLogger.logError("/ai/query", 0, "Unknown host", e.message)
            Result.failure(Exception("Network error: Unable to connect to server. Please check your internet connection and ensure the backend is running."))
        } catch (e: SocketTimeoutException) {
            Log.e(TAG, "❌ Network error: Timeout - ${e.message}", e)
            NetworkLogger.logError("/ai/query", 0, "Timeout", e.message)
            Result.failure(Exception("Request timeout. Please try again."))
        } catch (e: IOException) {
            Log.e(TAG, "❌ Network error: IO Exception - ${e.message}", e)
            NetworkLogger.logError("/ai/query", 0, "IO Exception", e.message)
            Result.failure(Exception("Network error: ${e.message}"))
        } catch (e: Exception) {
            Log.e(TAG, "❌ Unexpected error: ${e.message}", e)
            NetworkLogger.logError("/ai/query", 0, "Unexpected error", e.message)
            Result.failure(Exception("Unexpected error: ${e.message}"))
        }
    }
    
    /**
     * Get dashboard data
     */
    suspend fun getDashboard(): Result<DashboardResponse> {
        return try {
            Log.d(TAG, "=== GETTING DASHBOARD ===")
            
            val startTime = System.currentTimeMillis()
            val response = apiService.getDashboard()
            val endTime = System.currentTimeMillis()
            
            NetworkLogger.logTiming("/ai/dashboard", startTime, endTime)
            NetworkLogger.logResponse("/ai/dashboard", response)
            
            if (response.isSuccessful) {
                response.body()?.let { dashboardResponse ->
                    Log.d(TAG, "✅ Dashboard successful: ${dashboardResponse.message}")
                    Log.d(TAG, "Monthly sales: ${dashboardResponse.data.monthlySales.size}")
                    Log.d(TAG, "Region sales: ${dashboardResponse.data.regionSales.size}")
                    Log.d(TAG, "Product sales: ${dashboardResponse.data.productSales.size}")
                    Result.success(dashboardResponse)
                } ?: run {
                    Log.e(TAG, "❌ Dashboard response body is null")
                    Result.failure(Exception("Response body is null"))
                }
            } else {
                val errorBody = response.errorBody()?.string()
                Log.e(TAG, "❌ Dashboard failed: HTTP ${response.code()} - $errorBody")
                NetworkLogger.logError("/ai/dashboard", response.code(), response.message(), errorBody)
                Result.failure(Exception("API Error: ${response.code()} - ${response.message()}"))
            }
        } catch (e: UnknownHostException) {
            Log.e(TAG, "❌ Dashboard network error: Unknown host - ${e.message}", e)
            Result.failure(Exception("Network error: Unable to connect to server. Please check your internet connection and ensure the backend is running."))
        } catch (e: SocketTimeoutException) {
            Log.e(TAG, "❌ Dashboard timeout error - ${e.message}", e)
            Result.failure(Exception("Request timeout. Please try again."))
        } catch (e: IOException) {
            Log.e(TAG, "❌ Dashboard IO error - ${e.message}", e)
            Result.failure(Exception("Network error: ${e.message}"))
        } catch (e: Exception) {
            Log.e(TAG, "❌ Dashboard unexpected error - ${e.message}", e)
            Result.failure(Exception("Unexpected error: ${e.message}"))
        }
    }
    
    /**
     * Get insights data
     */
    suspend fun getInsights(): Result<InsightsResponse> {
        return try {
            Log.d(TAG, "=== GETTING INSIGHTS ===")
            
            val response = apiService.getInsights()
            NetworkLogger.logResponse("/ai/insights", response)
            
            if (response.isSuccessful) {
                response.body()?.let { insightsResponse ->
                    Log.d(TAG, "✅ Insights successful: ${insightsResponse.message}")
                    Log.d(TAG, "Insights count: ${insightsResponse.data.size}")
                    Result.success(insightsResponse)
                } ?: run {
                    Log.e(TAG, "❌ Insights response body is null")
                    Result.failure(Exception("Response body is null"))
                }
            } else {
                val errorBody = response.errorBody()?.string()
                Log.e(TAG, "❌ Insights failed: HTTP ${response.code()} - $errorBody")
                Result.failure(Exception("API Error: ${response.code()} - ${response.message()}"))
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ Insights error: ${e.message}", e)
            Result.failure(Exception("Error fetching insights: ${e.message}"))
        }
    }
    
    /**
     * Get alerts data
     */
    suspend fun getAlerts(): Result<AlertsResponse> {
        return try {
            Log.d(TAG, "=== GETTING ALERTS ===")
            
            val response = apiService.getAlerts()
            NetworkLogger.logResponse("/ai/alerts", response)
            
            if (response.isSuccessful) {
                response.body()?.let { alertsResponse ->
                    Log.d(TAG, "✅ Alerts successful: ${alertsResponse.message}")
                    Log.d(TAG, "Alerts count: ${alertsResponse.data.size}")
                    Result.success(alertsResponse)
                } ?: run {
                    Log.e(TAG, "❌ Alerts response body is null")
                    Result.failure(Exception("Response body is null"))
                }
            } else {
                val errorBody = response.errorBody()?.string()
                Log.e(TAG, "❌ Alerts failed: HTTP ${response.code()} - $errorBody")
                Result.failure(Exception("API Error: ${response.code()} - ${response.message()}"))
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ Alerts error: ${e.message}", e)
            Result.failure(Exception("Error fetching alerts: ${e.message}"))
        }
    }
    
    /**
     * Health check
     */
    suspend fun healthCheck(): Result<HealthResponse> {
        return try {
            Log.d(TAG, "=== HEALTH CHECK ===")
            
            val response = apiService.healthCheck()
            NetworkLogger.logResponse("/ai/health", response)
            
            if (response.isSuccessful) {
                response.body()?.let { healthResponse ->
                    Log.d(TAG, "✅ Health check successful: ${healthResponse.message}")
                    Log.d(TAG, "Service status: ${healthResponse.status}")
                    Result.success(healthResponse)
                } ?: run {
                    Log.e(TAG, "❌ Health check response body is null")
                    Result.failure(Exception("Response body is null"))
                }
            } else {
                val errorBody = response.errorBody()?.string()
                Log.e(TAG, "❌ Health check failed: HTTP ${response.code()} - $errorBody")
                Result.failure(Exception("Health check failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ Health check error: ${e.message}", e)
            Result.failure(Exception("Health check error: ${e.message}"))
        }
    }
    
    /**
     * Test connectivity with detailed logging
     */
    suspend fun testConnectivity(): Boolean {
        return try {
            Log.d(TAG, "=== CONNECTIVITY TEST ===")
            
            val result = healthCheck()
            when {
                result.isSuccess -> {
                    Log.d(TAG, "✅ Connectivity test PASSED")
                    true
                }
                result.isFailure -> {
                    Log.e(TAG, "❌ Connectivity test FAILED: ${result.exceptionOrNull()?.message}")
                    false
                }
                else -> {
                    Log.w(TAG, "⚠️ Connectivity test INCONCLUSIVE")
                    false
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ Connectivity test exception: ${e.message}", e)
            false
        }
    }
}
