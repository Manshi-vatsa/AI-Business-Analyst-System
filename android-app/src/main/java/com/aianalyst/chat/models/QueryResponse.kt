package com.aianalyst.chat.models

data class QueryResponse(
    val answer: String,
    val insights: List<String>
)
