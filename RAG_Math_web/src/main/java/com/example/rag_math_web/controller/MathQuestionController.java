package com.example.rag_math_web.controller;

import com.example.rag_math_web.model.MathQuestion;
import com.example.rag_math_web.service.MathQuestionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/math")
@RequiredArgsConstructor
public class MathQuestionController {

    private final MathQuestionService mathQuestionService;

    @PostMapping("/question")
    public ResponseEntity<MathQuestion> askQuestion(@RequestBody Map<String, String> request) {
        // TODO: 实现与LLM的交互逻辑
        return ResponseEntity.ok().build();
    }

    @GetMapping("/questions")
    public ResponseEntity<List<MathQuestion>> getAllQuestions() {
        return ResponseEntity.ok(mathQuestionService.getAllQuestions());
    }

    @PostMapping("/similar")
    public ResponseEntity<List<MathQuestion>> findSimilarQuestions(@RequestBody double[] embedding) {
        return ResponseEntity.ok(mathQuestionService.findSimilarQuestions(embedding, 5));
    }
} 