package com.example.aianalytics.data.model

import com.google.gson.annotations.SerializedName

data class MonthlySale(
    @SerializedName("month")
    val month: String,
    
    @SerializedName("revenue")
    val revenue: Double
)
