package com.elfn.mcpserver.tools;

import org.springframework.ai.tool.annotation.Tool;

import java.time.LocalDate;
import java.util.List;

/**
 * Service métier simulant des outils liés aux entreprises et à la bourse.
 *
 * Cette classe expose des méthodes utilisables comme outils (tools) dans un contexte d’agent IA, qui vont
 * être exploités par un agent pour récupérer des informations d’entreprises ou simuler des cours d’action.
 *
 * @author Elimane
 */
// @Service //=> Pas nécéssaire ici car l’objet StockTools est instancié manuellement dans la méthode suivante de la classe ToolsConfig
public class StockTools {

    /**
     * Liste statique d'entreprises simulées.
     */
    private List<Company> companies = List.of(
            new Company("Orance CI", "Telecom", 3, 10600, "Côte d'Ivoire"),
            new Company("BCM COTE D'IVOIRE", "Extraction minière", 5, 20000, "Côte d'Ivoire")
    );

    /**
     * Récupère toutes les entreprises disponibles.
     *
     * @return la liste des entreprises
     */
    @Tool(description = "Get All Companies")
    public List<Company> getAllCompanies() {
        return companies;
    }

    /**
     * Récupère une entreprise à partir de son nom.
     *
     * @param name le nom de l’entreprise
     * @return l’entreprise correspondante
     * @throws RuntimeException si l’entreprise n’est pas trouvée
     */
    @Tool(description = "Get a company by its name")
    public Company getCompanyByName(String name) {
        return companies.stream()
                .filter(c -> c.name().equals(name))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("Company not found"));
    }

    /**
     * Simule un cours de bourse pour une entreprise donnée.
     * Le prix est aléatoire entre 300 et 600.
     *
     * @param name le nom de l’entreprise
     * @return un objet Stock contenant le nom, la date et un prix simulé
     */
    @Tool(description = "Get a stock by company name")
    public Stock getStockByCompanyName(String name) {
        return new Stock(name, 300 + Math.random() * 300, LocalDate.now());
    }
}
