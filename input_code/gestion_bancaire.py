class BankAccount:
    """Un simple gestionnaire de compte bancaire avec historique des transactions."""
    
    def __init__(self, owner, initial_balance=0):
        """Initialise un compte avec un propriétaire et un solde initial."""
        self.owner = owner
        self.balance = initial_balance
        self.transactions = []  # Liste des transactions (historique)

    def deposit(self, amount):
        """Ajoute de l'argent au compte et enregistre la transaction."""
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être positif.")
        self.balance += amount
        self.transactions.append({"type": "dépôt", "amount": amount})

    def withdraw(self, amount):
        """Retire de l'argent du compte si le solde est suffisant."""
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être positif.")
        if amount > self.balance:
            raise ValueError("Fonds insuffisants.")
        self.balance -= amount
        self.transactions.append({"type": "retrait", "amount": amount})

    def get_balance(self):
        """Retourne le solde actuel du compte."""
        return self.balance

    def get_transaction_history(self):
        """Retourne l'historique des transactions."""
        return self.transactions

    def display_account_info(self):
        """Affiche les détails du compte et son historique."""
        print(f"Compte de : {self.owner}")
        print(f"Solde actuel : {self.balance}€")
        print("Historique des transactions :")
        for transaction in self.transactions:
            print(f" - {transaction['type']} : {transaction['amount']}€")

# Exemple d'utilisation
if __name__ == "__main__":
    account = BankAccount("Alice", 1000)
    
    # Opérations
    account.deposit(500)
    account.withdraw(200)

    # Affichage des informations du compte
    account.display_account_info()
