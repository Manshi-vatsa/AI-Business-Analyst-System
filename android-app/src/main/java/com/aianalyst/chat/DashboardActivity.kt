package com.aianalyst.chat

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.aianalyst.chat.databinding.ActivityDashboardBinding

class DashboardActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityDashboardBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityDashboardBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupUI()
    }
    
    private fun setupUI() {
        // Set up toolbar
        setSupportActionBar(binding.toolbar)
        supportActionBar?.apply {
            setDisplayHomeAsUpEnabled(true)
            title = "Dashboard"
        }
        
        // Bottom navigation setup
        binding.bottomNavigation.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_chat -> {
                    finish() // Go back to chat
                    true
                }
                R.id.nav_dashboard -> true // Already on dashboard
                R.id.nav_insights -> {
                    // Navigate to insights
                    // TODO: Implement navigation to InsightsActivity
                    true
                }
                else -> false
            }
        }
        binding.bottomNavigation.selectedItemId = R.id.nav_dashboard
        
        // Load sample charts data
        loadSampleCharts()
    }
    
    private fun loadSampleCharts() {
        // TODO: Implement sample charts
        // For now, just show placeholder text
        binding.textViewChartsInfo.text = "Sample charts will be displayed here\n\n" +
            "Revenue Trend: $125,000 (up 15%)\n" +
            "Customer Growth: +234 new customers\n" +
            "Product Performance: Top 3 products\n" +
            "Regional Sales: North America leads"
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
