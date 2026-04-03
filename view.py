rom django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from .models import FinancialRecord
import json

# --- Requirement: Analytics & Summary ---
def financial_summary(request):
    # RBAC: Only Admins and Analysts can see the summary
    if not request.user.groups.filter(name__in=['Admin', 'Analyst']).exists():
        return JsonResponse({"error": "Unauthorized: Analytics restricted"}, status=403)

    data = FinancialRecord.objects.filter(user=request.user)
    
    # Requirement: Filtering logic
    category = request.GET.get('category')
    if category:
        data = data.filter(category=category)

    summary = data.values('record_type').annotate(total=Sum('amount'))
    return JsonResponse({"summary": list(summary)}, status=200)

# --- Requirement: CRUD Operations ---
def manage_record(request, pk=None):
    # RBAC: Only Admin can Create, Update, or Delete
    if request.method in ['POST', 'PUT', 'DELETE'] and not request.user.groups.filter(name='Admin').exists():
        return JsonResponse({"error": "Admin role required for changes"}, status=403)

    if request.method == 'GET':
        records = FinancialRecord.objects.filter(user=request.user).values()
        return JsonResponse(list(records), safe=False)

    if request.method == 'POST':
        # Requirement: Input Validation
        try:
            data = json.loads(request.body)
            if float(data['amount']) <= 0:
                return JsonResponse({"error": "Amount must be positive"}, status=400)
            
            record = FinancialRecord.objects.create(
                user=request.user,
                amount=data['amount'],
                record_type=data['record_type'],
                category=data['category'],
                description=data.get('description', '')
            )
            return JsonResponse({"success": "Record created", "id": record.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
