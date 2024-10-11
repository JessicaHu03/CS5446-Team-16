from presentation.cli import available_tickets, book_ticket

def main():
    while True:
        print("\nFlight Booking System")
        print("1. Search available tickets")
        print("2. Book a ticket")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            available_tickets()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            refund()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()