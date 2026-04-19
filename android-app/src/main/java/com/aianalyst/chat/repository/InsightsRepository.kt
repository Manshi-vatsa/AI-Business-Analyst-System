package com.aianalyst.chat.repository

import com.aianalyst.chat.models.Insight
import com.aianalyst.chat.network.RetrofitClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.IOException

class InsightsRepository {
    
    private val apiService = RetrofitClient.apiService
    
    suspend fun getInsights(): Result<List<Insight>> {
        return withContext(Dispatchers.IO) {
            try {
                val response = apiService.getInsights()
                if (response.isSuccessful) {
                    response.body()?.let { insights ->
                        Result.success(insights)
                    } ?: Result.failure(IOException("Empty response"))
                } else {
                    Result.failure(IOException("HTTP ${response.code()}: ${response.message()}"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }
}
