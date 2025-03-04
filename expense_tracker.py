class ExpenseManager:
    def __init__(self):
        self.members = []
        self.expenses = []
        self.balances = {}

    def add_members(self, count):
        for i in range(count):
            name = input(f"Enter name of member {i+1}: ").strip()
            if name in self.members:
                print(f"{name} is already added!")
                continue
            self.members.append(name)
            self.balances[name] = {}
            for member in self.members:
                if member not in self.balances:
                    self.balances[member] = {}
                if member != name:
                    self.balances[name][member] = 0
                    self.balances[member][name] = 0
    
    def add_expense(self):
        print("\nHow would you like to add the expense?")
        print("1. All users share the expense")
        print("2. Only some users share the expense")
        sharing_option = input("Choose an option (1/2): ").strip()

        payer = input("Who paid the expense? ").strip()
        if payer not in self.members:
            print("This person is not in the member list!")
            return

        try:
            amount = float(input("How much did they pay? "))
        except ValueError:
            print("Invalid amount!")
            return

        sharers = []
        
        if sharing_option == '1':
            # All members share the expense
            sharers = self.members.copy()
        elif sharing_option == '2':
            # Only some members share the expense
            sharers_input = input("Who all share the expense? (separate names with commas): ").strip()
            sharers = [name.strip() for name in sharers_input.split(',')]
            
            # Validate that all sharers are in the members list
            for sharer in sharers:
                if sharer not in self.members:
                    print(f"{sharer} is not in the member list!")
                    return
            
            # Make sure the payer is included in sharers if not already
            if payer not in sharers:
                print(f"Adding {payer} to the list of sharers as they paid the expense.")
                sharers.append(payer)
        else:
            print("Invalid option!")
            return

        per_person = amount / len(sharers)
        
        # Initialize shares for all members
        shares = {member: 0 for member in self.members}
        
        # Update shares for only those who are sharing
        for sharer in sharers:
            shares[sharer] = per_person
        
        expense = {
            'payer': payer,
            'amount': amount,
            'sharers': sharers,
            'shares': shares
        }
        self.expenses.append(expense)

        # Update balances
        for member in self.members:
            if member != payer and shares[member] > 0:
                self.balances[member][payer] += shares[member]
                self.balances[payer][member] -= shares[member]

        print("Expense added successfully!")

    def show_expenses(self):
        if not self.expenses:
            print("No expenses recorded yet!")
            return

        print("\nNet Balances:")
        header = " " * 12 + "".join(f"{member:^12}" for member in self.members)
        print(header)
        print("-" * len(header))
        for row_member in self.members:
            row = f"{row_member:<12}"
            for col_member in self.members:
                if row_member == col_member:
                    row += f"{'0':^12}"
                else:
                    amount = self.balances.get(row_member, {}).get(col_member, 0)
                    if amount > 0:
                        row += f"{amount:^12.2f}"
                    else:
                        row += f"{'0':^12}"
            print(row)

def main():
    print("===== Expense Sharing Application =====")
    manager = ExpenseManager()

    try:
        n = int(input("Enter the number of members: "))
    except ValueError:
        print("Invalid number!")
        return

    if n <= 0:
        print("Invalid number of members!")
        return

    manager.add_members(n)

    while True:
        print("\nChoose from the following options:")
        print("1. Add an Expense")
        print("2. Show Expenses")
        print("3. Exit Program")

        choice = input("Enter your option: ").strip()
        if choice == '1':
            manager.add_expense()
        elif choice == '2':
            manager.show_expenses()
        elif choice == '3':
            print("Thank you for using the Expense Sharing Application!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()