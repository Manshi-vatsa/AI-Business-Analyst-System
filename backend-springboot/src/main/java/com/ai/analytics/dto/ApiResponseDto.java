package com.ai.analytics.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.util.Map;

/**
 * API Response DTO matching Python FastAPI JSON structure
 */
public class ApiResponseDto {
    
    private String status;
    private String message;
    private Object data;
    private String timestamp;
    
    // Constructors
    public ApiResponseDto() {}
    
    public ApiResponseDto(String status, String message, Object data) {
        this.status = status;
        this.message = message;
        this.data = data;
        this.timestamp = java.time.Instant.now().toString();
    }
    
    // Getters and Setters
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public Object getData() {
        return data;
    }
    
    public void setData(Object data) {
        this.data = data;
    }
    
    public String getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }
    
    /**
     * Dashboard Data DTO matching Python JSON structure
     */
    public static class DashboardDataDto {
        @JsonProperty("monthlySales")
        private List<Map<String, Object>> monthlySales;
        
        @JsonProperty("regionSales")
        private List<Map<String, Object>> regionSales;
        
        @JsonProperty("productSales")
        private List<Map<String, Object>> productSales;
        
        // Constructors
        public DashboardDataDto() {}
        
        public DashboardDataDto(List<Map<String, Object>> monthlySales, 
                               List<Map<String, Object>> regionSales, 
                               List<Map<String, Object>> productSales) {
            this.monthlySales = monthlySales;
            this.regionSales = regionSales;
            this.productSales = productSales;
        }
        
        // Getters and Setters
        public List<Map<String, Object>> getMonthlySales() {
            return monthlySales;
        }
        
        public void setMonthlySales(List<Map<String, Object>> monthlySales) {
            this.monthlySales = monthlySales;
        }
        
        public List<Map<String, Object>> getRegionSales() {
            return regionSales;
        }
        
        public void setRegionSales(List<Map<String, Object>> regionSales) {
            this.regionSales = regionSales;
        }
        
        public List<Map<String, Object>> getProductSales() {
            return productSales;
        }
        
        public void setProductSales(List<Map<String, Object>> productSales) {
            this.productSales = productSales;
        }
    }
    
    /**
     * Query Response DTO matching Python JSON structure
     */
    public static class QueryResponseDto {
        private String answer;
        private List<String> insights;
        
        @JsonProperty("sql_query")
        private String sqlQuery;
        
        private List<Map<String, Object>> results;
        
        // Constructors
        public QueryResponseDto() {}
        
        public QueryResponseDto(String answer, List<String> insights) {
            this.answer = answer;
            this.insights = insights;
        }
        
        // Getters and Setters
        public String getAnswer() {
            return answer;
        }
        
        public void setAnswer(String answer) {
            this.answer = answer;
        }
        
        public List<String> getInsights() {
            return insights;
        }
        
        public void setInsights(List<String> insights) {
            this.insights = insights;
        }
        
        public String getSqlQuery() {
            return sqlQuery;
        }
        
        public void setSqlQuery(String sqlQuery) {
            this.sqlQuery = sqlQuery;
        }
        
        public List<Map<String, Object>> getResults() {
            return results;
        }
        
        public void setResults(List<Map<String, Object>> results) {
            this.results = results;
        }
    }
    
    /**
     * Insight DTO matching Python JSON structure
     */
    public static class InsightDto {
        private String type;
        private String message;
        private Double value;
        private String category;
        private String timestamp;
        
        // Constructors
        public InsightDto() {}
        
        public InsightDto(String type, String message, Double value, String category) {
            this.type = type;
            this.message = message;
            this.value = value;
            this.category = category;
            this.timestamp = java.time.Instant.now().toString();
        }
        
        // Getters and Setters
        public String getType() {
            return type;
        }
        
        public void setType(String type) {
            this.type = type;
        }
        
        public String getMessage() {
            return message;
        }
        
        public void setMessage(String message) {
            this.message = message;
        }
        
        public Double getValue() {
            return value;
        }
        
        public void setValue(Double value) {
            this.value = value;
        }
        
        public String getCategory() {
            return category;
        }
        
        public void setCategory(String category) {
            this.category = category;
        }
        
        public String getTimestamp() {
            return timestamp;
        }
        
        public void setTimestamp(String timestamp) {
            this.timestamp = timestamp;
        }
    }
    
    /**
     * Alert DTO matching Python JSON structure
     */
    public static class AlertDto {
        private String title;
        private String message;
        private String priority;
        private String timestamp;
        
        // Constructors
        public AlertDto() {}
        
        public AlertDto(String title, String message, String priority) {
            this.title = title;
            this.message = message;
            this.priority = priority;
            this.timestamp = java.time.Instant.now().toString();
        }
        
        // Getters and Setters
        public String getTitle() {
            return title;
        }
        
        public void setTitle(String title) {
            this.title = title;
        }
        
        public String getMessage() {
            return message;
        }
        
        public void setMessage(String message) {
            this.message = message;
        }
        
        public String getPriority() {
            return priority;
        }
        
        public void setPriority(String priority) {
            this.priority = priority;
        }
        
        public String getTimestamp() {
            return timestamp;
        }
        
        public void setTimestamp(String timestamp) {
            this.timestamp = timestamp;
        }
    }
}
