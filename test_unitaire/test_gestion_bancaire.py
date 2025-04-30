
import unittest
from input_code.gestion_bancaire import BankAccount

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Initialisation d'un compte bancaire pour les tests."""
        self.account = BankAccount("Alice", 1000)

    def test_initial_balance(self):
        """Test du solde initial."""
        self.assertEqual(self.account.get_balance(), 1000)

    def test_deposit(self):
        """Test du dépôt d'argent."""
        self.account.deposit(500)
        self.assertEqual(self.account.get_balance(), 1500)
        self.assertEqual(self.account.get_transaction_history()[-1], {"type": "dépôt", "amount": 500})

    def test_withdraw(self):
        """Test du retrait d'argent."""
        self.account.withdraw(200)
        self.assertEqual(self.account.get_balance(), 800)
        self.assertEqual(self.account.get_transaction_history()[-1], {"type": "retrait", "amount": 200})

    def test_withdraw_insufficient_funds(self):
        """Test du retrait avec fonds insuffisants."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500)
        self.assertEqual(str(context.exception), "Fonds insuffisants.")

    def test_deposit_negative_amount(self):
        """Test du dépôt d'un montant négatif."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100)
        self.assertEqual(str(context.exception), "Le montant du dépôt doit être positif.")

    def test_withdraw_negative_amount(self):
        """Test du retrait d'un montant négatif."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100)
        self.assertEqual(str(context.exception), "Le montant du retrait doit être positif.")

    def test_transaction_history(self):
        """Test de l'historique des transactions."""
        self.account.deposit(300)
        self.account.withdraw(100)
        expected_history = [
            {"type": "dépôt", "amount": 300},
            {"type": "retrait", "amount": 100}
        ]
        self.assertEqual(self.account.get_transaction_history()[-2:], expected_history)

if __name__ == '__main__':
    unittest.main()
