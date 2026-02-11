from django.test import TestCase, Client
from django.urls import reverse
from .models import Contact
from .ml import auto_category
import json

class MLCategorizationTests(TestCase):
    """Tests for the ML-based auto-categorization logic"""

    def test_personal_love_keywords(self):
        """Test if love/relationship keywords return 'Personal'"""
        self.assertEqual(auto_category("Joyce", "Babe love of my life ❤️"), "Personal")
        self.assertEqual(auto_category("John", "My darling honey"), "Personal")
        self.assertEqual(auto_category("Significant Other", ""), "Personal")

    def test_family_keywords(self):
        """Test if family keywords return 'Family'"""
        self.assertEqual(auto_category("Mom", "Call every Sunday"), "Family")
        self.assertEqual(auto_category("Uncle Bob", ""), "Family")
        self.assertEqual(auto_category("Cousin Mike", "Birthday party"), "Family")

    def test_work_keywords(self):
        """Test if work keywords return 'Work'"""
        self.assertEqual(auto_category("Boss", "Meeting at 9"), "Work")
        self.assertEqual(auto_category("HR Team", "Contract details"), "Work")
        self.assertEqual(auto_category("Manager Sarah", ""), "Work")

    def test_education_keywords(self):
        """Test if education keywords return 'Education'"""
        self.assertEqual(auto_category("Professor Lee", "Math assignment"), "Education")
        self.assertEqual(auto_category("School Office", "Enrollment"), "Education")
        self.assertEqual(auto_category("Classmate", ""), "Education")

    def test_health_keywords(self):
        """Test if health keywords return 'Health'"""
        self.assertEqual(auto_category("Dr. Smith", "Checkup"), "Health")
        self.assertEqual(auto_category("Pharmacy", "Refill prescription"), "Health")
        self.assertEqual(auto_category("Hospital", ""), "Health")

    def test_default_personal(self):
        """Test if unknown terms default to 'Personal'"""
        self.assertEqual(auto_category("Random Person", "Met at the park"), "Personal")
        self.assertEqual(auto_category("John Doe", ""), "Personal")

class ContactModelTests(TestCase):
    """Tests for the Contact model"""

    def test_contact_creation(self):
        """Test creating a contact and its string representation"""
        contact = Contact.objects.create(
            name="Test User",
            phone="123456789",
            email="test@example.com",
            notes="Work colleague",
            category="Work"
        )
        self.assertEqual(str(contact), "Test User")
        self.assertEqual(contact.category, "Work")

    def test_to_dict(self):
        """Test the to_dict method"""
        contact = Contact.objects.create(
            name="Test User",
            phone="123456789",
            email="test@example.com",
            notes="Something",
            category="Personal"
        )
        expected_dict = {
            "name": "Test User",
            "phone": "123456789",
            "email": "test@example.com",
            "notes": "Something",
            "category": "Personal",
        }
        self.assertEqual(contact.to_dict(), expected_dict)

class ContactViewTests(TestCase):
    """Tests for the Contact views"""

    def setUp(self):
        self.client = Client()
        self.contact = Contact.objects.create(
            name="Existing Contact",
            phone="987654321",
            notes="Initial notes"
        )

    def test_contact_list_view(self):
        """Test the contact list page"""
        response = self.client.get(reverse('contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/list.html')
        self.assertContains(response, "Existing Contact")

    def test_add_contact_view(self):
        """Test adding a contact via POST"""
        response = self.client.post(reverse('add_contact'), {
            'name': 'New Contact',
            'phone': '111222333',
            'email': 'new@example.com',
            'notes': 'New Notes'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Contact.objects.filter(name='New Contact').exists())
        
        # Check auto-categorization in view
        new_contact = Contact.objects.get(name='New Contact')
        self.assertEqual(new_contact.category, 'Personal')

    def test_update_contact_view_ajax(self):
        """Test updating a contact via AJAX POST"""
        url = reverse('update_contact', args=[self.contact.id])
        data = {
            'name': 'Updated Name',
            'notes': 'Working on a project'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_res = response.json()
        self.assertTrue(json_res['success'])
        
        # Verify database update
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'Updated Name')
        self.assertEqual(self.contact.category, 'Work')  # 'project' keyword in notes

    def test_delete_contact_view(self):
        """Test deleting a contact"""
        url = reverse('delete_contact', args=[self.contact.id])
        response = self.client.get(url)  # View uses redirect, usually should be POST but currently GET
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())
