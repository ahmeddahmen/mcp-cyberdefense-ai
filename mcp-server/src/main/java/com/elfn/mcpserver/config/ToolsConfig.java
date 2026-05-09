package com.elfn.mcpserver.config;

import com.elfn.mcpserver.tools.StockTools;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Classe de configuration Spring utilisée pour déclarer les outils (tools)
 * accessibles par les agents via le mécanisme de MethodToolCallbackProvider.
 *
 * Elle permet d’enregistrer les objets outils (comme StockTools)
 * afin qu’ils soient appelables dynamiquement par les agents IA.
 *
 * @Author: Elimane
 */
@Configuration
public class ToolsConfig {

    /**
     * Crée et expose un bean MethodToolCallbackProvider contenant les objets outils.
     * Cela permet à Spring AI d’utiliser dynamiquement les méthodes annotées avec @Tool.
     *
     * @return une instance de MethodToolCallbackProvider avec les outils enregistrés.
     */
    @Bean
    public MethodToolCallbackProvider getMethodToolCallbackProvider() {
        return MethodToolCallbackProvider.builder()
                .toolObjects(new StockTools())
                .build();
    }
}
