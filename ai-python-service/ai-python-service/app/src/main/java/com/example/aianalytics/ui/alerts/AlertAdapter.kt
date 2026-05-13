package com.example.aianalytics.ui.alerts

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.aianalytics.R
import com.example.aianalytics.data.models.Alert

class AlertAdapter(private var alerts: List<Alert>) : RecyclerView.Adapter<AlertAdapter.AlertViewHolder>() {
    
    class AlertViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvAlertMessage: TextView = itemView.findViewById(R.id.tvAlertMessage)
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AlertViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_alert, parent, false)
        return AlertViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: AlertViewHolder, position: Int) {
        holder.tvAlertMessage.text = alerts[position].message
    }
    
    override fun getItemCount(): Int = alerts.size
    
    fun updateData(newAlerts: List<Alert>) {
        alerts = newAlerts
        notifyDataSetChanged()
    }
}
