package com.example.aianalytics.data.api

import android.content.Context
import android.util.Log
import com.example.aianalytics.utils.NetworkConfig
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitInstance {
    
    private const val TAG = "RetrofitInstance"
    
    // Spring Boot backend URL - Real device on same WiFi
    private const val BASE_URL = "http://192.168.29.53:8080/"
    
    // Alternative: Use localhost for testing
    // private const val BASE_URL = "http://localhost:8080/"
    
    // Logging interceptor for debugging
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }
    
    // OkHttpClient with timeout and logging
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    // Lazy-initialized API service
    val api: ApiService by lazy {
        Log.d(TAG, "Creating Retrofit instance with base URL: $BASE_URL")
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
    
    /**
     * Create API service with custom context (for testing different environments)
     */
    fun createApiService(context: Context): ApiService {
        val baseUrl = NetworkConfig.getBaseUrl(context)
        Log.d(TAG, "Creating API service with base URL: $baseUrl")
        
        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
    
    /**
     * Test connectivity to backend
     */
    fun testConnection(): Boolean {
        return try {
            val request = okhttp3.Request.Builder()
                .url("${BASE_URL}ai/health")
                .build()
            
            val response = okHttpClient.newCall(request).execute()
            val isConnected = response.isSuccessful
            Log.d(TAG, "Connection test result: $isConnected (HTTP ${response.code})")
            isConnected
        } catch (e: Exception) {
            Log.e(TAG, "Connection test failed: ${e.message}", e)
            false
        }
    }
}
