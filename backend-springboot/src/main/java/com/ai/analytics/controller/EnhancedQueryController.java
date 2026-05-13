package com.ai.analytics.controller;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.ResourceAccessException;

import java.util.HashMap;
import java.util.Map;
import java.time.Duration;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
@RequestMapping("/ai")
public class EnhancedQueryController {

    private static final Logger logger =
            LoggerFactory.getLogger(EnhancedQueryController.class);

    private static final String FASTAPI_BASE_URL =
            System.getenv().getOrDefault(
                    "FASTAPI_URL",
                    "http://localhost:8000"
            );

    private static final String FASTAPI_QUERY_ENDPOINT =
            FASTAPI_BASE_URL + "/ai/query";

    private static final int REQUEST_TIMEOUT_SECONDS = 30;

    private final RestTemplate restTemplate;

    @Autowired
    public EnhancedQueryController() {

        SimpleClientHttpRequestFactory factory =
                new SimpleClientHttpRequestFactory();

        factory.setConnectTimeout(
                (int) Duration.ofSeconds(10).toMillis()
        );

        factory.setReadTimeout(
                (int) Duration.ofSeconds(REQUEST_TIMEOUT_SECONDS).toMillis()
        );

        this.restTemplate = new RestTemplate(factory);
    }

    @PostMapping(
            value = "/query",
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    public ResponseEntity<Map<String, Object>> processQuery(
            @RequestBody Map<String, String> request
    ) {

        logger.info("=== SPRING BOOT QUERY START ===");

        try {

            String question = request.get("question");

            logger.info("Question = {}", question);

            if (question == null || question.trim().isEmpty()) {

                return createErrorResponse(
                        "Question is required",
                        HttpStatus.BAD_REQUEST
                );
            }

            // Send request to FastAPI
            Map<String, String> pythonRequest = new HashMap<>();
            pythonRequest.put("question", question);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, String>> entity =
                    new HttpEntity<>(pythonRequest, headers);

            logger.info("Calling FastAPI: {}", FASTAPI_QUERY_ENDPOINT);

            ResponseEntity<Map<String, Object>> pythonResponse =
                    restTemplate.exchange(
                            FASTAPI_QUERY_ENDPOINT,
                            HttpMethod.POST,
                            entity,
                            new ParameterizedTypeReference<Map<String, Object>>() {}
                    );

            logger.info("FastAPI Status = {}", pythonResponse.getStatusCode());

            Map<String, Object> pythonBody =
                    pythonResponse.getBody();

            logger.info("FastAPI Body = {}", pythonBody);

            if (pythonBody == null) {

                return createErrorResponse(
                        "FastAPI returned empty body",
                        HttpStatus.INTERNAL_SERVER_ERROR
                );
            }

            /*
             FASTAPI RETURNS:

             {
               "status":"success",
               "data":{
                  "answer":"..."
               }
             }

             OR DIRECT:

             {
                "answer":"..."
             }
            */

            Map<String, Object> finalData;

            // CASE 1 -> Wrapped response
            if (
                    pythonBody.containsKey("status")
                            && pythonBody.containsKey("data")
            ) {

                Object dataObj = pythonBody.get("data");

                if (!(dataObj instanceof Map)) {

                    return createErrorResponse(
                            "Invalid FastAPI data structure",
                            HttpStatus.INTERNAL_SERVER_ERROR
                    );
                }

                finalData = (Map<String, Object>) dataObj;
            }

            // CASE 2 -> Direct response
            else {

                finalData = pythonBody;
            }

            logger.info("FINAL DATA = {}", finalData);

            // FINAL RESPONSE FOR ANDROID
            Map<String, Object> finalResponse = new HashMap<>();

            finalResponse.put("status", "success");
            finalResponse.put("data", finalData);
            finalResponse.put(
                    "message",
                    "Query processed successfully"
            );

            logger.info("FINAL RESPONSE SENT TO ANDROID = {}", finalResponse);

            return ResponseEntity.ok(finalResponse);

        } catch (ResourceAccessException e) {

            logger.error("FastAPI connection failed", e);

            return createErrorResponse(
                    "FastAPI unreachable: " + e.getMessage(),
                    HttpStatus.SERVICE_UNAVAILABLE
            );

        } catch (Exception e) {

            logger.error("Controller exception", e);

            return createErrorResponse(
                    "Internal server error: " + e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {

        Map<String, Object> response = new HashMap<>();

        response.put("status", "healthy");
        response.put("springboot", true);
        response.put("fastapi_url", FASTAPI_BASE_URL);

        return ResponseEntity.ok(response);
    }

    private ResponseEntity<Map<String, Object>> createErrorResponse(
            String message,
            HttpStatus status
    ) {

        Map<String, Object> error = new HashMap<>();

        error.put("status", "error");
        error.put("message", message);

        return ResponseEntity
                .status(status)
                .body(error);
    }
}