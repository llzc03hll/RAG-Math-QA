package com.example.rag_math_web.repository;

import com.example.rag_math_web.model.MathQuestion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

// 这个类是用来保存和查询数学问题的
public interface MathQuestionRepository extends JpaRepository<MathQuestion, Long> {
    
    @Query(value = "SELECT * FROM math_questions ORDER BY embedding <-> :embedding LIMIT :limit", nativeQuery = true)
    List<MathQuestion> findSimilarQuestions(@Param("embedding") double[] embedding, @Param("limit") int limit);
} 