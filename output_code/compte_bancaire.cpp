#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>

class BankAccount {
public:
    // Constructeur avec solde initial et propriétaire
    BankAccount(const std::string& owner, double initial_balance = 0)
        : owner(owner), balance(initial_balance) {}

    // Dépôt sur le compte
    void deposit(double amount) {
        if (amount <= 0) {
            throw std::invalid_argument("Le montant du dépôt doit être positif.");
        }
        balance += amount;
        transactions.push_back({"dépôt", amount});
    }

    // Retrait du compte
    void withdraw(double amount) {
        if (amount <= 0) {
            throw std::invalid_argument("Le montant du retrait doit être positif.");
        }
        if (amount > balance) {
            throw std::invalid_argument("Fonds insuffisants.");
        }
        balance -= amount;
        transactions.push_back({"retrait", amount});
    }

    // Retourne le solde actuel
    double get_balance() const {
        return balance;
    }

    // Retourne l'historique des transactions
    const std::vector<std::pair<std::string, double>>& get_transaction_history() const {
        return transactions;
    }

    // Affiche les informations du compte
    void display_account_info() const {
        std::cout << "Compte de : " << owner << std::endl;
        std::cout << "Solde actuel : " << balance << "€" << std::endl;
        std::cout << "Historique des transactions :" << std::endl;
        for (const auto& transaction : transactions) {
            std::cout << " - " << transaction.first << " : " << transaction.second << "€" << std::endl;
        }
    }

private:
    std::string owner;
    double balance;
    std::vector<std::pair<std::string, double>> transactions; // Vecteur des transactions
};

int main() {
    // Exemple d'utilisation
    BankAccount account("Alice", 1000);

    // Opérations
    account.deposit(500);
    account.withdraw(200);

    // Affichage des informations du compte
    account.display_account_info();

    return 0;
}
