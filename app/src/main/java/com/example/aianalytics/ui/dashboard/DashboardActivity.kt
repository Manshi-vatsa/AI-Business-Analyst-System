package com.example.aianalytics.ui.dashboard

import android.graphics.Color
import android.os.Bundle
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.example.aianalytics.R
import com.example.aianalytics.data.models.MonthlySale
import com.example.aianalytics.data.models.DashboardResponse
import com.example.aianalytics.viewmodel.DashboardViewModel
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.charts.PieChart
import com.github.mikephil.charting.charts.BarChart
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.github.mikephil.charting.data.PieData
import com.github.mikephil.charting.data.PieDataSet
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry
import com.github.mikephil.charting.formatter.PercentFormatter
import com.github.mikephil.charting.utils.ColorTemplate

class DashboardActivity : AppCompatActivity() {
    
    private lateinit var viewModel: DashboardViewModel
    private lateinit var lineChart: LineChart
    private lateinit var pieChart: PieChart
    private lateinit var barChart: BarChart
    private lateinit var progressBar: ProgressBar
    private lateinit var totalSalesCard: TextView
    private lateinit var avgSalesCard: TextView
    private lateinit var growthCard: TextView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard)
        
        initViews()
        setupViewModel()
        setupCharts()
        loadDashboardData()
    }
    
    private fun initViews() {
        lineChart = findViewById(R.id.lineChart)
        pieChart = findViewById(R.id.pieChart)
        barChart = findViewById(R.id.barChart)
        progressBar = findViewById(R.id.progressBar)
        totalSalesCard = findViewById(R.id.totalSalesCard)
        avgSalesCard = findViewById(R.id.avgSalesCard)
        growthCard = findViewById(R.id.growthCard)
    }
    
    private fun setupViewModel() {
        viewModel = ViewModelProvider(this)[DashboardViewModel::class.java]
        
        viewModel.salesData.observe(this) { sales ->
            updateCharts(sales)
        }
        
        viewModel.isLoading.observe(this) { isLoading ->
            progressBar.visibility = if (isLoading) android.view.View.VISIBLE else android.view.View.GONE
        }
        
        viewModel.error.observe(this) { error ->
            error?.let {
                Toast.makeText(this, "Error: $it", Toast.LENGTH_LONG).show()
            }
        }
    }
    
    private fun loadDashboardData() {
        viewModel.loadSalesData()
    }
    
    private fun setupCharts() {
        setupLineChart()
        setupPieChart()
        setupBarChart()
    }
    
    private fun setupLineChart() {
        lineChart.description.isEnabled = true
        lineChart.description.text = "Monthly Sales Trend"
        lineChart.setTouchEnabled(true)
        lineChart.isDragEnabled = true
        lineChart.setScaleEnabled(true)
        lineChart.setPinchZoom(true)
        lineChart.setDrawGridBackground(false)
        
        lineChart.xAxis.isEnabled = true
        lineChart.axisLeft.isEnabled = true
        lineChart.axisRight.isEnabled = false
        lineChart.legend.isEnabled = true
    }
    
    private fun setupPieChart() {
        pieChart.description.isEnabled = false
        pieChart.setUsePercentValues(true)
        pieChart.setDrawEntryLabels(true)
        pieChart.setDrawHoleEnabled(true)
        pieChart.setHoleColor(Color.WHITE)
        pieChart.transparentCircleRadius = 58f
        pieChart.holeRadius = 48f
        pieChart.setDrawCenterText(true)
        pieChart.centerText = "Sales by Region"
        pieChart.rotationAngle = 0f
        pieChart.isRotationEnabled = true
        pieChart.isHighlightPerTapEnabled = true
        pieChart.legend.isEnabled = true
    }
    
    private fun setupBarChart() {
        barChart.description.isEnabled = true
        barChart.description.text = "Product Performance"
        barChart.setTouchEnabled(true)
        barChart.isDragEnabled = true
        barChart.setScaleEnabled(true)
        barChart.setDrawGridBackground(false)
        
        barChart.xAxis.isEnabled = true
        barChart.axisLeft.isEnabled = true
        barChart.axisRight.isEnabled = false
        barChart.legend.isEnabled = true
    }
    
    private fun updateCharts(sales: List<MonthlySale>) {
        if (sales.isEmpty()) return
        
        updateLineChart(sales)
        updatePieChart()
        updateBarChart()
        updateSummaryCards(sales)
    }
    
    private fun updateLineChart(sales: List<MonthlySale>) {
        val entries = mutableListOf<Entry>()
        sales.forEachIndexed { index, sale ->
            entries.add(Entry(index.toFloat(), sale.revenue.toFloat()))
        }
        
        val dataSet = LineDataSet(entries, "Revenue").apply {
            color = Color.BLUE
            valueTextColor = Color.BLACK
            lineWidth = 2f
            circleRadius = 4f
            setDrawCircleHole(false)
            setDrawValues(true)
        }
        
        val lineData = LineData(dataSet)
        lineChart.data = lineData
        lineChart.invalidate()
    }
    
    private fun updatePieChart() {
        // Mock region data for pie chart
        val entries = mutableListOf<com.github.mikephil.charting.data.PieEntry>()
        entries.add(com.github.mikephil.charting.data.PieEntry(35f, "North"))
        entries.add(com.github.mikephil.charting.data.PieEntry(25f, "South"))
        entries.add(com.github.mikephil.charting.data.PieEntry(20f, "East"))
        entries.add(com.github.mikephil.charting.data.PieEntry(20f, "West"))
        
        val dataSet = PieDataSet(entries, "Region Sales").apply {
            colors = ColorTemplate.COLORFUL_COLORS.toList()
            valueTextColor = Color.BLACK
            valueTextSize = 12f
            setDrawValues(true)
        }
        
        val pieData = PieData(dataSet)
        pieData.setValueFormatter(PercentFormatter(pieChart))
        pieChart.data = pieData
        pieChart.invalidate()
    }
    
    private fun updateBarChart() {
        // Mock product data for bar chart
        val entries = mutableListOf<BarEntry>()
        entries.add(BarEntry(0f, 75000f))
        entries.add(BarEntry(1f, 50000f))
        entries.add(BarEntry(2f, 30000f))
        
        val dataSet = BarDataSet(entries, "Product Revenue").apply {
            colors = listOf(Color.RED, Color.GREEN, Color.BLUE)
            valueTextColor = Color.BLACK
            valueTextSize = 12f
            setDrawValues(true)
        }
        
        val barData = BarData(dataSet)
        barChart.data = barData
        barChart.invalidate()
    }
    
    private fun updateSummaryCards(sales: List<MonthlySale>) {
        val totalSales = sales.sumOf { it.revenue.toDouble() }
        val avgSales = if (sales.isNotEmpty()) totalSales / sales.size else 0.0
        val growth = if (sales.size >= 2) {
            ((sales.last().revenue - sales.first().revenue) / sales.first().revenue * 100)
        } else 0.0
        
        totalSalesCard.text = "Total Sales\n$${String.format("%.0f", totalSales)}"
        avgSalesCard.text = "Avg Sales\n$${String.format("%.0f", avgSales)}"
        growthCard.text = "Growth\n${String.format("%.1f", growth)}%"
    }
}
