package com.ai.analytics.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "sales")
public class Sales {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "Product name is required")
    @Column(name = "product", nullable = false, length = 255)
    private String product;
    
    @NotBlank(message = "Region is required")
    @Column(name = "region", nullable = false, length = 100)
    private String region;
    
    @NotNull(message = "Revenue is required")
    @Positive(message = "Revenue must be positive")
    @Column(name = "revenue", nullable = false, precision = 19, scale = 2)
    private BigDecimal revenue;
    
    @NotNull(message = "Date is required")
    @Column(name = "date", nullable = false)
    private LocalDate date;
    
    // Default constructor
    public Sales() {}
    
    // Constructor with fields
    public Sales(String product, String region, BigDecimal revenue, LocalDate date) {
        this.product = product;
        this.region = region;
        this.revenue = revenue;
        this.date = date;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getProduct() {
        return product;
    }
    
    public void setProduct(String product) {
        this.product = product;
    }
    
    public String getRegion() {
        return region;
    }
    
    public void setRegion(String region) {
        this.region = region;
    }
    
    public BigDecimal getRevenue() {
        return revenue;
    }
    
    public void setRevenue(BigDecimal revenue) {
        this.revenue = revenue;
    }
    
    public LocalDate getDate() {
        return date;
    }
    
    public void setDate(LocalDate date) {
        this.date = date;
    }
    
    @Override
    public String toString() {
        return "Sales{" +
                "id=" + id +
                ", product='" + product + '\'' +
                ", region='" + region + '\'' +
                ", revenue=" + revenue +
                ", date=" + date +
                '}';
    }
}
