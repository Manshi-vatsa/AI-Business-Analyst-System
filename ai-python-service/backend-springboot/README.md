# AI Analytics Backend

A Spring Boot application for managing sales data with MySQL database integration and query processing capabilities.

## Project Structure

```
backend-springboot/
src/main/java/com/ai/analytics/
    entity/
        Sales.java              # JPA Entity
    repository/
        SalesRepository.java    # JPA Repository
    service/
        SalesService.java       # Business Logic Layer
    controller/
        SalesController.java    # REST API for Sales
        QueryController.java    # Query Processing API
    AiAnalyticsApplication.java # Main Spring Boot Application
src/main/resources/
    application.properties      # Database Configuration
pom.xml                        # Maven Dependencies
```

## Database Configuration

- **Database**: MySQL
- **Host**: localhost:3306
- **Database Name**: ai_analytics
- **Username**: root
- **Password**: root (configurable in application.properties)

## API Endpoints

### Sales Management
- `GET /api/sales` - Get all sales records
- `GET /api/sales/{id}` - Get sales by ID
- `POST /api/sales` - Create new sales record
- `PUT /api/sales/{id}` - Update existing sales record
- `DELETE /api/sales/{id}` - Delete sales record

### Sales Queries
- `GET /api/sales/product/{product}` - Get sales by product
- `GET /api/sales/region/{region}` - Get sales by region
- `GET /api/sales/date-range?startDate&endDate` - Get sales by date range
- `GET /api/sales/product-region/{product}/{region}` - Get sales by product and region
- `GET /api/sales/revenue-greater/{amount}` - Get sales with revenue greater than amount
- `GET /api/sales/stats/total-count` - Get total sales count

### Query Processing
- `POST /api/query` - Process natural language queries

## Entity Schema

**Sales Entity Fields:**
- `id` (Long) - Auto-generated primary key
- `product` (String) - Product name (required)
- `region` (String) - Region name (required)
- `revenue` (BigDecimal) - Revenue amount (required, positive)
- `date` (LocalDate) - Sales date (required)

## Query Examples

Send POST requests to `/api/query` with JSON body:

```json
{
  "question": "total sales"
}
```

```json
{
  "question": "total revenue for product laptop"
}
```

```json
{
  "question": "count sales by region north"
}
```

## Running the Application

1. Ensure MySQL is running and the `ai_analytics` database exists
2. Update database credentials in `application.properties` if needed
3. Run the application:
   ```bash
   mvn spring-boot:run
   ```
4. The application will start on `http://localhost:8080`

## Technologies Used

- Spring Boot 3.2.5
- Spring Data JPA
- MySQL Connector/J
- Maven
- Java 17

## Database Setup

Create the MySQL database:
```sql
CREATE DATABASE ai_analytics;
```

The application will automatically create the `sales` table using JPA DDL auto-update.
