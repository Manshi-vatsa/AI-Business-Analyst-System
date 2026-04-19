package com.aianalyst.chat.repository

import com.aianalyst.chat.models.QueryRequest
import com.aianalyst.chat.models.QueryResponse
import com.aianalyst.chat.network.ApiService
import com.aianalyst.chat.network.RetrofitClient

class ChatRepository {
    
    private val apiService: ApiService = RetrofitClient.apiService
    
    suspend fun sendQuery(question: String): Result<QueryResponse> {
        return try {
            val request = QueryRequest(question)
            val response = apiService.sendQuery(request)
            
            if (response.isSuccessful) {
                response.body()?.let { queryResponse ->
                    Result.success(queryResponse)
                } ?: Result.failure(Exception("Empty response body"))
            } else {
                Result.failure(Exception("API Error: ${response.code()} - ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
