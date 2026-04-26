package com.example.aianalytics.ui.insights

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.aianalytics.R
import com.example.aianalytics.data.models.Insight

class InsightAdapter(private var insights: List<Insight>) : RecyclerView.Adapter<InsightAdapter.InsightViewHolder>() {
    
    class InsightViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvInsightMessage: TextView = itemView.findViewById(R.id.tvInsightMessage)
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): InsightViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_insight, parent, false)
        return InsightViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: InsightViewHolder, position: Int) {
        holder.tvInsightMessage.text = insights[position].message
    }
    
    override fun getItemCount(): Int = insights.size
    
    fun updateData(newInsights: List<Insight>) {
        insights = newInsights
        notifyDataSetChanged()
    }
}
