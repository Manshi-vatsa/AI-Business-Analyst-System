package com.ai.analytics.repository;

import com.ai.analytics.entity.Sales;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Repository
public interface SalesRepository extends JpaRepository<Sales, Long> {
    
    // Find sales by product
    List<Sales> findByProduct(String product);
    
    // Find sales by region
    List<Sales> findByRegion(String region);
    
    // Find sales by date range
    List<Sales> findByDateBetween(LocalDate startDate, LocalDate endDate);
    
    // Find sales by product and region
    List<Sales> findByProductAndRegion(String product, String region);
    
    // Find sales with revenue greater than specified amount
    List<Sales> findByRevenueGreaterThan(BigDecimal revenue);
    
    // Get total revenue by product
    @Query("SELECT SUM(s.revenue) FROM Sales s WHERE s.product = :product")
    BigDecimal getTotalRevenueByProduct(@Param("product") String product);
    
    // Get total revenue by region
    @Query("SELECT SUM(s.revenue) FROM Sales s WHERE s.region = :region")
    BigDecimal getTotalRevenueByRegion(@Param("region") String region);
    
    // Get total revenue by date range
    @Query("SELECT SUM(s.revenue) FROM Sales s WHERE s.date BETWEEN :startDate AND :endDate")
    BigDecimal getTotalRevenueByDateRange(@Param("startDate") LocalDate startDate, 
                                        @Param("endDate") LocalDate endDate);
    
    // Count sales by product
    @Query("SELECT COUNT(s) FROM Sales s WHERE s.product = :product")
    Long countSalesByProduct(@Param("product") String product);
    
    // Count sales by region
    @Query("SELECT COUNT(s) FROM Sales s WHERE s.region = :region")
    Long countSalesByRegion(@Param("region") String region);
}
