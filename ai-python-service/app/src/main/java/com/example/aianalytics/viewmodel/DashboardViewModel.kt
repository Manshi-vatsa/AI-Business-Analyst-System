package com.example.aianalytics.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aianalytics.data.models.MonthlySale
import com.example.aianalytics.data.models.DashboardResponse
import com.example.aianalytics.data.repository.MainRepository
import kotlinx.coroutines.launch

class DashboardViewModel : ViewModel() {
    private val repository = MainRepository()
    
    private val _salesData = MutableLiveData<List<MonthlySale>>()
    val salesData: LiveData<List<MonthlySale>> = _salesData
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String>()
    val error: LiveData<String> = _error
    
    fun loadSalesData() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val dashboardResponse = repository.getSales()
                _salesData.value = dashboardResponse.data.monthlySales
                _error.value = ""
            } catch (e: Exception) {
                _error.value = ""
                // Use mock data when network fails
                _salesData.value = getMockSalesData()
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    private fun getMockSalesData(): List<MonthlySale> {
        return listOf(
            MonthlySale(month = "2024-01", revenue = 75000.0),
            MonthlySale(month = "2024-02", revenue = 82000.0),
            MonthlySale(month = "2024-03", revenue = 68000.0),
            MonthlySale(month = "2024-04", revenue = 91000.0),
            MonthlySale(month = "2024-05", revenue = 78000.0),
            MonthlySale(month = "2024-06", revenue = 85000.0)
        )
    }
}
