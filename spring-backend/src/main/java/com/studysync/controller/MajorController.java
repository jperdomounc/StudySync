package com.studysync.controller;

import com.studysync.dto.ClassRankingResponse;
import com.studysync.dto.MajorStatsResponse;
import com.studysync.service.RatingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/majors")
public class MajorController {

    @Autowired
    private RatingService ratingService;

    @GetMapping
    public ResponseEntity<List<String>> getAllMajors() {
        try {
            List<String> majors = ratingService.getAllMajors();
            return ResponseEntity.ok(majors);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/{major}/stats")
    public ResponseEntity<MajorStatsResponse> getMajorStats(@PathVariable String major) {
        try {
            MajorStatsResponse stats = ratingService.getMajorStats(major);
            return ResponseEntity.ok(stats);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/{major}/classes")
    public ResponseEntity<List<ClassRankingResponse>> getClassRankings(
            @PathVariable String major,
            @RequestParam(defaultValue = "50") int limit) {
        try {
            List<ClassRankingResponse> rankings = ratingService.getClassRankings(major, limit);
            return ResponseEntity.ok(rankings);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}
