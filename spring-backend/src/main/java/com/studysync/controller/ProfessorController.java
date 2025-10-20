package com.studysync.controller;

import com.studysync.model.ProfessorRating;
import com.studysync.service.RatingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/professors")
public class ProfessorController {

    @Autowired
    private RatingService ratingService;

    @GetMapping("/{professor}/ratings")
    public ResponseEntity<Map<String, Object>> getProfessorRatings(
            @PathVariable String professor,
            @RequestParam(required = false) String classCode) {
        try {
            List<ProfessorRating> ratings = ratingService.getProfessorRatings(professor, classCode);
            return ResponseEntity.ok(Map.of(
                    "professor", professor,
                    "classCode", classCode != null ? classCode : "",
                    "ratings", ratings
            ));
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}
