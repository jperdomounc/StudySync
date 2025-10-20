package com.studysync.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class ClassDifficultyRequest {
    @NotBlank(message = "Class code is required")
    @Pattern(regexp = "^[A-Z]{2,4}\\s+\\d{3,4}[A-Z]?$",
            message = "Class code must be in format like 'COMP 550' or 'MATH 231'")
    private String classCode;

    @NotBlank(message = "Class name is required")
    @Size(max = 200, message = "Class name too long (max 200 characters)")
    private String className;

    @NotBlank(message = "Major is required")
    private String major;

    @NotNull(message = "Difficulty rating is required")
    @Min(value = 1, message = "Difficulty rating must be between 1 and 10")
    @Max(value = 10, message = "Difficulty rating must be between 1 and 10")
    private Integer difficultyRating;

    @NotBlank(message = "Professor name is required")
    @Size(max = 100, message = "Professor name too long (max 100 characters)")
    private String professor;

    @NotBlank(message = "Semester is required")
    @Pattern(regexp = "^(Fall|Spring|Summer)\\s+\\d{4}$",
            message = "Semester must be in format like 'Fall 2024'")
    private String semester;
}
