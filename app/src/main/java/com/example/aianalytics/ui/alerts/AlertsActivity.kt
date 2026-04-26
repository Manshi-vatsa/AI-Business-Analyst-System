package com.example.aianalytics.ui.alerts

import android.os.Bundle
import android.view.View
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.aianalytics.R
import com.example.aianalytics.ui.alerts.AlertAdapter
import com.example.aianalytics.viewmodel.AlertsViewModel

class AlertsActivity : AppCompatActivity() {
    
    private lateinit var viewModel: AlertsViewModel
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var alertAdapter: AlertAdapter
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_alerts)
        
        initViews()
        setupRecyclerView()
        setupViewModel()
    }
    
    private fun initViews() {
        recyclerView = findViewById(R.id.recyclerViewAlerts)
        progressBar = findViewById(R.id.progressBar)
    }
    
    private fun setupRecyclerView() {
        alertAdapter = AlertAdapter(emptyList())
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = alertAdapter
    }
    
    private fun setupViewModel() {
        viewModel = ViewModelProvider(this)[AlertsViewModel::class.java]
        
        viewModel.alerts.observe(this) { alerts ->
            alertAdapter.updateData(alerts)
        }
        
        viewModel.isLoading.observe(this) { isLoading ->
            progressBar.visibility = if (isLoading) android.view.View.VISIBLE else android.view.View.GONE
        }
        
        viewModel.error.observe(this) { error ->
            error?.let {
                Toast.makeText(this, "Error: $it", Toast.LENGTH_LONG).show()
            }
        }
        
        // Load alerts when activity starts
        viewModel.loadAlerts()
    }
}
