package com.studysync.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.CompoundIndexes;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "professor_ratings")
@CompoundIndexes({
    @CompoundIndex(name = "prof_class_idx", def = "{'professor': 1, 'classCode': 1}"),
    @CompoundIndex(name = "major_prof_idx", def = "{'major': 1, 'professor': 1}")
})
public class ProfessorRating {
    @Id
    private String id;

    @Indexed
    private String professor;

    private String classCode;

    private Double rating; // 1-5 stars

    private String review;

    @Indexed
    private String major;

    private String semester;

    @Indexed
    private String userId;

    private LocalDateTime submittedAt;
}
