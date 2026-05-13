package com.example.aianalytics.viewmodel

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aianalytics.data.models.ChatMessage
import com.example.aianalytics.data.models.QueryResponse
import com.example.aianalytics.data.repository.MainRepository
import kotlinx.coroutines.launch

class ChatViewModel : ViewModel() {
    private val repository = MainRepository()
    
    // 🔥 STEP 2: FIX LiveData DECLARATION
    private val _messages = MutableLiveData<List<ChatMessage>>(emptyList())
    val messages: LiveData<List<ChatMessage>> = _messages
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String>()
    val error: LiveData<String> = _error
    
    // 🔥 STEP 1: FIX ChatViewModel (CRITICAL)
    fun sendMessage(message: String) {
        Log.d("CHAT_DEBUG", "Before API call - User message: $message")
        
        // Add USER message immediately
        val currentList = _messages.value ?: emptyList()
        _messages.value = currentList + ChatMessage(message, true)
        
        viewModelScope.launch {
            _isLoading.value = true
            try {
                Log.d("CHAT_DEBUG", "After API call - Starting repository call")
                val response = repository.sendQuery(message)
                
                if (response != null) {
                    Log.d("CHAT_DEBUG", "FULL RESPONSE: $response")
                    Log.d("CHAT_DEBUG", "RESPONSE STATUS: ${response.status}")
                    Log.d("CHAT_DEBUG", "RESPONSE MESSAGE: ${response.message}")
                    Log.d("CHAT_DEBUG", "RESPONSE DATA: ${response.data}")
                    
                    val answer = response.data.answer ?: "No answer from AI"
                    Log.d("CHAT_DEBUG", "ANSWER: $answer")
                    Log.d("CHAT_DEBUG", "INSIGHTS COUNT: ${response.data.insights.size}")
                    Log.d("CHAT_DEBUG", "INSIGHTS: ${response.data.insights}")
                    
                    // 🔥 STEP 7: VERIFY UI THREAD ISSUE - use postValue inside coroutine
                    val updatedList = (_messages.value ?: emptyList()) + ChatMessage(answer, false)
                    _messages.postValue(updatedList)
                    
                    _error.value = ""
                } else {
                    Log.e("CHAT_DEBUG", "API FAILED - Response is null")
                    
                    val errorList = (_messages.value ?: emptyList()) + ChatMessage(
                        "Error: Unable to get response",
                        false
                    )
                    _messages.postValue(errorList)
                    _error.value = "Unable to get response"
                }
                
            } catch (e: Exception) {
                Log.e("CHAT_DEBUG", "API FAILED - Exception: ${e.message}", e)
                
                val errorList = (_messages.value ?: emptyList()) + ChatMessage(
                    "Error: ${e.message}",
                    false
                )
                _messages.postValue(errorList)
                _error.value = e.message
            } finally {
                _isLoading.postValue(false)
            }
        }
    }
    
    // Legacy method for compatibility
    fun sendQuery(question: String) {
        sendMessage(question)
    }
}
