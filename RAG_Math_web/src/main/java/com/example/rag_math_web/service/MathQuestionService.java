package com.example.rag_math_web.service;

import com.example.rag_math_web.model.MathQuestion;
import com.example.rag_math_web.repository.MathQuestionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

// 这个类是用来保存和查询数学问题的
@Service
@RequiredArgsConstructor
public class MathQuestionService {
    
    private final MathQuestionRepository mathQuestionRepository;
    
    public MathQuestion saveMathQuestion(String question, String answer, double[] embedding) {
        MathQuestion mathQuestion = new MathQuestion();
        mathQuestion.setQuestion(question);
        mathQuestion.setAnswer(answer);
        mathQuestion.setEmbedding(embedding);
        return mathQuestionRepository.save(mathQuestion);
    }
    
    public List<MathQuestion> findSimilarQuestions(double[] embedding, int limit) {
        return mathQuestionRepository.findSimilarQuestions(embedding, limit);
    }
    
    public List<MathQuestion> getAllQuestions() {
        return mathQuestionRepository.findAll();
    }
} 