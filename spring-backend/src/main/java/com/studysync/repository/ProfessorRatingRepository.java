package com.studysync.repository;

import com.studysync.model.ProfessorRating;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ProfessorRatingRepository extends MongoRepository<ProfessorRating, String> {
    List<ProfessorRating> findByProfessorAndClassCodeAndMajor(String professor, String classCode, String major);
    List<ProfessorRating> findByProfessor(String professor);
    List<ProfessorRating> findByProfessorAndClassCode(String professor, String classCode);
    Optional<ProfessorRating> findByUserIdAndProfessorAndClassCode(String userId, String professor, String classCode);
}
