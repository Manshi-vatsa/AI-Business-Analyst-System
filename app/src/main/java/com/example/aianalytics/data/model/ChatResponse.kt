package com.example.aianalytics.data.model

import com.google.gson.annotations.SerializedName

data class ChatResponse(

    @SerializedName("answer")
    val answer: String? = null,

    @SerializedName("insights")
    val insights: List<String> = emptyList()
)