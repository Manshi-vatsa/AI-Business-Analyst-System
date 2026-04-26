package com.example.aianalytics.data.models

/**
 * Chat message data model for chat UI
 */
data class ChatMessage(
    val text: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)
