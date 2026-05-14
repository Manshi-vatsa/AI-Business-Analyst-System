package com.ai.analytics.controller;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;

import java.util.HashMap;
import java.util.Map;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
@RequestMapping("/ai")
@CrossOrigin(origins = "*")
public class MinimalController {

    private static final Logger logger =
            LoggerFactory.getLogger(MinimalController.class);

    // ==========================================
    // PYTHON AI SERVICE URL
    // ==========================================
    private static final String PYTHON_BASE_URL =
            System.getenv().getOrDefault(
                    "FASTAPI_URL",
                    "https://ai-business-analyst-system.onrender.com"
            );

    @Autowired
    private RestTemplate restTemplate;

    // ==========================================
    // HEALTH ENDPOINT
    // ==========================================
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {

        Map<String, Object> response = new HashMap<>();

        response.put("status", "healthy");
        response.put("springboot", true);
        response.put("python_ai_url", PYTHON_BASE_URL);

        return ResponseEntity.ok(response);
    }

    // ==========================================
    // QUERY ENDPOINT
    // ==========================================
    @PostMapping("/query")
    public ResponseEntity<Map<String, Object>> processQuery(
            @RequestBody Map<String, String> request
    ) {

        logger.info("=== QUERY PROCESSING START ===");

        Map<String, Object> response = new HashMap<>();

        try {

            String question = request.get("question");

            logger.info("Question received = {}", question);

            // ==========================================
            // VALIDATION
            // ==========================================
            if (question == null || question.trim().isEmpty()) {

                response.put("status", "error");
                response.put("message", "Question is required");

                return ResponseEntity
                        .badRequest()
                        .body(response);
            }

            // ==========================================
            // PYTHON API URL
            // ==========================================
            String pythonApiUrl =
                    PYTHON_BASE_URL + "/ai/query";

            logger.info("Calling Python API = {}", pythonApiUrl);

            try {

                Map<String, String> pythonRequest =
                        new HashMap<>();

                pythonRequest.put("question", question);

                HttpHeaders headers = new HttpHeaders();
                headers.setContentType(MediaType.APPLICATION_JSON);

                HttpEntity<Map<String, String>> entity =
                        new HttpEntity<>(pythonRequest, headers);

                ResponseEntity<Map<String, Object>> pythonResponse =
                        restTemplate.exchange(
                                pythonApiUrl,
                                HttpMethod.POST,
                                entity,
                                new ParameterizedTypeReference<Map<String, Object>>() {}
                        );

                logger.info(
                        "Python API response status = {}",
                        pythonResponse.getStatusCode()
                );

                // ==========================================
                // SUCCESS RESPONSE
                // ==========================================
                if (pythonResponse.getStatusCode().is2xxSuccessful()
                        && pythonResponse.getBody() != null) {

                    return ResponseEntity.ok(
                            pythonResponse.getBody()
                    );
                }

            } catch (RestClientException e) {

                logger.error(
                        "Python AI unavailable = {}",
                        e.getMessage()
                );
            }

            // ==========================================
            // FALLBACK RESPONSE
            // ==========================================
            response.put("status", "success");

            response.put(
                    "data",
                    Map.of(
                            "answer",
                            "AI system working successfully. Question received: "
                                    + question,

                            "insights",
                            List.of(
                                    "Fallback mode active",
                                    "Python AI temporarily unavailable"
                            )
                    )
            );

            response.put(
                    "message",
                    "Fallback response returned successfully"
            );

            return ResponseEntity.ok(response);

        } catch (Exception e) {

            logger.error(
                    "Internal server error",
                    e
            );

            response.put("status", "error");

            response.put(
                    "message",
                    "Internal server error occurred"
            );

            return ResponseEntity
                    .status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(response);
        }
    }

    // ==========================================
    // DASHBOARD ENDPOINT
    // ==========================================
    @GetMapping("/dashboard")
    public ResponseEntity<Map<String, Object>> getDashboardData() {

        logger.info("=== DASHBOARD REQUEST ===");

        Map<String, Object> mockData =
                new HashMap<>();

        mockData.put(
                "monthlySales",
                List.of(
                        Map.of(
                                "month", "2024-01",
                                "revenue", 75000
                        ),
                        Map.of(
                                "month", "2024-02",
                                "revenue", 82000
                        )
                )
        );

        mockData.put(
                "regionSales",
                List.of(
                        Map.of(
                                "region", "North",
                                "revenue", 125000
                        ),
                        Map.of(
                                "region", "South",
                                "revenue", 89000
                        )
                )
        );

        mockData.put(
                "productSales",
                List.of(
                        Map.of(
                                "product", "Laptop",
                                "revenue", 185000
                        ),
                        Map.of(
                                "product", "Phone",
                                "revenue", 125000
                        )
                )
        );

        Map<String, Object> response =
                new HashMap<>();

        response.put("status", "success");
        response.put("data", mockData);
        response.put(
                "message",
                "Dashboard data retrieved successfully"
        );

        return ResponseEntity.ok(response);
    }

    // ==========================================
    // INSIGHTS ENDPOINT
    // ==========================================
    @GetMapping("/insights")
    public ResponseEntity<Map<String, Object>> getInsights() {

        Map<String, Object> response =
                new HashMap<>();

        response.put("status", "success");

        response.put(
                "data",
                Map.of(
                        "type", "sales_drop",
                        "message", "Sales decreased by 15%",
                        "value", -15
                )
        );

        response.put(
                "message",
                "Insights retrieved successfully"
        );

        return ResponseEntity.ok(response);
    }

    // ==========================================
    // ALERTS ENDPOINT
    // ==========================================
    @GetMapping("/alerts")
    public ResponseEntity<Map<String, Object>> getAlerts() {

        Map<String, Object> response =
                new HashMap<>();

        response.put("status", "success");

        response.put(
                "data",
                Map.of(
                        "title", "Low Inventory Alert",
                        "message", "Laptop inventory running low",
                        "priority", "medium"
                )
        );

        response.put(
                "message",
                "Alerts retrieved successfully"
        );

        return ResponseEntity.ok(response);
    }
}