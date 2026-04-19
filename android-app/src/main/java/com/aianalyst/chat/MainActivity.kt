package com.aianalyst.chat

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.aianalyst.chat.adapter.ChatMessageAdapter
import com.aianalyst.chat.databinding.ActivityMainBinding
import com.aianalyst.chat.viewModel.ChatViewModel

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private lateinit var messageAdapter: ChatMessageAdapter
    private val viewModel: ChatViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupToolbar()
        setupRecyclerView()
        setupObservers()
        setupClickListeners()
        setupBottomNavigation()
    }
    
    private fun setupToolbar() {
        // Toolbar is set in layout, no need to setSupportActionBar with NoActionBar theme
        supportActionBar?.apply {
            title = "AI Business Analyst"
        }
    }
    
    private fun setupRecyclerView() {
        try {
            messageAdapter = ChatMessageAdapter()
            binding.recyclerViewMessages?.apply {
                layoutManager = LinearLayoutManager(this@MainActivity).apply {
                    stackFromEnd = true
                }
                adapter = messageAdapter
            }
        } catch (e: Exception) {
            Toast.makeText(this, "Error setting up RecyclerView: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }
    
    private fun setupObservers() {
        viewModel.messages.observe(this) { messages ->
            messageAdapter.submitList(messages)
            binding.recyclerViewMessages.scrollToPosition(messages.size - 1)
        }
        
        viewModel.isLoading.observe(this) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.buttonSend.isEnabled = !isLoading
        }
        
        viewModel.errorMessage.observe(this) { errorMessage ->
            errorMessage?.let {
                Toast.makeText(this, it, Toast.LENGTH_LONG).show()
                viewModel.clearError()
            }
        }
    }
    
    private fun setupClickListeners() {
        try {
            binding.buttonSend.setOnClickListener {
                val message = binding.editTextMessage.text?.toString()?.trim() ?: ""
                if (message.isNotEmpty()) {
                    viewModel.sendMessage(message)
                    binding.editTextMessage.text?.clear()
                }
            }
            
            binding.editTextMessage.setOnEditorActionListener { _, actionId, _ ->
                if (actionId == android.view.inputmethod.EditorInfo.IME_ACTION_SEND) {
                    binding.buttonSend.performClick()
                    return@setOnEditorActionListener true
                }
                false
            }
        } catch (e: Exception) {
            Toast.makeText(this, "Error setting up listeners: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }
    
    private fun setupBottomNavigation() {
        binding.bottomNavigation.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_chat -> true // Already on chat
                R.id.nav_dashboard -> {
                    startActivity(Intent(this, DashboardActivity::class.java))
                    true
                }
                R.id.nav_insights -> {
                    startActivity(Intent(this, InsightsActivity::class.java))
                    true
                }
                else -> false
            }
        }
        binding.bottomNavigation.selectedItemId = R.id.nav_chat
    }
}
