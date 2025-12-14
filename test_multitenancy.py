import unittest
from app import create_app, db
from app.models import User, Bank, LoanApplication

class MultiTenancyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = self.app.test_client()
        self.maxDiff = 50 # Reduce diff output
        
        with self.app.app_context():
            db.create_all()
            
            # Setup Banks
            bank_a = Bank(name="Bank A", settings='{"dti_threshold": 0.5}')
            bank_b = Bank(name="Bank B", settings='{"dti_threshold": 0.5}')
            db.session.add_all([bank_a, bank_b])
            db.session.commit()
            
            self.bank_a_id = bank_a.id
            self.bank_b_id = bank_b.id
            
            # Setup Users
            officer_a = User(name='Officer A', email='officer_a@bank.com', role='officer', bank_id=bank_a.id)
            officer_a.set_password('pass')
            
            officer_b = User(name='Officer B', email='officer_b@bank.com', role='officer', bank_id=bank_b.id)
            officer_b.set_password('pass')
            
            customer = User(name='Cust', email='cust@gmail.com', role='customer', bank_id=None)
            customer.set_password('pass')
            
            db.session.add_all([officer_a, officer_b, customer])
            db.session.commit()
            
            # Setup Application for Bank A
            app_a = LoanApplication(
                user_id=customer.id,
                bank_id=bank_a.id,
                income=50000,
                amount_requested=10000,
                purpose='Test',
                term_months=12,
                debt=0,
                status='Pending'
            )
            db.session.add(app_a)
            db.session.commit()
            
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        import os
        if os.path.exists('test.db'):
            os.remove('test.db')

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_officer_isolation(self):
        # Officer A should see App A
        self.login('officer_a@bank.com', 'pass')
        response = self.client.get('/officer/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'10,000', response.data, msg="Amount 10,000 not found") # Amount shows up formatted
        
        self.client.get('/logout')
        
        # Officer B should NOT see App A
        self.login('officer_b@bank.com', 'pass')
        response = self.client.get('/officer/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'10000', response.data)
        
    def test_customer_application(self):
        self.login('cust@gmail.com', 'pass')
        
        # Apply to Bank B
        response = self.client.post('/apply', data=dict(
            bank_id=self.bank_b_id,
            income=60000,
            amount=5000,
            term=24,
            debt=100,
            purpose='Car',
            credit_score=700
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Application submitted successfully!', response.data)
        
        # Logout and check if Officer B sees it
        self.client.get('/logout')
        self.login('officer_b@bank.com', 'pass')
        response = self.client.get('/officer/dashboard')
        self.assertIn(b'5,000', response.data, msg="Amount 5,000 not found")
        
    def test_dti_rejection(self):
        self.login('cust@gmail.com', 'pass')
        
        # High DTI: Income 1000/mo, Debt 0, Loan 600/mo -> DTI 0.6 > 0.5
        response = self.client.post('/apply', data=dict(
            bank_id=self.bank_a_id,
            income=12000, # 1000/mo
            amount=7200, # 600/mo for 12 mo
            term=12,
            debt=0,
            purpose='High Risk',
            credit_score=700
        ), follow_redirects=True)
        
        self.assertIn(b'Auto-Rejected', response.data)

if __name__ == '__main__':
    unittest.main()
