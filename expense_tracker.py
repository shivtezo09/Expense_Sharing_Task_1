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
        payer = input("Who paid the expense? ").strip()
        if payer not in self.members:
            print("This person is not in the member list!")
            return

        try:
            amount = float(input("How much did they pay? "))
        except ValueError:
            print("Invalid amount!")
            return

        per_person = amount / len(self.members)
        shares = {member: per_person for member in self.members}
        
        expense = {
            'payer': payer,
            'amount': amount,
            'shares': shares
        }
        self.expenses.append(expense)

        for member in self.members:
            if member != payer:
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