package com.example.aianalytics.data.model

data class DashboardResponse(
    val monthlySales: List<Sales> = emptyList(),
    val regionSales: List<Any> = emptyList(),
    val productSales: List<Any> = emptyList()
)
