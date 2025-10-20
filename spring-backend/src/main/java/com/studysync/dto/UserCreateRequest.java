package com.studysync.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class UserCreateRequest {
    @NotBlank(message = "Email is required")
    @Email(message = "Must be a valid email")
    @Pattern(regexp = "^[a-zA-Z0-9._%+-]+@(unc\\.edu|live\\.unc\\.edu|ad\\.unc\\.edu)$",
            message = "Must use a valid UNC email address (@unc.edu, @live.unc.edu, or @ad.unc.edu)")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, max = 100, message = "Password must be between 8 and 100 characters")
    @Pattern(regexp = "^(?=.*[A-Za-z])(?=.*\\d).+$",
            message = "Password must contain at least one letter and one number")
    private String password;

    @NotBlank(message = "Major is required")
    @Size(max = 100, message = "Major name too long (max 100 characters)")
    private String major;

    @NotNull(message = "Graduation year is required")
    @Min(value = 2024, message = "Graduation year must be current or future")
    @Max(value = 2034, message = "Graduation year must be within 10 years")
    private Integer gradYear;
}
