package com.studysync.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "users")
public class User {
    @Id
    private String id;

    @Indexed(unique = true)
    private String email;

    private String passwordHash;

    @Indexed
    private String major;

    @Indexed
    private Integer gradYear;

    private String displayName;

    private LocalDateTime createdAt;

    private Boolean isActive = true;

    private Boolean emailVerified = false;
}
