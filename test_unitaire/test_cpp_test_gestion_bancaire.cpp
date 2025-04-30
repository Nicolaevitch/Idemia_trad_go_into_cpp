Pour traduire ce script de test unitaire Python en C++, nous allons utiliser le framework de test Google Test, qui est couramment utilisé pour les tests unitaires en C++. Voici comment le code pourrait être traduit :

```cpp
#include <gtest/gtest.h>
#include "gestion_bancaire.h" // Assurez-vous que ce fichier contient la classe BankAccount

class TestBankAccount : public ::testing::Test {
protected:
    BankAccount* account;

    void SetUp() override {
        // Initialisation d'un compte bancaire pour les tests
        account = new BankAccount("Alice", 1000);
    }

    void TearDown() override {
        delete account;
    }
};

TEST_F(TestBankAccount, InitialBalance) {
    // Test du solde initial
    EXPECT_EQ(account->getBalance(), 1000);
}

TEST_F(TestBankAccount, Deposit) {
    // Test du dépôt d'argent
    account->deposit(500);
    EXPECT_EQ(account->getBalance(), 1500);
    auto history = account->getTransactionHistory();
    EXPECT_EQ(history.back().type, "dépôt");
    EXPECT_EQ(history.back().amount, 500);
}

TEST_F(TestBankAccount, Withdraw) {
    // Test du retrait d'argent
    account->withdraw(200);
    EXPECT_EQ(account->getBalance(), 800);
    auto history = account->getTransactionHistory();
    EXPECT_EQ(history.back().type, "retrait");
    EXPECT_EQ(history.back().amount, 200);
}

TEST_F(TestBankAccount, WithdrawInsufficientFunds) {
    // Test du retrait avec fonds insuffisants
    try {
        account->withdraw(1500);
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument& e) {
        EXPECT_EQ(e.what(), std::string("Fonds insuffisants."));
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(TestBankAccount, DepositNegativeAmount) {
    // Test du dépôt d'un montant négatif
    try {
        account->deposit(-100);
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument& e) {
        EXPECT_EQ(e.what(), std::string("Le montant du dépôt doit être positif."));
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(TestBankAccount, WithdrawNegativeAmount) {
    // Test du retrait d'un montant négatif
    try {
        account->withdraw(-100);
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument& e) {
        EXPECT_EQ(e.what(), std::string("Le montant du retrait doit être positif."));
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(TestBankAccount, TransactionHistory) {
    // Test de l'historique des transactions
    account->deposit(300);
    account->withdraw(100);
    auto history = account->getTransactionHistory();
    ASSERT_GE(history.size(), 2);
    EXPECT_EQ(history[history.size() - 2].type, "dépôt");
    EXPECT_EQ(history[history.size() - 2].amount, 300);
    EXPECT_EQ(history.back().type, "retrait");
    EXPECT_EQ(history.back().amount, 100);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

### Remarques :

1. **Gestion des exceptions** : En C++, nous utilisons `try-catch` pour gérer les exceptions, et nous vérifions le type d'exception attendu.

2. **Google Test** : Nous utilisons les macros `TEST_F` pour définir des tests qui utilisent des fixtures, ce qui permet de configurer et de nettoyer les objets de test.

3. **Assertions** : Les assertions `EXPECT_EQ` et `ASSERT_GE` sont utilisées pour vérifier les conditions dans les tests.

4. **Historique des transactions** : Nous supposons que `getTransactionHistory()` retourne un vecteur de structures ou d'objets contenant les informations de type et de montant.

Assurez-vous que la classe `BankAccount` en C++ est correctement définie avec les méthodes `getBalance()`, `deposit()`, `withdraw()`, et `getTransactionHistory()`, et qu'elle gère les exceptions comme attendu.