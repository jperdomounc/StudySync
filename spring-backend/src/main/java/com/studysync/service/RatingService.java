package com.studysync.service;

import com.studysync.dto.*;
import com.studysync.model.ClassDifficultySubmission;
import com.studysync.model.ProfessorRating;
import com.studysync.model.User;
import com.studysync.repository.ClassDifficultyRepository;
import com.studysync.repository.ProfessorRatingRepository;
import com.studysync.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.*;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class RatingService {

    @Autowired
    private ClassDifficultyRepository classRepository;

    @Autowired
    private ProfessorRatingRepository professorRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private MongoTemplate mongoTemplate;

    public void submitClassDifficulty(ClassDifficultyRequest request, String userId) {
        // Get user to verify major
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        if (!request.getMajor().equals(user.getMajor())) {
            throw new IllegalArgumentException("You can only submit ratings for your own major");
        }

        // Check if user already submitted for this class
        Optional<ClassDifficultySubmission> existing = classRepository
                .findByUserIdAndClassCodeAndMajor(userId, request.getClassCode(), request.getMajor());

        ClassDifficultySubmission submission;
        if (existing.isPresent()) {
            // Update existing submission
            submission = existing.get();
        } else {
            // Create new submission
            submission = new ClassDifficultySubmission();
            submission.setUserId(userId);
        }

        submission.setClassCode(request.getClassCode().toUpperCase());
        submission.setClassName(request.getClassName().trim());
        submission.setMajor(request.getMajor());
        submission.setDifficultyRating(request.getDifficultyRating());
        submission.setProfessor(request.getProfessor().trim());
        submission.setSemester(request.getSemester());
        submission.setSubmittedAt(LocalDateTime.now());

        classRepository.save(submission);
    }

    public void submitProfessorRating(ProfessorRatingRequest request, String userId) {
        // Get user to verify major
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        if (!request.getMajor().equals(user.getMajor())) {
            throw new IllegalArgumentException("You can only submit ratings for your own major");
        }

        // Check if user already rated this professor for this class
        Optional<ProfessorRating> existing = professorRepository
                .findByUserIdAndProfessorAndClassCode(userId, request.getProfessor(), request.getClassCode());

        ProfessorRating rating;
        if (existing.isPresent()) {
            // Update existing rating
            rating = existing.get();
        } else {
            // Create new rating
            rating = new ProfessorRating();
            rating.setUserId(userId);
        }

        rating.setProfessor(request.getProfessor().trim());
        rating.setClassCode(request.getClassCode());
        rating.setRating(Math.round(request.getRating() * 10.0) / 10.0);
        rating.setReview(request.getReview() != null ? request.getReview().trim() : "");
        rating.setMajor(request.getMajor());
        rating.setSemester(request.getSemester());
        rating.setSubmittedAt(LocalDateTime.now());

        professorRepository.save(rating);
    }

    public List<ClassRankingResponse> getClassRankings(String major, int limit) {
        // Use MongoDB aggregation to get class rankings
        MatchOperation matchMajor = Aggregation.match(Criteria.where("major").is(major));

        GroupOperation groupByClass = Aggregation.group("classCode", "className", "major")
                .avg("difficultyRating").as("averageDifficulty")
                .count().as("totalSubmissions")
                .addToSet("professor").as("professors");

        SortOperation sortByDifficulty = Aggregation.sort(
                org.springframework.data.domain.Sort.Direction.DESC, "averageDifficulty");

        LimitOperation limitResults = Aggregation.limit(limit);

        Aggregation aggregation = Aggregation.newAggregation(
                matchMajor, groupByClass, sortByDifficulty, limitResults);

        List<Map> results = mongoTemplate.aggregate(
                aggregation, "class_submissions", Map.class).getMappedResults();

        return results.stream().map(result -> {
            Map<String, Object> id = (Map<String, Object>) result.get("_id");
            String classCode = (String) id.get("classCode");
            String className = (String) id.get("className");

            List<String> professors = (List<String>) result.get("professors");
            List<ClassRankingResponse.ProfessorStats> professorStats =
                    getProfessorStats(professors, classCode, major);

            return ClassRankingResponse.builder()
                    .classCode(classCode)
                    .className(className)
                    .major((String) id.get("major"))
                    .averageDifficulty(Math.round(((Number) result.get("averageDifficulty")).doubleValue() * 10.0) / 10.0)
                    .totalSubmissions(((Number) result.get("totalSubmissions")).intValue())
                    .professors(professorStats)
                    .build();
        }).collect(Collectors.toList());
    }

    private List<ClassRankingResponse.ProfessorStats> getProfessorStats(
            List<String> professors, String classCode, String major) {
        return professors.stream().map(prof -> {
            List<ProfessorRating> ratings = professorRepository
                    .findByProfessorAndClassCodeAndMajor(prof, classCode, major);

            if (ratings.isEmpty()) {
                return ClassRankingResponse.ProfessorStats.builder()
                        .name(prof)
                        .avgRating(0.0)
                        .ratingCount(0)
                        .build();
            }

            double avgRating = ratings.stream()
                    .mapToDouble(ProfessorRating::getRating)
                    .average()
                    .orElse(0.0);

            return ClassRankingResponse.ProfessorStats.builder()
                    .name(prof)
                    .avgRating(Math.round(avgRating * 10.0) / 10.0)
                    .ratingCount(ratings.size())
                    .build();
        }).sorted((a, b) -> Double.compare(b.getAvgRating(), a.getAvgRating()))
          .collect(Collectors.toList());
    }

    public List<String> getAllMajors() {
        return classRepository.findDistinctMajorBy().stream()
                .sorted()
                .collect(Collectors.toList());
    }

    public MajorStatsResponse getMajorStats(String major) {
        // Count unique classes
        List<ClassDifficultySubmission> submissions = classRepository.findByMajor(major);
        long uniqueClasses = submissions.stream()
                .map(ClassDifficultySubmission::getClassCode)
                .distinct()
                .count();

        // Count users in this major
        long userCount = userRepository.countByMajor(major);

        // Calculate average difficulty
        double avgDifficulty = submissions.stream()
                .mapToInt(ClassDifficultySubmission::getDifficultyRating)
                .average()
                .orElse(0.0);

        return MajorStatsResponse.builder()
                .major(major)
                .totalClasses((int) uniqueClasses)
                .totalUsers((int) userCount)
                .averageDifficulty(Math.round(avgDifficulty * 10.0) / 10.0)
                .build();
    }

    public List<ProfessorRating> getProfessorRatings(String professor, String classCode) {
        if (classCode != null && !classCode.isEmpty()) {
            return professorRepository.findByProfessorAndClassCode(professor, classCode);
        }
        return professorRepository.findByProfessor(professor);
    }
}
