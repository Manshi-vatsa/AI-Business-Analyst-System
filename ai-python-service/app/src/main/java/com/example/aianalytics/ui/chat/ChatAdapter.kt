package com.example.aianalytics.ui.chat

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.aianalytics.R
import com.example.aianalytics.data.models.ChatMessage

class ChatAdapter : RecyclerView.Adapter<ChatAdapter.ChatViewHolder>() {
    
    private var messages: List<ChatMessage> = emptyList()
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_chat_message, parent, false)
        return ChatViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        holder.bind(messages[position])
    }
    
    override fun getItemCount(): Int = messages.size
    
    // 🔥 STEP 4: FIX ADAPTER
    fun submitList(newList: List<ChatMessage>) {
        messages = newList
        notifyDataSetChanged()
    }
    
    class ChatViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val messageText: TextView = itemView.findViewById(R.id.tvMessage)
        private val container: View = itemView.findViewById(R.id.messageContainer)
        
        fun bind(message: ChatMessage) {
            messageText.text = message.text
            
            // Set different background for user vs bot messages
            if (message.isUser) {
                container.setBackgroundResource(R.drawable.bg_user_message)
                messageText.textAlignment = TextView.TEXT_ALIGNMENT_TEXT_END
            } else {
                container.setBackgroundResource(R.drawable.bg_bot_message)
                messageText.textAlignment = TextView.TEXT_ALIGNMENT_TEXT_START
            }
        }
    }
}
