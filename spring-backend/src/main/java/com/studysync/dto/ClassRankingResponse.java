package com.studysync.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ClassRankingResponse {
    private String classCode;
    private String className;
    private String major;
    private Double averageDifficulty;
    private Integer totalSubmissions;
    private List<ProfessorStats> professors;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ProfessorStats {
        private String name;
        private Double avgRating;
        private Integer ratingCount;
    }
}
