package com.ai.analytics.service;

import com.ai.analytics.model.DashboardData;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class DashboardService {
    
    public DashboardData getDashboardData() {
        // In a real application, this would fetch data from a database
        // For now, we'll return sample data
        
        double totalSales = 120000.0;
        
        // Sample region data
        Map<String, Object> regionData = new HashMap<>();
        regionData.put("North America", 45000.0);
        regionData.put("Europe", 35000.0);
        regionData.put("Asia", 28000.0);
        regionData.put("Other", 12000.0);
        
        // Add percentage breakdown
        Map<String, Double> regionPercentages = new HashMap<>();
        regionPercentages.put("North America", 37.5);
        regionPercentages.put("Europe", 29.2);
        regionPercentages.put("Asia", 23.3);
        regionPercentages.put("Other", 10.0);
        regionData.put("percentages", regionPercentages);
        
        // Add growth data
        Map<String, Double> growthData = new HashMap<>();
        growthData.put("North America", 15.2);
        growthData.put("Europe", 8.7);
        growthData.put("Asia", 22.1);
        growthData.put("Other", 5.4);
        regionData.put("growth", growthData);
        
        String topProduct = "Laptop";
        
        return new DashboardData(totalSales, regionData, topProduct);
    }
}
