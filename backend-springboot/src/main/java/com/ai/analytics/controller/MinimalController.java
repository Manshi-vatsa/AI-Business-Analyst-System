package com.ai.analytics.controller;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;

import java.util.HashMap;
import java.util.Map;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.ai.analytics.dto.ApiResponseDto;

@RestController
@RequestMapping("/ai")
@CrossOrigin(origins = "*")
public class MinimalController {
    
    private static final Logger logger = LoggerFactory.getLogger(MinimalController.class);
    
    @Autowired
    private RestTemplate restTemplate;
    
    @PostMapping("/query")
    public ResponseEntity<Map<String, Object>> processQuery(@RequestBody Map<String, String> request) {
        logger.info("=== SPRING BOOT QUERY PROCESSING ===");
        logger.info("1. Request received: {}", request);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            String question = request.get("question");
            logger.info("2. Question extracted: {}", question);
            
            if (question == null || question.trim().isEmpty()) {
                logger.warn("3. Question is empty or null");
                response.put("status", "error");
                response.put("message", "Question is required");
                return ResponseEntity.badRequest().body(response);
            }
            
            // Call Python FastAPI service on localhost:8000
            String pythonApiUrl = "http://localhost:8000/ai/query";
            logger.info("4. Calling Python API: {}", pythonApiUrl);
            
            try {
                Map<String, String> pythonRequest = new HashMap<>();
                pythonRequest.put("question", question);
                
                ResponseEntity<Map<String, Object>> pythonResponse = restTemplate.exchange(
                    pythonApiUrl, HttpMethod.POST, 
                    new HttpEntity<>(pythonRequest), 
                    new ParameterizedTypeReference<Map<String, Object>>() {});
                
                if (pythonResponse.getStatusCode().is2xxSuccessful()) {
                    Map<String, Object> pythonData = pythonResponse.getBody();
                    logger.info("5. Python API response successful: {}", pythonData);
                    return ResponseEntity.ok(pythonData);
                } else {
                    logger.error("5. Python API error status: {}", pythonResponse.getStatusCode());
                    response.put("status", "error");
                    response.put("message", "Python service error: " + pythonResponse.getStatusCode());
                    return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(response);
                }
                
            } catch (Exception e) {
                logger.error("5. Python API call failed: {}", e.getMessage());
                // Fallback to mock response if Python service is unavailable
                response.put("status", "success");
                response.put("data", Map.of(
                    "answer", "Mock response for: " + question + " (Python service unavailable)",
                    "insights", List.of("Service unavailable", "Using fallback response")
                ));
                response.put("message", "Query processed with fallback");
                logger.info("6. Using fallback response");
                return ResponseEntity.ok(response);
            }
            
        } catch (Exception e) {
            logger.error("7. Internal server error: {}", e.getMessage(), e);
            response.put("status", "error");
            response.put("message", "Internal server error: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    @GetMapping("/dashboard")
    public ResponseEntity<Map<String, Object>> getDashboardData() {
        logger.info("=== SPRING BOOT DASHBOARD PROCESSING ===");
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Call Python FastAPI service for dashboard data
            String pythonApiUrl = "http://localhost:8000/ai/dashboard";
            logger.info("1. Calling Python dashboard API: {}", pythonApiUrl);
            
            try {
                ResponseEntity<Map<String, Object>> pythonResponse = restTemplate.exchange(
                    pythonApiUrl, HttpMethod.GET, 
                    null, 
                    new ParameterizedTypeReference<Map<String, Object>>() {});
                
                if (pythonResponse.getStatusCode().is2xxSuccessful()) {
                    Map<String, Object> dashboardData = pythonResponse.getBody();
                    logger.info("2. Python dashboard response successful: {}", dashboardData);
                    return ResponseEntity.ok(dashboardData);
                } else {
                    logger.error("2. Python dashboard error status: {}", pythonResponse.getStatusCode());
                    // Fallback to mock data
                    Map<String, Object> mockData = new HashMap<>();
                    mockData.put("monthlySales", List.of(
                        Map.of("month", "2024-01", "revenue", 75000.0),
                        Map.of("month", "2024-02", "revenue", 82000.0)
                    ));
                    mockData.put("regionSales", List.of(
                        Map.of("region", "North", "revenue", 125000.0),
                        Map.of("region", "South", "revenue", 89000.0)
                    ));
                    mockData.put("productSales", List.of(
                        Map.of("product", "Laptop", "revenue", 185000.0),
                        Map.of("product", "Phone", "revenue", 125000.0)
                    ));
                    
                    ApiResponseDto apiResponse = new ApiResponseDto("success", "Dashboard data retrieved (mock)", mockData);
                    logger.info("3. Using mock dashboard data");
                    return ResponseEntity.ok(Map.of(
                        "status", apiResponse.getStatus(),
                        "data", apiResponse.getData(),
                        "message", apiResponse.getMessage(),
                        "timestamp", apiResponse.getTimestamp()
                    ));
                }
                
            } catch (Exception e) {
                logger.error("2. Python dashboard API call failed: {}", e.getMessage());
                // Return error response
                response.put("status", "error");
                response.put("message", "Failed to retrieve dashboard data: " + e.getMessage());
                return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(response);
            }
            
        } catch (Exception e) {
            logger.error("3. Internal server error in dashboard: {}", e.getMessage(), e);
            response.put("status", "error");
            response.put("message", "Internal server error: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    @GetMapping("/insights")
    public ResponseEntity<Map<String, Object>> getInsights() {
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Mock insights data
            Map<String, Object> insights = new HashMap<>();
            insights.put("type", "sales_drop");
            insights.put("message", "Sales decreased by 15% this week");
            insights.put("value", -15.0);
            
            response.put("status", "success");
            response.put("data", insights);
            response.put("message", "Insights retrieved successfully");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", "Failed to retrieve insights: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    @GetMapping("/alerts")
    public ResponseEntity<Map<String, Object>> getAlerts() {
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Mock alerts data
            Map<String, Object> alerts = new HashMap<>();
            alerts.put("title", "Low Inventory Alert");
            alerts.put("message", "Laptop inventory running low");
            alerts.put("priority", "medium");
            alerts.put("timestamp", "2024-01-23T15:45:00Z");
            
            response.put("status", "success");
            response.put("data", alerts);
            response.put("message", "Alerts retrieved successfully");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", "Failed to retrieve alerts: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
}
