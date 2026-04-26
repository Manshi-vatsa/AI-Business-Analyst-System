# 📋 FINAL WORKING JSON STRUCTURE

## 🎯 COMPLETE API RESPONSE STRUCTURES

### **1. Dashboard API Response**
```json
{
  "status": "success",
  "data": {
    "monthlySales": [
      {
        "month": "2024-01",
        "revenue": 75000.0
      },
      {
        "month": "2024-02",
        "revenue": 82000.0
      },
      {
        "month": "2024-03",
        "revenue": 68000.0
      }
    ],
    "regionSales": [
      {
        "region": "North",
        "revenue": 125000.0,
        "percentage": 35.0
      },
      {
        "region": "South",
        "revenue": 89000.0,
        "percentage": 25.0
      },
      {
        "region": "East",
        "revenue": 71000.0,
        "percentage": 20.0
      },
      {
        "region": "West",
        "revenue": 71000.0,
        "percentage": 20.0
      }
    ],
    "productSales": [
      {
        "product": "Laptop",
        "revenue": 185000.0,
        "quantity": 185
      },
      {
        "product": "Phone",
        "revenue": 125000.0,
        "quantity": 250
      },
      {
        "product": "Tablet",
        "revenue": 56000.0,
        "quantity": 112
      }
    ]
  },
  "message": "Dashboard data retrieved successfully",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **2. Query API Response**
```json
{
  "status": "success",
  "data": {
    "answer": "Total sales revenue across all regions is $356,000.00 with 547 transactions recorded.",
    "insights": [
      "North region generated the highest revenue at $125,000",
      "Laptop is the top-selling product with $185,000 in revenue",
      "Sales increased by 15% compared to previous month"
    ],
    "sql_query": "SELECT SUM(revenue) as total_revenue, COUNT(*) as total_transactions FROM sales",
    "results": [
      {
        "id": 1,
        "product": "Laptop",
        "quantity": 25,
        "revenue": 125000.0,
        "date": "2024-01-15",
        "region": "North"
      },
      {
        "id": 2,
        "product": "Phone",
        "quantity": 35,
        "revenue": 70000.0,
        "date": "2024-01-16",
        "region": "South"
      }
    ]
  },
  "message": "Query processed successfully through multi-agent pipeline",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **3. Insights API Response**
```json
{
  "status": "success",
  "data": [
    {
      "type": "drop",
      "message": "Sales decreased by 15% this week",
      "value": -15.0,
      "category": "sales",
      "timestamp": "2024-01-23T15:45:00Z"
    },
    {
      "type": "increase",
      "message": "North region showed 20% growth",
      "value": 20.0,
      "category": "region",
      "timestamp": "2024-01-23T15:45:00Z"
    },
    {
      "type": "alert",
      "message": "Phone inventory running low",
      "value": 5.0,
      "category": "inventory",
      "timestamp": "2024-01-23T15:45:00Z"
    }
  ],
  "message": "Insights retrieved successfully",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **4. Alerts API Response**
```json
{
  "status": "success",
  "data": [
    {
      "title": "Low Inventory Alert",
      "message": "Laptop inventory running low",
      "priority": "medium",
      "timestamp": "2024-01-23T15:45:00Z"
    },
    {
      "title": "Sales Drop Alert",
      "message": "Sales decreased by 15% compared to last week",
      "priority": "high",
      "timestamp": "2024-01-23T15:45:00Z"
    },
    {
      "title": "Regional Performance Alert",
      "message": "South region underperforming by 10%",
      "priority": "low",
      "timestamp": "2024-01-23T15:45:00Z"
    }
  ],
  "message": "Alerts retrieved successfully",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **5. Health Check Response**
```json
{
  "status": "healthy",
  "service": "AI Business Analyst Service",
  "message": "Service is running normally",
  "timestamp": "2024-01-23T15:45:00Z",
  "version": "1.0.0",
  "database": "connected",
  "memory_usage": "45%",
  "cpu_usage": "12%"
}
```

## 🔧 ERROR RESPONSE STRUCTURES

### **1. Validation Error**
```json
{
  "status": "error",
  "error": "Validation failed",
  "details": "Question is required and cannot be empty",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **2. Database Error**
```json
{
  "status": "error",
  "error": "Database connection failed",
  "details": "Unable to connect to MySQL database",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **3. Service Unavailable**
```json
{
  "status": "error",
  "error": "Service unavailable",
  "details": "Python FastAPI service is not responding",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

## 📱 ANDROID EXPECTED RESPONSES

### **1. Dashboard Data Model**
```kotlin
data class DashboardResponse(
    val status: String,
    val data: DashboardData,
    val message: String,
    val timestamp: String
)

data class DashboardData(
    val monthlySales: List<MonthlySale>,
    val regionSales: List<RegionSale>,
    val productSales: List<ProductSale>
)

data class MonthlySale(
    val month: String,
    val revenue: Double
)

data class RegionSale(
    val region: String,
    val revenue: Double,
    val percentage: Double
)

data class ProductSale(
    val product: String,
    val revenue: Double,
    val quantity: Int
)
```

### **2. Query Response Model**
```kotlin
data class QueryResponse(
    val status: String,
    val data: QueryData,
    val message: String,
    val timestamp: String
)

data class QueryData(
    val answer: String,
    val insights: List<String>,
    val sql_query: String,
    val results: List<SalesRecord>
)

data class SalesRecord(
    val id: Int,
    val product: String,
    val quantity: Int,
    val revenue: Double,
    val date: String,
    val region: String
)
```

## 🔄 SPRING BOOT TO PYTHON FLOW

### **1. Request Flow**
```
Android App → Spring Boot (8080) → Python FastAPI (8000) → MySQL (3306)
```

### **2. Response Flow**
```
MySQL → Python FastAPI → Spring Boot → Android App
```

### **3. Data Transformation**
```
MySQL Raw Data → Python Processing → JSON Response → Spring Boot Proxy → Android Parsing
```

## 🎯 FIELD NAME CONSISTENCY

### **Database → Python → Spring Boot → Android**
| Database | Python | Spring Boot | Android |
|-----------|--------|-------------|---------|
| `type` | `type` | `type` | `type` |
| `date` | `date` | `date` | `date` |
| `revenue` | `revenue` | `revenue` | `revenue` |
| `region` | `region` | `region` | `region` |
| `product` | `product` | `product` | `product` |

### **JSON Field Naming Convention**
- ✅ **camelCase**: `monthlySales`, `regionSales`, `productSales`
- ✅ **snake_case**: `sql_query` (only in query response)
- ✅ **Consistent**: All timestamps use `timestamp` field

## 📊 RESPONSE VALIDATION

### **Required Fields for Each Response**
```json
// Dashboard Response
{
  "status": "required",
  "data": {
    "monthlySales": "required",
    "regionSales": "required", 
    "productSales": "required"
  },
  "message": "required",
  "timestamp": "required"
}

// Query Response
{
  "status": "required",
  "data": {
    "answer": "required",
    "insights": "required",
    "sql_query": "optional",
    "results": "optional"
  },
  "message": "required",
  "timestamp": "required"
}

// Insights Response
{
  "status": "required",
  "data": [
    {
      "type": "required",
      "message": "required",
      "value": "optional",
      "category": "required",
      "timestamp": "required"
    }
  ],
  "message": "required",
  "timestamp": "required"
}
```

## 🚀 TESTING COMMANDS

### **Test All Endpoints**
```bash
# Dashboard
curl http://localhost:8000/ai/dashboard | python -m json.tool

# Query
curl -X POST http://localhost:8000/ai/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What are total sales?"}' | python -m json.tool

# Insights
curl http://localhost:8000/ai/insights | python -m json.tool

# Alerts
curl http://localhost:8000/ai/alerts | python -m json.tool

# Health
curl http://localhost:8000/health | python -m json.tool
```

### **Validate JSON Structure**
```bash
# Check field names
curl http://localhost:8000/ai/dashboard | jq 'keys'
curl http://localhost:8000/ai/dashboard | jq '.data | keys'

# Check data types
curl http://localhost:8000/ai/dashboard | jq '.data.monthlySales | type'
curl http://localhost:8000/ai/dashboard | jq '.data.monthlySales[0] | keys'
```

**🎉 This is the complete, working JSON structure that your entire system should use!**
