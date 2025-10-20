package com.studysync.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MajorStatsResponse {
    private String major;
    private Integer totalClasses;
    private Integer totalUsers;
    private Double averageDifficulty;
}
