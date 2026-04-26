package com.example.aianalytics.ui.chat

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.aianalytics.R
import com.example.aianalytics.ui.chat.ChatAdapter
import com.example.aianalytics.viewmodel.ChatViewModel

class ChatActivity : AppCompatActivity() {
    
    private val TAG = "ChatActivity"
    
    // UI Components
    private lateinit var etQuestion: EditText
    private lateinit var btnSend: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var recyclerView: RecyclerView
    
    // Chat Components
    private lateinit var chatAdapter: ChatAdapter
    private lateinit var chatViewModel: ChatViewModel
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat)
        
        Log.d(TAG, "=== CHAT ACTIVITY CREATED ===")
        
        initViews()
        setupViewModel()
        setupRecyclerView()
        setupClickListeners()
    }
    
    private fun initViews() {
        Log.d(TAG, "Initializing views...")
        
        etQuestion = findViewById(R.id.etQuestion)
        btnSend = findViewById(R.id.btnSend)
        progressBar = findViewById(R.id.progressBar)
        recyclerView = findViewById(R.id.recyclerView)
        
        Log.d(TAG, "✅ Views initialized")
    }
    
    private fun setupViewModel() {
        Log.d(TAG, "Setting up ViewModel...")
        
        chatViewModel = ViewModelProvider(this)[ChatViewModel::class.java]
        
        // 🔥 STEP 3: FIX ChatActivity OBSERVER
        chatViewModel.messages.observe(this) { messages ->
            Log.d("CHAT_DEBUG", "Messages updated: ${messages.size}")
            chatAdapter.submitList(messages)
        }
        
        chatViewModel.isLoading.observe(this) { isLoading ->
            progressBar.visibility = if (isLoading) android.view.View.VISIBLE else android.view.View.GONE
            btnSend.isEnabled = !isLoading
        }
        
        chatViewModel.error.observe(this) { error ->
            if (error.isNotEmpty()) {
                Toast.makeText(this, error, Toast.LENGTH_SHORT).show()
            }
        }
        
        Log.d(TAG, "✅ ViewModel setup completed")
    }
    
    private fun setupRecyclerView() {
        Log.d(TAG, "Setting up RecyclerView...")
        
        chatAdapter = ChatAdapter()
        recyclerView.apply {
            layoutManager = LinearLayoutManager(this@ChatActivity)
            adapter = chatAdapter
        }
        
        Log.d(TAG, "✅ RecyclerView setup completed")
    }
    
    private fun setupClickListeners() {
        Log.d(TAG, "Setting up click listeners...")
        
        btnSend.setOnClickListener {
            val question = etQuestion.text.toString().trim()
            if (question.isEmpty()) {
                Toast.makeText(this, "Please enter a question", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            
            Log.d(TAG, "Send button clicked with question: $question")
            chatViewModel.sendMessage(question)
            etQuestion.text.clear()
        }
        
        Log.d(TAG, "✅ Click listeners setup completed")
    }
    
}
