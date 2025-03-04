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
            self.balances[name] = {member: 0 for member in self.members}  
            for member in self.members:
                if member not in self.balances:
                    self.balances[member] = {}
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

        print("\nSharing Pattern:")
        print("1. All users share the expense")
        print("2. Only some users share the expense")
        try:
            sharing_pattern = int(input("Enter your choice (1/2): "))
        except ValueError:
            print("Invalid choice!")
            return

        sharers = []
        if sharing_pattern == 1:
            sharers = self.members.copy()
        elif sharing_pattern == 2:
            sharers_input = input("Who all share the expense? (comma-separated names): ")
            sharers = [name.strip() for name in sharers_input.split(',')]
            for name in sharers:
                if name not in self.members:
                    print(f"{name} is not in the member list!")
                    return
        else:
            print("Invalid choice!")
            return

        print("\nExpense Distribution:")
        print("1. Everyone shares the expense equally")
        print("2. Expense is shared in a ratio")
        try:
            distribution = int(input("Enter your choice (1/2): "))
        except ValueError:
            print("Invalid choice!")
            return

        shares = {}
        if distribution == 1:
            per_person = amount / len(sharers)
            for member in sharers:
                shares[member] = per_person
        elif distribution == 2:
            ratios_input = input(f"Enter the ratios for {', '.join(sharers)} (comma-separated): ")
            try:
                ratios = [float(r.strip()) for r in ratios_input.split(',')]
            except ValueError:
                print("Invalid ratio input!")
                return
            if len(ratios) != len(sharers):
                print("Number of ratios doesn't match number of sharers!")
                return

            total_ratio = sum(ratios)
            if total_ratio == 0:
                print("Invalid ratios! Total ratio cannot be zero.")
                return

            for i, member in enumerate(sharers):
                shares[member] = round((ratios[i] / total_ratio) * amount, 2)
        else:
            print("Invalid choice!")
            return

        expense = {
            'payer': payer,
            'amount': amount,
            'sharers': sharers,
            'shares': shares
        }
        self.expenses.append(expense)

        for member in sharers:
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
                        row += f"{amount:^12.0f}"
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
