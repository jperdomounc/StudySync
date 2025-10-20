package com.studysync.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.Map;

@RestController
public class HealthController {

    @Autowired
    private MongoTemplate mongoTemplate;

    @Value("${app.environment}")
    private String environment;

    @GetMapping("/")
    public ResponseEntity<Map<String, Object>> root() {
        return ResponseEntity.ok(Map.of(
                "message", "StudySync API v2.0 - UNC Class Rating System",
                "status", "active",
                "timestamp", LocalDateTime.now()
        ));
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        try {
            // Test MongoDB connection
            mongoTemplate.getDb().runCommand(new org.bson.Document("ping", 1));

            return ResponseEntity.ok(Map.of(
                    "status", "healthy",
                    "timestamp", LocalDateTime.now(),
                    "version", "2.0.0",
                    "environment", environment,
                    "database", Map.of(
                            "status", "healthy",
                            "name", mongoTemplate.getDb().getName()
                    ),
                    "services", Map.of(
                            "auth", "operational",
                            "ratings", "operational"
                    )
            ));
        } catch (Exception e) {
            return ResponseEntity.status(503).body(Map.of(
                    "status", "unhealthy",
                    "error", e.getMessage(),
                    "timestamp", LocalDateTime.now()
            ));
        }
    }
}
