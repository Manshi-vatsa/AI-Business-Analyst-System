package com.aianalyst.chat.network

import com.aianalyst.chat.models.QueryRequest
import com.aianalyst.chat.models.QueryResponse
import com.aianalyst.chat.models.Insight
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    
    @POST("api/query")
    suspend fun sendQuery(@Body request: QueryRequest): Response<QueryResponse>
    
    @GET("ai/insights")
    suspend fun getInsights(): Response<List<Insight>>
}
