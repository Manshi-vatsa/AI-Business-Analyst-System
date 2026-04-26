package com.ai.analytics.service;

import com.ai.analytics.entity.Sales;
import com.ai.analytics.repository.SalesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class SalesService {
    
    private final SalesRepository salesRepository;
    
    @Autowired
    public SalesService(SalesRepository salesRepository) {
        this.salesRepository = salesRepository;
    }
    
    // Get all sales
    public List<Sales> getAllSales() {
        return salesRepository.findAll();
    }
    
    // Get sales by ID
    public Optional<Sales> getSalesById(Long id) {
        return salesRepository.findById(id);
    }
    
    // Create new sales record
    public Sales createSales(Sales sales) {
        return salesRepository.save(sales);
    }
    
    // Update existing sales record
    public Sales updateSales(Long id, Sales salesDetails) {
        Optional<Sales> existingSales = salesRepository.findById(id);
        if (existingSales.isPresent()) {
            Sales sales = existingSales.get();
            sales.setProduct(salesDetails.getProduct());
            sales.setRegion(salesDetails.getRegion());
            sales.setRevenue(salesDetails.getRevenue());
            sales.setDate(salesDetails.getDate());
            return salesRepository.save(sales);
        }
        return null;
    }
    
    // Delete sales record
    public boolean deleteSales(Long id) {
        if (salesRepository.existsById(id)) {
            salesRepository.deleteById(id);
            return true;
        }
        return false;
    }
    
    // Get sales by product
    public List<Sales> getSalesByProduct(String product) {
        return salesRepository.findByProduct(product);
    }
    
    // Get sales by region
    public List<Sales> getSalesByRegion(String region) {
        return salesRepository.findByRegion(region);
    }
    
    // Get sales by date range
    public List<Sales> getSalesByDateRange(LocalDate startDate, LocalDate endDate) {
        return salesRepository.findByDateBetween(startDate, endDate);
    }
    
    // Get sales by product and region
    public List<Sales> getSalesByProductAndRegion(String product, String region) {
        return salesRepository.findByProductAndRegion(product, region);
    }
    
    // Get sales with revenue greater than specified amount
    public List<Sales> getSalesWithRevenueGreaterThan(BigDecimal revenue) {
        return salesRepository.findByRevenueGreaterThan(revenue);
    }
    
    // Get total revenue by product
    public BigDecimal getTotalRevenueByProduct(String product) {
        BigDecimal total = salesRepository.getTotalRevenueByProduct(product);
        return total != null ? total : BigDecimal.ZERO;
    }
    
    // Get total revenue by region
    public BigDecimal getTotalRevenueByRegion(String region) {
        BigDecimal total = salesRepository.getTotalRevenueByRegion(region);
        return total != null ? total : BigDecimal.ZERO;
    }
    
    // Get total revenue by date range
    public BigDecimal getTotalRevenueByDateRange(LocalDate startDate, LocalDate endDate) {
        BigDecimal total = salesRepository.getTotalRevenueByDateRange(startDate, endDate);
        return total != null ? total : BigDecimal.ZERO;
    }
    
    // Count sales by product
    public Long countSalesByProduct(String product) {
        return salesRepository.countSalesByProduct(product);
    }
    
    // Count sales by region
    public Long countSalesByRegion(String region) {
        return salesRepository.countSalesByRegion(region);
    }
    
    // Get total number of sales records
    public long getTotalSalesCount() {
        return salesRepository.count();
    }
}
