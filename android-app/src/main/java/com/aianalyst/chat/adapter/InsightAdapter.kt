package com.aianalyst.chat.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.aianalyst.chat.databinding.ItemInsightBinding
import com.aianalyst.chat.models.Insight

class InsightAdapter : ListAdapter<Insight, InsightAdapter.InsightViewHolder>(InsightDiffCallback()) {
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): InsightViewHolder {
        val binding = ItemInsightBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return InsightViewHolder(binding)
    }
    
    override fun onBindViewHolder(holder: InsightViewHolder, position: Int) {
        holder.bind(getItem(position))
    }
    
    class InsightViewHolder(private val binding: ItemInsightBinding) : 
        RecyclerView.ViewHolder(binding.root) {
        
        fun bind(insight: Insight) {
            binding.textViewTitle.text = insight.title
            binding.textViewDescription.text = insight.description
            binding.textViewCategory.text = insight.category
            binding.textViewTimestamp.text = insight.timestamp
        }
    }
    
    private class InsightDiffCallback : DiffUtil.ItemCallback<Insight>() {
        override fun areItemsTheSame(oldItem: Insight, newItem: Insight): Boolean {
            return oldItem.id == newItem.id
        }
        
        override fun areContentsTheSame(oldItem: Insight, newItem: Insight): Boolean {
            return oldItem == newItem
        }
    }
}
