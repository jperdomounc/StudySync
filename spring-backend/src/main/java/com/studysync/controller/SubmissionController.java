package com.studysync.controller;

import com.studysync.dto.ClassDifficultyRequest;
import com.studysync.dto.ProfessorRatingRequest;
import com.studysync.service.RatingService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/submissions")
public class SubmissionController {

    @Autowired
    private RatingService ratingService;

    @PostMapping("/difficulty")
    public ResponseEntity<Map<String, String>> submitClassDifficulty(
            @Valid @RequestBody ClassDifficultyRequest request,
            Authentication authentication) {
        try {
            String userId = (String) authentication.getPrincipal();
            ratingService.submitClassDifficulty(request, userId);
            return ResponseEntity.ok(Map.of("message", "Difficulty rating submitted successfully"));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body(Map.of("error", "Failed to submit rating"));
        }
    }

    @PostMapping("/professor")
    public ResponseEntity<Map<String, String>> submitProfessorRating(
            @Valid @RequestBody ProfessorRatingRequest request,
            Authentication authentication) {
        try {
            String userId = (String) authentication.getPrincipal();
            ratingService.submitProfessorRating(request, userId);
            return ResponseEntity.ok(Map.of("message", "Professor rating submitted successfully"));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body(Map.of("error", "Failed to submit rating"));
        }
    }
}
