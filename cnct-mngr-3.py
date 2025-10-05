#!/usr/bin/env python3
"""
Contact Manager 2.0 - Advanced Business Management System

A comprehensive contact management application for handling organizations,
employees, customers, and products with modern Python best practices.

Author: pyz3r
Python Version: 3.8+
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Optional, List, Union
from pathlib import Path

# ░█▀█░█░█░▀▀█░▀▀█░█▀▄
# ░█▀▀░░█░░▄▀░░░▀▄░█▀▄
# ░▀░░░░▀░░▀▀▀░▀▀░░▀░▀

class ContactManager:
    """
    Main Contact Manager class implementing modern Python patterns.
    
    This class manages organizations, employees, customers, and products
    with automatic data persistence and validation.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize ContactManager with data directory.
        
        Args:
            data_dir: Directory to store JSON files (default: 'data')
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.organizations: Dict[int, Dict] = {}
        self.employees: Dict[int, Dict] = {}
        self.customers: Dict[int, Dict] = {}
        self.products: Dict[int, Dict] = {}
        
        # File paths
        self.files = {
            'organizations': self.data_dir / "organizations.json",
            'employees': self.data_dir / "employees.json",
            'customers': self.data_dir / "customers.json",
            'products': self.data_dir / "products.json"
        }
        
        # Load existing data
        self._load_all_data()
        
    def _save_data(self, data_type: str, data: Dict) -> None:
        """
        Save data to JSON file with error handling.
        
        Args:
            data_type: Type of data ('organizations', 'employees', etc.)
            data: Dictionary to save
        """
        try:
            with open(self.files[data_type], 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self._show_error(f"Error saving {data_type}: {e}")
    
    def _load_data(self, data_type: str) -> Dict:
        """
        Load data from JSON file with error handling.
        
        Args:
            data_type: Type of data to load
            
        Returns:
            Dictionary with loaded data or empty dict if file doesn't exist
        """
        try:
            if self.files[data_type].exists():
                with open(self.files[data_type], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert string keys back to integers
                    return {int(k): v for k, v in data.items()}
            return {}
        except Exception as e:
            self._show_error(f"Error loading {data_type}: {e}")
            return {}
    
    def _load_all_data(self) -> None:
        """Load all data from JSON files."""
        self.organizations = self._load_data('organizations')
        self.employees = self._load_data('employees')
        self.customers = self._load_data('customers')
        self.products = self._load_data('products')
    
    def _generate_id(self, data_dict: Dict) -> int:
        """
        Generate next available ID for any data type.
        
        Args:
            data_dict: Dictionary to generate ID for
            
        Returns:
            Next available integer ID
        """
        return max(data_dict.keys(), default=0) + 1
    
    @staticmethod
    def _clear_screen() -> None:
        """Clear terminal screen cross-platform."""
        os.system('cls' if sys.platform.startswith('win') else 'clear')
    
    @staticmethod
    def _show_header(title: str) -> None:
        """
        Display formatted header.
        
        Args:
            title: Header title to display
        """
        ContactManager._clear_screen()
        width = max(60, len(title) + 10)
        print("┌" + "─" * (width - 2) + "┐")
        print(f"│{title:^{width-2}}│")
        print("└" + "─" * (width - 2) + "┘")
        print()
    
    @staticmethod
    def _show_error(message: str) -> None:
        """
        Display error message with formatting.
        
        Args:
            message: Error message to display
        """
        print(f"❌ {message}")
    
    @staticmethod
    def _show_success(message: str) -> None:
        """
        Display success message with formatting.
        
        Args:
            message: Success message to display
        """
        print(f"✅ {message}")
    
    @staticmethod
    def _get_input(prompt: str, input_type: type = str, required: bool = True) -> Optional[Union[str, int, float]]:
        """
        Get user input with type validation.
        
        Args:
            prompt: Input prompt message
            input_type: Expected input type (str, int, float)
            required: Whether input is required
            
        Returns:
            Validated input or None if not required and empty
        """
        while True:
            try:
                value = input(f"📝 {prompt}: ").strip()
                
                if not value and not required:
                    return None
                if not value and required:
                    print("❌ This field is required!")
                    continue
                
                if input_type == str:
                    return value
                elif input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                    
            except ValueError:
                print(f"❌ Please enter a valid {input_type.__name__}!")
            except KeyboardInterrupt:
                print("\n\n👋 Operation cancelled.")
                return None
    
    def _get_valid_org_id(self) -> Optional[int]:
        """
        Get valid organization ID from user.
        
        Returns:
            Valid organization ID or None if cancelled
        """
        if not self.organizations:
            self._show_error("No organizations available. Create one first.")
            return None
        
        self._list_organizations()
        while True:
            org_id = self._get_input("Select Organization ID", int)
            if org_id is None:  # Cancelled
                return None
            if org_id in self.organizations:
                return org_id
            self._show_error("Organization not found!")
    
    # Organization Management
    def add_organization(self) -> None:
        """Add new organization with user input."""
        self._show_header("ADD NEW ORGANIZATION")
        
        name = self._get_input("Organization Name")
        if not name:
            return
            
        oib = self._get_input("Tax ID/OIB")
        if not oib:
            return
            
        address = self._get_input("Address")
        if not address:
            return
            
        website = self._get_input("Website", required=False)
        
        org_id = self._generate_id(self.organizations)
        
        organization = {
            'id': org_id,
            'name': name,
            'oib': oib,
            'address': address,
            'website': website or '',
            'created_at': datetime.now().isoformat(),
            'employee_count': 0,
            'customer_count': 0,
            'product_count': 0
        }
        
        self.organizations[org_id] = organization
        self._save_data('organizations', self.organizations)
        self._show_success(f"Organization '{name}' added with ID: {org_id}")
        
        input("\n⏸️  Press Enter to continue...")
    
    def _list_organizations(self) -> None:
        """Display all organizations in formatted table."""
        if not self.organizations:
            print("📭 No organizations found.")
            return
        
        print("🏢 ORGANIZATIONS:")
        print("─" * 80)
        print(f"{'ID':<4} {'Name':<25} {'OIB':<15} {'Address':<35}")
        print("─" * 80)
        
        for org in self.organizations.values():
            website_info = f" 🌐 {org['website']}" if org['website'] else ""
            print(f"{org['id']:<4} {org['name']:<25} {org['oib']:<15} {org['address']:<35}")
            if website_info:
                print(f"{'':>44}{website_info}")
        print()
    
    def view_organizations(self) -> None:
        """View all organizations."""
        self._show_header("ALL ORGANIZATIONS")
        self._list_organizations()
        input("⏸️  Press Enter to continue...")
    
    def delete_organization(self) -> None:
        """Delete organization with confirmation."""
        self._show_header("DELETE ORGANIZATION")
        
        org_id = self._get_valid_org_id()
        if not org_id:
            return
        
        org_name = self.organizations[org_id]['name']
        print(f"\n⚠️  WARNING: This will delete organization '{org_name}' and ALL related data!")
        print("   - All employees")
        print("   - All customers") 
        print("   - All products")
        
        confirm = input("\n❓ Type 'DELETE' to confirm: ").strip()
        if confirm != 'DELETE':
            print("❌ Deletion cancelled.")
            input("⏸️  Press Enter to continue...")
            return
        
        # Delete related data
        self.employees = {k: v for k, v in self.employees.items() if v['organization_id'] != org_id}
        self.customers = {k: v for k, v in self.customers.items() if v['organization_id'] != org_id}
        self.products = {k: v for k, v in self.products.items() if v['organization_id'] != org_id}
        
        # Delete organization
        del self.organizations[org_id]
        
        # Save all changes
        self._save_data('organizations', self.organizations)
        self._save_data('employees', self.employees)
        self._save_data('customers', self.customers)
        self._save_data('products', self.products)
        
        self._show_success(f"Organization '{org_name}' and all related data deleted.")
        input("⏸️  Press Enter to continue...")
    
    # Employee Management
    def add_employee(self) -> None:
        """Add new employee."""
        self._show_header("ADD NEW EMPLOYEE")
        
        org_id = self._get_valid_org_id()
        if not org_id:
            return
        
        first_name = self._get_input("First Name")
        if not first_name:
            return
            
        last_name = self._get_input("Last Name")
        if not last_name:
            return
            
        position = self._get_input("Position")
        if not position:
            return
            
        phone = self._get_input("Phone", required=False)
        email = self._get_input("Email", required=False)
        
        emp_id = self._generate_id(self.employees)
        
        employee = {
            'id': emp_id,
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'phone': phone or '',
            'email': email or '',
            'organization_id': org_id,
            'created_at': datetime.now().isoformat()
        }
        
        self.employees[emp_id] = employee
        self._save_data('employees', self.employees)
        
        # Update organization employee count
        self.organizations[org_id]['employee_count'] = len([e for e in self.employees.values() if e['organization_id'] == org_id])
        self._save_data('organizations', self.organizations)
        
        self._show_success(f"Employee '{first_name} {last_name}' added with ID: {emp_id}")
        input("⏸️  Press Enter to continue...")
    
    def view_employees(self) -> None:
        """View all employees."""
        self._show_header("ALL EMPLOYEES")
        
        if not self.employees:
            print("📭 No employees found.")
            input("⏸️  Press Enter to continue...")
            return
        
        print("👥 EMPLOYEES:")
        print("─" * 90)
        print(f"{'ID':<4} {'Name':<25} {'Position':<20} {'Phone':<15} {'Organization':<25}")
        print("─" * 90)
        
        for emp in self.employees.values():
            org_name = self.organizations.get(emp['organization_id'], {}).get('name', 'Unknown')
            full_name = f"{emp['first_name']} {emp['last_name']}"
            print(f"{emp['id']:<4} {full_name:<25} {emp['position']:<20} {emp['phone']:<15} {org_name:<25}")
            
        input("\n⏸️  Press Enter to continue...")
    
    # Customer Management  
    def add_customer(self) -> None:
        """Add new customer."""
        self._show_header("ADD NEW CUSTOMER")
        
        org_id = self._get_valid_org_id()
        if not org_id:
            return
        
        name = self._get_input("Customer Name")
        if not name:
            return
            
        contact_person = self._get_input("Contact Person", required=False)
        phone = self._get_input("Phone", required=False)
        email = self._get_input("Email", required=False)
        address = self._get_input("Address", required=False)
        
        cust_id = self._generate_id(self.customers)
        
        customer = {
            'id': cust_id,
            'name': name,
            'contact_person': contact_person or '',
            'phone': phone or '',
            'email': email or '',
            'address': address or '',
            'organization_id': org_id,
            'created_at': datetime.now().isoformat()
        }
        
        self.customers[cust_id] = customer
        self._save_data('customers', self.customers)
        
        # Update organization customer count
        self.organizations[org_id]['customer_count'] = len([c for c in self.customers.values() if c['organization_id'] == org_id])
        self._save_data('organizations', self.organizations)
        
        self._show_success(f"Customer '{name}' added with ID: {cust_id}")
        input("⏸️  Press Enter to continue...")
    
    def view_customers(self) -> None:
        """View all customers."""
        self._show_header("ALL CUSTOMERS")
        
        if not self.customers:
            print("📭 No customers found.")
            input("⏸️  Press Enter to continue...")
            return
        
        print("🤝 CUSTOMERS:")
        print("─" * 90)
        print(f"{'ID':<4} {'Name':<25} {'Contact':<20} {'Phone':<15} {'Organization':<25}")
        print("─" * 90)
        
        for cust in self.customers.values():
            org_name = self.organizations.get(cust['organization_id'], {}).get('name', 'Unknown')
            print(f"{cust['id']:<4} {cust['name']:<25} {cust['contact_person']:<20} {cust['phone']:<15} {org_name:<25}")
            
        input("\n⏸️  Press Enter to continue...")
    
    # Product Management
    def add_product(self) -> None:
        """Add new product."""
        self._show_header("ADD NEW PRODUCT")
        
        org_id = self._get_valid_org_id()
        if not org_id:
            return
        
        name = self._get_input("Product Name")
        if not name:
            return
            
        code = self._get_input("Product Code")
        if not code:
            return
            
        price = self._get_input("Price (EUR)", float)
        if price is None:
            return
            
        description = self._get_input("Description", required=False)
        manufacturer = self._get_input("Manufacturer", required=False)
        
        prod_id = self._generate_id(self.products)
        
        product = {
            'id': prod_id,
            'name': name,
            'code': code,
            'price': price,
            'description': description or '',
            'manufacturer': manufacturer or '',
            'organization_id': org_id,
            'created_at': datetime.now().isoformat()
        }
        
        self.products[prod_id] = product
        self._save_data('products', self.products)
        
        # Update organization product count
        self.organizations[org_id]['product_count'] = len([p for p in self.products.values() if p['organization_id'] == org_id])
        self._save_data('organizations', self.organizations)
        
        self._show_success(f"Product '{name}' added with ID: {prod_id}")
        input("⏸️  Press Enter to continue...")
    
    def view_products(self) -> None:
        """View all products."""
        self._show_header("ALL PRODUCTS")
        
        if not self.products:
            print("📭 No products found.")
            input("⏸️  Press Enter to continue...")
            return
        
        print("📦 PRODUCTS:")
        print("─" * 90)
        print(f"{'ID':<4} {'Name':<25} {'Code':<15} {'Price':<12} {'Organization':<25}")
        print("─" * 90)
        
        for prod in self.products.values():
            org_name = self.organizations.get(prod['organization_id'], {}).get('name', 'Unknown')
            price_str = f"€{prod['price']:.2f}"
            print(f"{prod['id']:<4} {prod['name']:<25} {prod['code']:<15} {price_str:<12} {org_name:<25}")
            
        input("\n⏸️  Press Enter to continue...")
    
    # Dashboard and Statistics
    def show_dashboard(self) -> None:
        """Display comprehensive dashboard."""
        self._show_header("📊 DASHBOARD")
        
        org_count = len(self.organizations)
        emp_count = len(self.employees)
        cust_count = len(self.customers)
        prod_count = len(self.products)
        
        print(f"🏢 Organizations: {org_count}")
        print(f"👥 Employees:     {emp_count}")
        print(f"🤝 Customers:     {cust_count}")
        print(f"📦 Products:      {prod_count}")
        print("─" * 40)
        
        if self.organizations:
            print("\n📈 ORGANIZATION BREAKDOWN:")
            for org in self.organizations.values():
                org_employees = len([e for e in self.employees.values() if e['organization_id'] == org['id']])
                org_customers = len([c for c in self.customers.values() if c['organization_id'] == org['id']])
                org_products = len([p for p in self.products.values() if p['organization_id'] == org['id']])
                
                print(f"\n🏢 {org['name']}:")
                print(f"   👥 Employees: {org_employees}")
                print(f"   🤝 Customers: {org_customers}")
                print(f"   📦 Products:  {org_products}")
        
        input("\n⏸️  Press Enter to continue...")
    
    def run(self) -> None:
        """Main application loop."""
        while True:
            self._show_header("🏢 CONTACT MANAGER 2.0")
            
            print("🎯 MAIN MENU")
            print("─" * 25)
            print("1️⃣  Organizations")
            print("2️⃣  Employees")
            print("3️⃣  Customers")
            print("4️⃣  Products")
            print("📊 Dashboard")
            print("5️⃣  Dashboard")
            print("0️⃣  Exit")
            print()
            
            choice = input("🎯 Select option: ").strip()
            
            if choice == '1':
                self._organization_menu()
            elif choice == '2':
                self._employee_menu()
            elif choice == '3':
                self._customer_menu()
            elif choice == '4':
                self._product_menu()
            elif choice == '5':
                self.show_dashboard()
            elif choice == '0':
                self._show_header("👋 THANK YOU!")
                print("Contact Manager 2.0")
                print("\n# ░█▀█░█░█░▀▀█░▀▀█░█▀▄")
                print("# ░█▀▀░░█░░▄▀░░░▀▄░█▀▄")
                print("# ░▀░░░░▀░░▀▀▀░▀▀░░▀░▀")
                break
            else:
                print("❌ Invalid option!")
                input("⏸️  Press Enter to continue...")
    
    def _organization_menu(self) -> None:
        """Organization management menu."""
        while True:
            self._show_header("🏢 ORGANIZATION MANAGEMENT")
            print("1️⃣  Add Organization")
            print("2️⃣  View All Organizations")
            print("3️⃣  Delete Organization")
            print("0️⃣  Back to Main Menu")
            print()
            
            choice = input("🎯 Select option: ").strip()
            
            if choice == '1':
                self.add_organization()
            elif choice == '2':
                self.view_organizations()
            elif choice == '3':
                self.delete_organization()
            elif choice == '0':
                break
            else:
                print("❌ Invalid option!")
                input("⏸️  Press Enter to continue...")
    
    def _employee_menu(self) -> None:
        """Employee management menu."""
        while True:
            self._show_header("👥 EMPLOYEE MANAGEMENT")
            print("1️⃣  Add Employee")
            print("2️⃣  View All Employees")
            print("0️⃣  Back to Main Menu")
            print()
            
            choice = input("🎯 Select option: ").strip()
            
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.view_employees()
            elif choice == '0':
                break
            else:
                print("❌ Invalid option!")
                input("⏸️  Press Enter to continue...")
    
    def _customer_menu(self) -> None:
        """Customer management menu."""
        while True:
            self._show_header("🤝 CUSTOMER MANAGEMENT")
            print("1️⃣  Add Customer")
            print("2️⃣  View All Customers")
            print("0️⃣  Back to Main Menu")
            print()
            
            choice = input("🎯 Select option: ").strip()
            
            if choice == '1':
                self.add_customer()
            elif choice == '2':
                self.view_customers()
            elif choice == '0':
                break
            else:
                print("❌ Invalid option!")
                input("⏸️  Press Enter to continue...")
    
    def _product_menu(self) -> None:
        """Product management menu."""
        while True:
            self._show_header("📦 PRODUCT MANAGEMENT")
            print("1️⃣  Add Product")
            print("2️⃣  View All Products")
            print("0️⃣  Back to Main Menu")
            print()
            
            choice = input("🎯 Select option: ").strip()
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.view_products()
            elif choice == '0':
                break
            else:
                print("❌ Invalid option!")
                input("⏸️  Press Enter to continue...")


def main() -> None:
    """Main entry point of the application."""
    try:
        manager = ContactManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue.")


if __name__ == "__main__":
    main()