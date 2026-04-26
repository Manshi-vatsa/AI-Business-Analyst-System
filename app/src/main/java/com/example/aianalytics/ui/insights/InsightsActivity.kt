package com.example.aianalytics.ui.insights

import android.os.Bundle
import android.view.View
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.aianalytics.R
import com.example.aianalytics.ui.insights.InsightAdapter
import com.example.aianalytics.viewmodel.InsightsViewModel

class InsightsActivity : AppCompatActivity() {
    
    private lateinit var viewModel: InsightsViewModel
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var insightAdapter: InsightAdapter
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_insights)
        
        initViews()
        setupRecyclerView()
        setupViewModel()
    }
    
    private fun initViews() {
        recyclerView = findViewById(R.id.recyclerViewInsights)
        progressBar = findViewById(R.id.progressBar)
    }
    
    private fun setupRecyclerView() {
        insightAdapter = InsightAdapter(emptyList())
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = insightAdapter
    }
    
    private fun setupViewModel() {
        viewModel = ViewModelProvider(this)[InsightsViewModel::class.java]
        
        viewModel.insights.observe(this) { insights ->
            insightAdapter.updateData(insights)
        }
        
        viewModel.isLoading.observe(this) { isLoading ->
            progressBar.visibility = if (isLoading) android.view.View.VISIBLE else android.view.View.GONE
        }
        
        viewModel.error.observe(this) { error ->
            error?.let {
                Toast.makeText(this, "Error: $it", Toast.LENGTH_LONG).show()
            }
        }
        
        // Load insights when activity starts
        viewModel.loadInsights()
    }
}
