package com.ai.analytics.model;

import java.util.Map;

public class DashboardData {
    private double totalSales;
    private Map<String, Object> regionData;
    private String topProduct;
    
    public DashboardData() {}
    
    public DashboardData(double totalSales, Map<String, Object> regionData, String topProduct) {
        this.totalSales = totalSales;
        this.regionData = regionData;
        this.topProduct = topProduct;
    }
    
    public double getTotalSales() {
        return totalSales;
    }
    
    public void setTotalSales(double totalSales) {
        this.totalSales = totalSales;
    }
    
    public Map<String, Object> getRegionData() {
        return regionData;
    }
    
    public void setRegionData(Map<String, Object> regionData) {
        this.regionData = regionData;
    }
    
    public String getTopProduct() {
        return topProduct;
    }
    
    public void setTopProduct(String topProduct) {
        this.topProduct = topProduct;
    }
}
