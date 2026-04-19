package com.ai.analytics.controller;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class MinimalController {
    
    @Autowired
    private RestTemplate restTemplate;
    
    @PostMapping("/query")
    public ResponseEntity<Map<String, Object>> processQuery(@RequestBody Map<String, String> request) {
        Map<String, Object> response = new HashMap<>();
        
        try {
            String question = request.get("question");
            if (question == null || question.trim().isEmpty()) {
                response.put("status", "error");
                response.put("message", "Question is required");
                return ResponseEntity.badRequest().body(response);
            }
            
            // Mock response for now - just return success
            response.put("status", "success");
            response.put("data", "Mock response for: " + question);
            response.put("message", "Query processed successfully");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", "Internal server error: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    @GetMapping("/dashboard")
    public ResponseEntity<Map<String, Object>> getDashboardData() {
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Mock dashboard data for now
            Map<String, Object> dashboardData = new HashMap<>();
            dashboardData.put("totalSales", 100000);
            dashboardData.put("totalRevenue", 500000);
            dashboardData.put("topProducts", 10);
            
            response.put("status", "success");
            response.put("data", dashboardData);
            response.put("message", "Dashboard data retrieved successfully");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", "Failed to retrieve dashboard data: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
}
