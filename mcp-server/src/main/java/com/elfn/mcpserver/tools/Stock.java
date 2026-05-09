package com.elfn.mcpserver.tools;

import java.time.LocalDate;

/**
 * @Author: Elimane
 */
public record Stock(String companyName, double stock, LocalDate date) {
}
