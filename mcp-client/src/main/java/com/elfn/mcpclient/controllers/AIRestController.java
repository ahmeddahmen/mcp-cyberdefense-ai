package com.elfn.mcpclient.controllers;

import com.elfn.mcpclient.agents.AIAgent;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Contrôleur REST exposant une interface pour interagir avec l'agent d'IA.
 * <p>
 * Ce contrôleur permet de poser une requête (question) à un agent LLM via une méthode REST.
 * L'agent utilise un client LLM (comme OpenAI) pour générer une réponse.
 *
 * @author Elimane
 */
@RestController
public class AIRestController {

    /** Instance de l'agent d'IA chargé de gérer les appels LLM. */
    private final AIAgent agent;

    /**
     * Constructeur par injection de dépendance.
     *
     * @param agent l'agent IA utilisé pour traiter les requêtes
     */
    public AIRestController(AIAgent agent) {
        this.agent = agent;
    }

    /**
     * Méthode REST permettant d'envoyer une requête (prompt) à l'agent IA.
     *
     * @param query la question ou commande utilisateur
     * @return la réponse générée par le LLM
     */
    @GetMapping("chat")
    public String chat(String query) {
        return agent.askLLM(query);
    }
}
