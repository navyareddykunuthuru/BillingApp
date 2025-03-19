import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem
import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="navya@123",  # Your MySQL password
        database="billing_system"
    )

class BillingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing System")
        
        self.layout = QVBoxLayout()

        # Customer form inputs
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Customer Name")
        self.layout.addWidget(self.name_input)

        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Customer Address")
        self.layout.addWidget(self.address_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Customer Phone")
        self.layout.addWidget(self.phone_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Customer Email")
        self.layout.addWidget(self.email_input)

        # Bill form inputs
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Bill Amount")
        self.layout.addWidget(self.amount_input)

        # Submit Button
        self.submit_button = QPushButton("Submit Bill", self)
        self.submit_button.clicked.connect(self.submit_bill)
        self.layout.addWidget(self.submit_button)

        # Table for displaying bills and customers
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Customer Name", "Amount", "Date", "Action"])
        self.layout.addWidget(self.table)

        # Set layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Display Existing Data
        self.load_data()

    def submit_bill(self):
        # Get values from input fields
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        amount = self.amount_input.text()

        # Basic Validation (ensure that no fields are empty)
        if not name or not address or not phone or not email or not amount:
            # Show an error or message if validation fails
            print("All fields are required!")
            return

        try:
            # Insert customer data into 'customers' table
            db = connect_to_db()
            cursor = db.cursor()

            cursor.execute(
                "INSERT INTO customers (name, address, phone_number, email) VALUES (%s, %s, %s, %s)",
                (name, address, phone, email)
            )
            db.commit()  # Commit the transaction

            # Get the customer_id of the newly inserted customer
            customer_id = cursor.lastrowid

            # Insert bill data into 'bills' table
            cursor.execute(
                "INSERT INTO bills (customer_id, amount, bill_date) VALUES (%s, %s, NOW())",
                (customer_id, amount)
            )
            db.commit()  # Commit the transaction

            # Close the cursor and connection
            cursor.close()
            db.close()

            # Clear the input fields after successful insertion
            self.name_input.clear()
            self.address_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.amount_input.clear()

            # Refresh the table to show the newly inserted data
            self.load_data()

            print("Data Submitted Successfully!")
            
        except Exception as e:
            print(f"Error: {e}")

    def load_data(self):
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT c.name, b.amount, b.bill_date FROM bills b JOIN customers c ON b.customer_id = c.customer_id")
        bills = cursor.fetchall()

        self.table.setRowCount(0)
        for row_num, row in enumerate(bills):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

        cursor.close()
        db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
