package com.example.aianalytics.utils

import android.util.Log
import retrofit2.Response
import com.google.gson.Gson
import com.google.gson.JsonSyntaxException

/**
 * Network logging utility for debugging API responses
 */
object NetworkLogger {
    
    private const val TAG = "AIAnalytics_Network"
    private val gson = Gson()
    
    /**
     * Log API request details
     */
    fun logRequest(endpoint: String, method: String, body: Any? = null) {
        Log.d(TAG, "=== API REQUEST ===")
        Log.d(TAG, "Endpoint: $endpoint")
        Log.d(TAG, "Method: $method")
        if (body != null) {
            Log.d(TAG, "Body: ${gson.toJson(body)}")
        }
        Log.d(TAG, "==================")
    }
    
    /**
     * Log API response details
     */
    fun <T> logResponse(endpoint: String, response: Response<T>) {
        Log.d(TAG, "=== API RESPONSE ===")
        Log.d(TAG, "Endpoint: $endpoint")
        Log.d(TAG, "Status: ${response.code()} ${response.message()}")
        Log.d(TAG, "Success: ${response.isSuccessful()}")
        
        // Log headers
        Log.d(TAG, "Headers:")
        response.headers().names().forEach { name ->
            Log.d(TAG, "  $name: ${response.headers().get(name)}")
        }
        
        // Log body
        response.body()?.let { body ->
            try {
                val jsonBody = gson.toJson(body)
                Log.d(TAG, "Body: $jsonBody")
                
                // Validate JSON structure
                validateJsonStructure(jsonBody, endpoint)
                
            } catch (e: JsonSyntaxException) {
                Log.e(TAG, "JSON parsing error: ${e.message}")
                Log.d(TAG, "Raw body: $body")
            }
        } ?: Log.d(TAG, "Body: null")
        
        Log.d(TAG, "===================")
    }
    
    /**
     * Log API error details
     */
    fun logError(endpoint: String, errorCode: Int, errorMessage: String, errorBody: String? = null) {
        Log.e(TAG, "=== API ERROR ===")
        Log.e(TAG, "Endpoint: $endpoint")
        Log.e(TAG, "Error Code: $errorCode")
        Log.e(TAG, "Error Message: $errorMessage")
        if (errorBody != null) {
            Log.e(TAG, "Error Body: $errorBody")
        }
        Log.e(TAG, "================")
    }
    
    /**
     * Validate JSON structure for different endpoints
     */
    private fun validateJsonStructure(jsonBody: String, endpoint: String) {
        try {
            when {
                endpoint.contains("/dashboard") -> validateDashboardJson(jsonBody)
                endpoint.contains("/query") -> validateQueryJson(jsonBody)
                endpoint.contains("/insights") -> validateInsightsJson(jsonBody)
                endpoint.contains("/alerts") -> validateAlertsJson(jsonBody)
                else -> Log.d(TAG, "No specific validation for endpoint: $endpoint")
            }
        } catch (e: Exception) {
            Log.e(TAG, "JSON validation error: ${e.message}")
        }
    }
    
    /**
     * Validate dashboard JSON structure
     */
    private fun validateDashboardJson(jsonBody: String) {
        Log.d(TAG, "Validating dashboard JSON structure...")
        
        // Parse JSON and check required fields
        val jsonElement = gson.fromJson(jsonBody, com.google.gson.JsonElement::class.java)
        val jsonObject = jsonElement.asJsonObject
        
        // Check top-level fields
        val requiredFields = listOf("status", "data", "message")
        requiredFields.forEach { field ->
            if (!jsonObject.has(field)) {
                Log.w(TAG, "Missing required field in dashboard response: $field")
            } else {
                Log.d(TAG, "✓ Found field: $field")
            }
        }
        
        // Check data structure
        if (jsonObject.has("data")) {
            val dataObject = jsonObject.getAsJsonObject("data")
            val dataFields = listOf("monthlySales", "regionSales", "productSales")
            dataFields.forEach { field ->
                if (dataObject.has(field)) {
                    val salesArray = dataObject.getAsJsonArray(field)
                    Log.d(TAG, "✓ Found $field with ${salesArray.size()} items")
                } else {
                    Log.w(TAG, "Missing data field: $field")
                }
            }
        }
    }
    
    /**
     * Validate query JSON structure
     */
    private fun validateQueryJson(jsonBody: String) {
        Log.d(TAG, "Validating query JSON structure...")
        
        val jsonElement = gson.fromJson(jsonBody, com.google.gson.JsonElement::class.java)
        val jsonObject = jsonElement.asJsonObject
        
        val requiredFields = listOf("status", "data", "message")
        requiredFields.forEach { field ->
            if (!jsonObject.has(field)) {
                Log.w(TAG, "Missing required field in query response: $field")
            } else {
                Log.d(TAG, "✓ Found field: $field")
            }
        }
        
        if (jsonObject.has("data")) {
            val dataObject = jsonObject.getAsJsonObject("data")
            val dataFields = listOf("answer", "insights")
            dataFields.forEach { field ->
                if (dataObject.has(field)) {
                    Log.d(TAG, "✓ Found $field")
                } else {
                    Log.w(TAG, "Missing data field: $field")
                }
            }
        }
    }
    
    /**
     * Validate insights JSON structure
     */
    private fun validateInsightsJson(jsonBody: String) {
        Log.d(TAG, "Validating insights JSON structure...")
        
        val jsonElement = gson.fromJson(jsonBody, com.google.gson.JsonElement::class.java)
        val jsonObject = jsonElement.asJsonObject
        
        val requiredFields = listOf("status", "data", "message")
        requiredFields.forEach { field ->
            if (!jsonObject.has(field)) {
                Log.w(TAG, "Missing required field in insights response: $field")
            } else {
                Log.d(TAG, "✓ Found field: $field")
            }
        }
    }
    
    /**
     * Validate alerts JSON structure
     */
    private fun validateAlertsJson(jsonBody: String) {
        Log.d(TAG, "Validating alerts JSON structure...")
        
        val jsonElement = gson.fromJson(jsonBody, com.google.gson.JsonElement::class.java)
        val jsonObject = jsonElement.asJsonObject
        
        val requiredFields = listOf("status", "data", "message")
        requiredFields.forEach { field ->
            if (!jsonObject.has(field)) {
                Log.w(TAG, "Missing required field in alerts response: $field")
            } else {
                Log.d(TAG, "✓ Found field: $field")
            }
        }
    }
    
    /**
     * Log network connectivity status
     */
    fun logConnectivity(isConnected: Boolean, networkType: String) {
        Log.d(TAG, "=== NETWORK STATUS ===")
        Log.d(TAG, "Connected: $isConnected")
        Log.d(TAG, "Network Type: $networkType")
        Log.d(TAG, "==================")
    }
    
    /**
     * Log API call timing
     */
    fun logTiming(endpoint: String, startTime: Long, endTime: Long) {
        val duration = endTime - startTime
        Log.d(TAG, "=== API TIMING ===")
        Log.d(TAG, "Endpoint: $endpoint")
        Log.d(TAG, "Duration: ${duration}ms")
        Log.d(TAG, "=================")
    }
}
