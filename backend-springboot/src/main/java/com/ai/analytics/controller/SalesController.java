package com.ai.analytics.controller;

import com.ai.analytics.entity.Sales;
import com.ai.analytics.service.SalesService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/sales")
@CrossOrigin(origins = "*")
public class SalesController {
    
    private final SalesService salesService;
    
    @Autowired
    public SalesController(SalesService salesService) {
        this.salesService = salesService;
    }
    
    // GET /api/sales - Get all sales
    @GetMapping
    public ResponseEntity<List<Sales>> getAllSales() {
        List<Sales> sales = salesService.getAllSales();
        return ResponseEntity.ok(sales);
    }
    
    // GET /api/sales/{id} - Get sales by ID
    @GetMapping("/{id}")
    public ResponseEntity<Sales> getSalesById(@PathVariable Long id) {
        Optional<Sales> sales = salesService.getSalesById(id);
        return sales.map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    // POST /api/sales - Create new sales
    @PostMapping
    public ResponseEntity<Sales> createSales(@Valid @RequestBody Sales sales) {
        Sales createdSales = salesService.createSales(sales);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdSales);
    }
    
    // PUT /api/sales/{id} - Update sales
    @PutMapping("/{id}")
    public ResponseEntity<Sales> updateSales(@PathVariable Long id, @Valid @RequestBody Sales salesDetails) {
        Sales updatedSales = salesService.updateSales(id, salesDetails);
        if (updatedSales != null) {
            return ResponseEntity.ok(updatedSales);
        }
        return ResponseEntity.notFound().build();
    }
    
    // DELETE /api/sales/{id} - Delete sales
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteSales(@PathVariable Long id) {
        boolean deleted = salesService.deleteSales(id);
        if (deleted) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }
    
    // GET /api/sales/product/{product} - Get sales by product
    @GetMapping("/product/{product}")
    public ResponseEntity<List<Sales>> getSalesByProduct(@PathVariable String product) {
        List<Sales> sales = salesService.getSalesByProduct(product);
        return ResponseEntity.ok(sales);
    }
    
    // GET /api/sales/region/{region} - Get sales by region
    @GetMapping("/region/{region}")
    public ResponseEntity<List<Sales>> getSalesByRegion(@PathVariable String region) {
        List<Sales> sales = salesService.getSalesByRegion(region);
        return ResponseEntity.ok(sales);
    }
    
    // GET /api/sales/date-range - Get sales by date range
    @GetMapping("/date-range")
    public ResponseEntity<List<Sales>> getSalesByDateRange(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        List<Sales> sales = salesService.getSalesByDateRange(startDate, endDate);
        return ResponseEntity.ok(sales);
    }
    
    // GET /api/sales/product-region/{product}/{region} - Get sales by product and region
    @GetMapping("/product-region/{product}/{region}")
    public ResponseEntity<List<Sales>> getSalesByProductAndRegion(
            @PathVariable String product, @PathVariable String region) {
        List<Sales> sales = salesService.getSalesByProductAndRegion(product, region);
        return ResponseEntity.ok(sales);
    }
    
    // GET /api/sales/revenue-greater/{amount} - Get sales with revenue greater than amount
    @GetMapping("/revenue-greater/{amount}")
    public ResponseEntity<List<Sales>> getSalesWithRevenueGreaterThan(@PathVariable BigDecimal amount) {
        List<Sales> sales = salesService.getSalesWithRevenueGreaterThan(amount);
        return ResponseEntity.ok(sales);
    }
    
    // GET /api/sales/stats/total-count - Get total sales count
    @GetMapping("/stats/total-count")
    public ResponseEntity<Long> getTotalSalesCount() {
        long count = salesService.getTotalSalesCount();
        return ResponseEntity.ok(count);
    }
}
