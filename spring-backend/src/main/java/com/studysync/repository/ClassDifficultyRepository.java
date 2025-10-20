package com.studysync.repository;

import com.studysync.model.ClassDifficultySubmission;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ClassDifficultyRepository extends MongoRepository<ClassDifficultySubmission, String> {
    List<ClassDifficultySubmission> findByMajor(String major);
    List<ClassDifficultySubmission> findByMajorAndClassCode(String major, String classCode);
    Optional<ClassDifficultySubmission> findByUserIdAndClassCodeAndMajor(String userId, String classCode, String major);
    List<String> findDistinctMajorBy();
}
