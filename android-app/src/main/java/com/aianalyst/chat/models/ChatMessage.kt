package com.aianalyst.chat.models

data class ChatMessage(
    val id: String,
    val message: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)
