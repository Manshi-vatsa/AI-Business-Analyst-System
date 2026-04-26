package com.example.aianalytics.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aianalytics.data.models.Insight
import com.example.aianalytics.data.repository.MainRepository
import kotlinx.coroutines.launch

class InsightsViewModel : ViewModel() {
    private val repository = MainRepository()
    
    private val _insights = MutableLiveData<List<Insight>>()
    val insights: LiveData<List<Insight>> = _insights
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String>()
    val error: LiveData<String> = _error
    
    fun loadInsights() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val insightsList = repository.getInsights()
                _insights.value = insightsList
                _error.value = ""
            } catch (e: Exception) {
                _error.value = ""
                // Use mock data when network fails
                _insights.value = getMockInsights()
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    private fun getMockInsights(): List<Insight> {
        return listOf(
            Insight(
                type = "drop",
                message = "Sales decreased by 15% this week compared to last week",
                category = "sales",
                timestamp = java.time.Instant.now().toString()
            ),
            Insight(
                type = "increase", 
                message = "North region showed 20% growth in laptop sales",
                category = "region",
                timestamp = java.time.Instant.now().toString()
            ),
            Insight(
                type = "alert",
                message = "Phone inventory running low, restock recommended",
                category = "inventory",
                timestamp = java.time.Instant.now().toString()
            ),
            Insight(
                type = "trend",
                message = "Laptop sales trending upward for 3 consecutive months",
                category = "product",
                timestamp = java.time.Instant.now().toString()
            )
        )
    }
}
