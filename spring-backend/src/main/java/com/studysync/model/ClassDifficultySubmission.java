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
@Document(collection = "class_submissions")
@CompoundIndexes({
    @CompoundIndex(name = "major_class_idx", def = "{'major': 1, 'classCode': 1}"),
    @CompoundIndex(name = "class_major_idx", def = "{'classCode': 1, 'major': 1}")
})
public class ClassDifficultySubmission {
    @Id
    private String id;

    private String classCode;

    private String className;

    @Indexed
    private String major;

    private Integer difficultyRating;

    @Indexed
    private String professor;

    private String semester;

    @Indexed
    private String userId;

    private LocalDateTime submittedAt;
}
