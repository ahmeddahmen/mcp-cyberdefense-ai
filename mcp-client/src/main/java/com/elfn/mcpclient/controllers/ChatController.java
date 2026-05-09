package com.elfn.mcpclient.controllers;

import com.elfn.mcpclient.agents.AIAgent;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

/**
 * @Author: Elimane
 */
@Controller
@CrossOrigin("*")
public class ChatController {
    private final AIAgent agent;

    public ChatController(AIAgent agent) {
        this.agent = agent;
    }

    @GetMapping("/")
    public String chatPage() {
        return "chat";
    }

    @PostMapping("/chat/send")
    @ResponseBody
    public ResponseEntity<String> sendMessage(@RequestParam String message) {
        try {
            String response = agent.askLLM(message);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            String errorMsg = e.getClass().getSimpleName() + ": " + e.getMessage();
            System.err.println("[ChatController ERROR] " + errorMsg);
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("Error: " + errorMsg);
        }
    }
}
