package com.aianalyst.chat.viewModel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aianalyst.chat.models.Insight
import com.aianalyst.chat.repository.InsightsRepository
import kotlinx.coroutines.launch

class InsightsViewModel : ViewModel() {
    
    private val repository = InsightsRepository()
    
    private val _insights = MutableLiveData<List<Insight>>()
    val insights: LiveData<List<Insight>> = _insights
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _errorMessage = MutableLiveData<String?>()
    val errorMessage: LiveData<String?> = _errorMessage
    
    fun loadInsights() {
        _isLoading.value = true
        _errorMessage.value = null
        
        viewModelScope.launch {
            val result = repository.getInsights()
            _isLoading.value = false
            
            result.fold(
                onSuccess = { insightsList ->
                    _insights.value = insightsList
                },
                onFailure = { error ->
                    _errorMessage.value = "Failed to load insights: ${error.message}"
                }
            )
        }
    }
    
    fun clearError() {
        _errorMessage.value = null
    }
}
