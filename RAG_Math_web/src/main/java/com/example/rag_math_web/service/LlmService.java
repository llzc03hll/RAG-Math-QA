package com.example.rag_math_web.service;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import java.util.Map;
import java.util.HashMap;
import java.util.List;

// 这个类是用来调用llm服务的
@Service
@RequiredArgsConstructor
public class LlmService {
    
    @Value("${llm.service.url}")
    private String llmServiceUrl;
    
    private final RestTemplate restTemplate;
    
    public Map<String, Object> askQuestion(String question, List<String> context) {
        String url = llmServiceUrl + "/ask";
        
        Map<String, Object> request = new HashMap<>();
        request.put("question", question);
        request.put("context", context);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);
        
        return restTemplate.postForObject(url, entity, Map.class);
    }
    
    public double[] getEmbedding(String text) {
        String url = llmServiceUrl + "/embed";
        
        Map<String, String> request = new HashMap<>();
        request.put("text", text);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        HttpEntity<Map<String, String>> entity = new HttpEntity<>(request, headers);
        
        Map<String, List<Double>> response = restTemplate.postForObject(url, entity, Map.class);
        List<Double> embeddingList = response.get("embedding");
        
        return embeddingList.stream().mapToDouble(Double::doubleValue).toArray();
    }
} 