package com.aianalyst.chat

import android.os.Bundle
import android.view.View
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.aianalyst.chat.adapter.InsightAdapter
import com.aianalyst.chat.databinding.ActivityInsightsBinding
import com.aianalyst.chat.viewModel.InsightsViewModel

class InsightsActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityInsightsBinding
    private lateinit var insightAdapter: InsightAdapter
    private val viewModel: InsightsViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityInsightsBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupUI()
        setupRecyclerView()
        setupObservers()
        loadInsights()
    }
    
    private fun setupUI() {
        setSupportActionBar(binding.toolbar)
        supportActionBar?.apply {
            setDisplayHomeAsUpEnabled(true)
            title = "Insights"
        }
        
        binding.bottomNavigation.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_chat -> {
                    finish() // Go back to chat
                    true
                }
                R.id.nav_dashboard -> {
                    // Navigate to dashboard
                    // TODO: Implement navigation to DashboardActivity
                    true
                }
                R.id.nav_insights -> true // Already on insights
                else -> false
            }
        }
        binding.bottomNavigation.selectedItemId = R.id.nav_insights
    }
    
    private fun setupRecyclerView() {
        insightAdapter = InsightAdapter()
        binding.recyclerViewInsights.apply {
            layoutManager = LinearLayoutManager(this@InsightsActivity)
            adapter = insightAdapter
        }
    }
    
    private fun setupObservers() {
        viewModel.insights.observe(this) { insights ->
            insightAdapter.submitList(insights)
            binding.textViewEmpty.visibility = if (insights.isEmpty()) View.VISIBLE else View.GONE
        }
        
        viewModel.isLoading.observe(this) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        }
        
        viewModel.errorMessage.observe(this) { errorMessage ->
            errorMessage?.let {
                // Show error message (could use Toast or Snackbar)
                binding.textViewError.text = it
                binding.textViewError.visibility = View.VISIBLE
                viewModel.clearError()
            }
        }
    }
    
    private fun loadInsights() {
        viewModel.loadInsights()
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
