# contacts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Contact
from .ml import auto_category
import json

def contact_list(request):
    """View to display all contacts"""
    contacts = Contact.objects.all().order_by('name')
    return render(request, "contacts/list.html", {"contacts": contacts})

def add_contact(request):
    """View to add a new contact"""
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST.get("email", "")
        notes = request.POST.get("notes", "")
        
        category = auto_category(name, notes)

        Contact.objects.create(
            name=name,
            phone=phone,
            email=email,
            notes=notes,
            category=category
        )
        return redirect("contact_list")

    return render(request, "contacts/add.html")

def update_contact(request, contact_id):  # THIS IS THE CORRECT FUNCTION NAME
    """View to handle AJAX updates for inline editing"""
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == "POST":
        try:
            # Get JSON data from AJAX request
            data = json.loads(request.body)
            
            # Update fields
            contact.name = data.get('name', contact.name)
            contact.phone = data.get('phone', contact.phone)
            contact.email = data.get('email', contact.email)
            contact.notes = data.get('notes', contact.notes)
            
            # Re-categorize with ML
            contact.category = auto_category(contact.name, contact.notes)
            
            contact.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Contact updated successfully',
                'category': contact.category
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def delete_contact(request, contact_id):
    """View to delete a contact"""
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    return redirect("contact_list")