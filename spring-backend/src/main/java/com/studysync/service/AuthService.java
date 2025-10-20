package com.studysync.service;

import com.studysync.dto.*;
import com.studysync.model.User;
import com.studysync.repository.UserRepository;
import com.studysync.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtil jwtUtil;

    public AuthResponse register(UserCreateRequest request) {
        // Check if user already exists
        if (userRepository.existsByEmail(request.getEmail().toLowerCase())) {
            throw new IllegalArgumentException("User with this email already exists");
        }

        // Create new user
        User user = new User();
        user.setEmail(request.getEmail().toLowerCase());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setMajor(request.getMajor().trim());
        user.setGradYear(request.getGradYear());
        user.setDisplayName(request.getMajor().trim() + " " + request.getGradYear());
        user.setCreatedAt(LocalDateTime.now());
        user.setIsActive(true);
        user.setEmailVerified(false);

        User savedUser = userRepository.save(user);

        // Generate JWT token
        String token = jwtUtil.generateToken(savedUser.getId());

        // Build response
        return AuthResponse.builder()
                .accessToken(token)
                .tokenType("bearer")
                .user(mapToUserResponse(savedUser))
                .build();
    }

    public AuthResponse login(LoginRequest request) {
        // Find user by email
        User user = userRepository.findByEmail(request.getEmail().toLowerCase())
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password"));

        // Verify password
        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new IllegalArgumentException("Invalid email or password");
        }

        // Check if user is active
        if (!user.getIsActive()) {
            throw new IllegalArgumentException("User account is deactivated");
        }

        // Generate JWT token
        String token = jwtUtil.generateToken(user.getId());

        // Build response
        return AuthResponse.builder()
                .accessToken(token)
                .tokenType("bearer")
                .user(mapToUserResponse(user))
                .build();
    }

    public UserResponse getCurrentUser(String userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));
        return mapToUserResponse(user);
    }

    private UserResponse mapToUserResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .email(user.getEmail())
                .displayName(user.getDisplayName())
                .major(user.getMajor())
                .gradYear(user.getGradYear())
                .build();
    }
}
