package com.example.aianalytics.utils

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.os.Build
import android.util.Log

object NetworkConfig {
    
    private const val TAG = "NetworkConfig"
    
    // Default port for Python service
    private const val DEFAULT_PORT = 8000
    
    /**
     * Get the appropriate base URL based on the current environment
     */
    fun getBaseUrl(context: Context? = null): String {
        return try {
            when {
                isRunningOnEmulator() -> {
                    Log.d(TAG, "Running on emulator, using 10.0.2.2")
                    "http://10.0.2.2:$DEFAULT_PORT/"
                }
                isRunningOnRealDevice() -> {
                    // For real device, you need to replace this with your actual computer's IP
                    // To find your IP:
                    // 1. On Windows: ipconfig in command prompt
                    // 2. On Mac/Linux: ifconfig or ip addr in terminal
                    // 3. Look for IPv4 address (usually 192.168.x.x)
                    val computerIp = "192.168.29.53" // <-- REPLACE WITH YOUR ACTUAL IP
                    Log.d(TAG, "Running on real device, using computer IP: $computerIp")
                    "http://$computerIp:$DEFAULT_PORT/"
                }
                else -> {
                    Log.d(TAG, "Unknown environment, using localhost")
                    "http://localhost:$DEFAULT_PORT/"
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error determining base URL, using fallback", e)
            "http://10.0.2.2:$DEFAULT_PORT/"
        }
    }
    
    /**
     * Check if running on Android emulator
     */
    private fun isRunningOnEmulator(): Boolean {
        return (Build.FINGERPRINT.startsWith("generic")
                || Build.FINGERPRINT.startsWith("unknown")
                || Build.MODEL.contains("google_sdk")
                || Build.MODEL.contains("Emulator")
                || Build.MODEL.contains("Android SDK built for x86")
                || Build.MANUFACTURER.contains("Genymotion")
                || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
                || "google_sdk" == Build.PRODUCT)
    }
    
    /**
     * Check if running on a real device
     */
    private fun isRunningOnRealDevice(): Boolean {
        return !isRunningOnEmulator()
    }
    
    /**
     * Check if network is available using modern NetworkCapabilities API
     */
    fun debugNetworkInfo(context: Context): String {
        val info = StringBuilder()
        info.append("=== Network Debug Info ===\n")
        info.append("Model: ${Build.MODEL}\n")
        info.append("Manufacturer: ${Build.MANUFACTURER}\n")
        info.append("Is Emulator: ${isRunningOnEmulator()}\n")
        info.append("Is Real Device: ${isRunningOnRealDevice()}\n")
        info.append("Base URL: ${getBaseUrl(context)}\n")
        info.append("Network Available: ${isNetworkAvailable(context)}\n")
        
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val activeNetwork = connectivityManager.activeNetwork
        if (activeNetwork != null) {
            val networkCapabilities = connectivityManager.getNetworkCapabilities(activeNetwork)
            if (networkCapabilities != null) {
                info.append("Has Internet: ${networkCapabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)}\n")
                info.append("Has WiFi: ${networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)}\n")
                info.append("Has Cellular: ${networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)}\n")
            }
        }
        return info.toString()
    }
    
    fun isNetworkAvailable(context: Context): Boolean {
        return try {
            val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
            
            // For API level < 23, use deprecated method
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) {
                @Suppress("DEPRECATION")
                val networkInfo = connectivityManager.activeNetworkInfo
                return networkInfo?.isConnectedOrConnecting == true
            }
            
            // For API level >= 23, use modern method
            val activeNetwork = connectivityManager.activeNetwork
            if (activeNetwork == null) return false
            val networkCapabilities = connectivityManager.getNetworkCapabilities(activeNetwork) ?: return false
            
            networkCapabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
        } catch (e: Exception) {
            Log.e(TAG, "Error checking network availability", e)
            false
        }
    }
    
    /**
     * Test connectivity to the server
     */
    fun canConnectToServer(baseUrl: String): Boolean {
        return try {
            val url = java.net.URL(baseUrl)
            val connection = url.openConnection() as java.net.HttpURLConnection
            connection.requestMethod = "HEAD"
            connection.connectTimeout = 5000
            connection.readTimeout = 5000
            connection.responseCode == 200
        } catch (e: Exception) {
            Log.e(TAG, "Cannot connect to server: ${e.message}")
            false
        }
    }
}
