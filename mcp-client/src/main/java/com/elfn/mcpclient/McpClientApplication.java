package com.elfn.mcpclient;

import io.modelcontextprotocol.client.McpSyncClient;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.List;

@SpringBootApplication
public class McpClientApplication {

    public static void main(String[] args) {
        SpringApplication.run(McpClientApplication.class, args);
    }

    /**
     * Lists available MCP tools at startup for diagnostic purposes.
     */
    @Bean
    public CommandLineRunner commandLineRunner(List<McpSyncClient> clients) {
        return args -> clients.forEach(client -> {
            System.out.println("=== MCP Tools Available ===");
            client.listTools().tools().forEach(tool ->
                System.out.printf("  [%s] %s%n", tool.name(), tool.description())
            );
            System.out.println("===========================");
        });
    }
}
