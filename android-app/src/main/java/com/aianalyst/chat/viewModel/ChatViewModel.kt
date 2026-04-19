package com.aianalyst.chat.viewModel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aianalyst.chat.models.ChatMessage
import com.aianalyst.chat.models.QueryResponse
import com.aianalyst.chat.repository.ChatRepository
import kotlinx.coroutines.launch
import java.util.UUID

class ChatViewModel : ViewModel() {
    
    private val repository = ChatRepository()
    
    private val _messages = MutableLiveData<List<ChatMessage>>()
    val messages: LiveData<List<ChatMessage>> = _messages
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _errorMessage = MutableLiveData<String?>()
    val errorMessage: LiveData<String?> = _errorMessage
    
    private val messageList = mutableListOf<ChatMessage>()
    
    init {
        _messages.value = messageList
    }
    
    fun sendMessage(question: String) {
        if (question.isBlank()) return
        
        val userMessage = ChatMessage(
            id = UUID.randomUUID().toString(),
            message = question,
            isUser = true
        )
        
        messageList.add(userMessage)
        _messages.value = messageList.toList()
        
        _isLoading.value = true
        _errorMessage.value = null
        
        viewModelScope.launch {
            val result = repository.sendQuery(question)
            _isLoading.value = false
            
            result.fold(
                onSuccess = { response ->
                    handleSuccessResponse(response)
                },
                onFailure = { error ->
                    handleError(error)
                }
            )
        }
    }
    
    private fun handleSuccessResponse(response: QueryResponse) {
        val answerMessage = ChatMessage(
            id = UUID.randomUUID().toString(),
            message = response.answer,
            isUser = false
        )
        
        messageList.add(answerMessage)
        
        if (response.insights.isNotEmpty()) {
            val insightsText = response.insights.joinToString("\n", "Insights:\n")
            val insightsMessage = ChatMessage(
                id = UUID.randomUUID().toString(),
                message = insightsText,
                isUser = false
            )
            messageList.add(insightsMessage)
        }
        
        _messages.value = messageList.toList()
    }
    
    private fun handleError(error: Throwable) {
        _errorMessage.value = "Failed to send message: ${error.message}"
    }
    
    fun clearError() {
        _errorMessage.value = null
    }
}
