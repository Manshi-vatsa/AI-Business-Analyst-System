package com.example.aianalytics

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.example.aianalytics.R
import com.example.aianalytics.ui.alerts.AlertsActivity
import com.example.aianalytics.ui.chat.ChatActivity
import com.example.aianalytics.ui.dashboard.DashboardActivity
import com.example.aianalytics.ui.insights.InsightsActivity

class MainActivity : AppCompatActivity() {
    
    private lateinit var btnChat: Button
    private lateinit var btnDashboard: Button
    private lateinit var btnInsights: Button
    private lateinit var btnAlerts: Button
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initViews()
        setupClickListeners()
    }
    
    private fun initViews() {
        btnChat = findViewById(R.id.btnChat)
        btnDashboard = findViewById(R.id.btnDashboard)
        btnInsights = findViewById(R.id.btnInsights)
        btnAlerts = findViewById(R.id.btnAlerts)
    }
    
    private fun setupClickListeners() {
        btnChat.setOnClickListener {
            startActivity(Intent(this, ChatActivity::class.java))
        }
        
        btnDashboard.setOnClickListener {
            startActivity(Intent(this, DashboardActivity::class.java))
        }
        
        btnInsights.setOnClickListener {
            startActivity(Intent(this, InsightsActivity::class.java))
        }
        
        btnAlerts.setOnClickListener {
            startActivity(Intent(this, AlertsActivity::class.java))
        }
    }
}
