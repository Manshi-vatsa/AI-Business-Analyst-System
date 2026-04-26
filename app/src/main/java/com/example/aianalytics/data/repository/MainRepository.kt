package com.example.aianalytics.data.repository

import android.util.Log
import com.example.aianalytics.data.api.RetrofitInstance
import com.example.aianalytics.data.models.*

class MainRepository {
    private val apiService = RetrofitInstance.api
    private val TAG = "MainRepository"
    
    suspend fun sendQuery(question: String): QueryResponse {
        Log.d(TAG, "=== MAIN REPOSITORY SEND QUERY ===")
        Log.d(TAG, "Question: $question")
        
        try {
            val request = QueryRequest(question)
            val response = apiService.sendQuery(request)
            
            Log.d(TAG, "API Response Code: ${response.code()}")
            Log.d(TAG, "API Response Successful: ${response.isSuccessful()}")
            Log.d(TAG, "API Response Body: ${response.body()}")
            
            if (response.isSuccessful && response.body() != null) {
                val queryResponse = response.body()!!
                Log.d(TAG, "✅ Query successful: ${queryResponse.message}")
                Log.d(TAG, "Answer: ${queryResponse.data.answer}")
                Log.d(TAG, "Insights count: ${queryResponse.data.insights.size}")
                return queryResponse
            } else {
                val errorBody = response.errorBody()?.string()
                Log.e(TAG, "❌ Query failed: HTTP ${response.code()} - $errorBody")
                throw Exception("API Error: ${response.code()} - ${response.message()}")
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ Query exception: ${e.message}", e)
            throw e
        }
    }
    
    suspend fun getSales(): DashboardResponse {
        val response = apiService.getDashboard()
        return response.body() ?: throw Exception("Dashboard response is null")
    }
    
    suspend fun getInsights(): List<Insight> {
        val response = apiService.getInsights()
        return response.body()?.data ?: throw Exception("Insights response is null")
    }
    
    suspend fun getAlerts(): List<Alert> {
        val response = apiService.getAlerts()
        return response.body()?.data ?: throw Exception("Alerts response is null")
    }
}
