from presentation.cli import available_tickets, book_ticket, refund

def main():
    while True:
        print("\nFlight Booking System")
        print("1. Search available tickets")
        print("2. Book a ticket")
        print("3. Refund a ticket")
        print("4: Exit system")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            available_tickets()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            refund()    
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 