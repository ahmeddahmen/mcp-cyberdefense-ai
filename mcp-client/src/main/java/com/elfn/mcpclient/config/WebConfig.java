package com.elfn.mcpclient.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.AsyncSupportConfigurer;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Web configuration to increase async request timeout
 * for long-running MCP tool calls (port scanning, log analysis).
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void configureAsyncSupport(AsyncSupportConfigurer configurer) {
        // 120 seconds timeout for async requests (MCP tool calls can be slow)
        configurer.setDefaultTimeout(120_000);
    }
}
