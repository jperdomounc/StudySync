package com.studysync.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class ProfessorRatingRequest {
    @NotBlank(message = "Professor name is required")
    @Size(max = 100, message = "Professor name too long")
    private String professor;

    @NotBlank(message = "Class code is required")
    private String classCode;

    @NotNull(message = "Rating is required")
    @DecimalMin(value = "1.0", message = "Rating must be between 1.0 and 5.0")
    @DecimalMax(value = "5.0", message = "Rating must be between 1.0 and 5.0")
    private Double rating;

    @Size(max = 1000, message = "Review too long (max 1000 characters)")
    private String review;

    @NotBlank(message = "Major is required")
    private String major;

    @NotBlank(message = "Semester is required")
    @Pattern(regexp = "^(Fall|Spring|Summer)\\s+\\d{4}$",
            message = "Semester must be in format like 'Fall 2024'")
    private String semester;
}
