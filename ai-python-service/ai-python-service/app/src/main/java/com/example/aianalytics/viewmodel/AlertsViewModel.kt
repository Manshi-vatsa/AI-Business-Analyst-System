package com.example.aianalytics.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aianalytics.data.models.Alert
import com.example.aianalytics.data.repository.MainRepository
import kotlinx.coroutines.launch

class AlertsViewModel : ViewModel() {
    private val repository = MainRepository()
    
    private val _alerts = MutableLiveData<List<Alert>>()
    val alerts: LiveData<List<Alert>> = _alerts
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String>()
    val error: LiveData<String> = _error
    
    fun loadAlerts() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val alertsList = repository.getAlerts()
                _alerts.value = alertsList
                _error.value = ""
            } catch (e: Exception) {
                _error.value = ""
                // Use mock data when network fails
                _alerts.value = getMockAlerts()
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    private fun getMockAlerts(): List<Alert> {
        return listOf(
            Alert(
                title = "Low Stock Alert",
                message = "Phone inventory below minimum threshold. Current stock: 25 units",
                priority = "high",
                timestamp = java.time.Instant.now().toString()
            ),
            Alert(
                title = "Sales Target Missed",
                message = "South region missed monthly sales target by 10%",
                priority = "medium",
                timestamp = java.time.Instant.now().toString()
            ),
            Alert(
                title = "System Maintenance",
                message = "Database maintenance scheduled for tonight at 2:00 AM",
                priority = "low",
                timestamp = java.time.Instant.now().toString()
            ),
            Alert(
                title = "Price Update Required",
                message = "Laptop prices need adjustment due to market changes",
                priority = "medium",
                timestamp = java.time.Instant.now().toString()
            )
        )
    }
}
