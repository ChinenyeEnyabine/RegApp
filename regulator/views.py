from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Regulation, RegulationType, IndustrySector, Regulator, Technology

# def regulation_list(request):
#     # Extract filters from GET request
#     query = request.GET.get('q', '')
#     regulation_type_id = request.GET.get('regulation_type')
#     jurisdiction = request.GET.get('jurisdiction')
#     industry_sector_id = request.GET.get('industry_sector')
#     regulator_id = request.GET.get('regulator')

#     # Filter queryset based on GET parameters
#     regulations = Regulation.objects.all()

#     if query:
#         regulations = regulations.filter(title__icontains=query)

#     if regulation_type_id:
#         regulations = regulations.filter(regulation_type_id=regulation_type_id)

#     if jurisdiction:
#         # Filter by jurisdiction through related Regulator model
#         regulations = regulations.filter(regulators__jurisdiction=jurisdiction)

#     if industry_sector_id:
#         regulations = regulations.filter(industry_sector_id=industry_sector_id)

#     if regulator_id:
#         regulations = regulations.filter(regulators__id=regulator_id)

#     # Add ordering to the queryset to avoid pagination warnings
#     regulations = regulations.order_by('title')  # You can choose a different field if needed

#     # Pagination
#     paginator = Paginator(regulations, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Get distinct values for filter fields
#     regulator_types = RegulationType.objects.all()
#     jurisdictions = Regulator.objects.values_list('jurisdiction', flat=True).distinct()
#     industry_sectors = IndustrySector.objects.all()
#     regulators = Regulator.objects.all()

#     context = {
#         'query': query,
#         'regulation_types': regulator_types,
#         'jurisdictions': jurisdictions,
#         'industry_sectors': industry_sectors,
#         'regulators': regulators,
#         'page_obj': page_obj,
#     }

#     return render(request, 'regulations/regulation_list.html', context)
# views.py

# from django.core.paginator import Paginator
# from django.shortcuts import render
# from .models import Regulation, RegulationType, IndustrySector, Regulator, Technology

def regulation_list(request):
    # Extract filters from GET request
    query = request.GET.get('q', '')
    regulation_type_id = request.GET.get('regulation_type')
    jurisdiction = request.GET.get('jurisdiction')
    industry_sector_id = request.GET.get('industry_sector')
    regulator_id = request.GET.get('regulator')

    # Filter queryset based on GET parameters
    regulations = Regulation.objects.all()

    if query:
        regulations = regulations.filter(title__icontains=query)

    if regulation_type_id:
        regulations = regulations.filter(regulation_type_id=regulation_type_id)

    if jurisdiction:
        # Filter by jurisdiction through related Regulator model
        regulations = regulations.filter(regulators__jurisdiction=jurisdiction)

    if industry_sector_id:
        regulations = regulations.filter(industry_sector_id=industry_sector_id)

    if regulator_id:
        regulations = regulations.filter(regulators__id=regulator_id)

    # Add ordering to the queryset to avoid pagination warnings
    regulations = regulations.order_by('title')  # You can choose a different field if needed

    # Pagination
    paginator = Paginator(regulations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get distinct values for filter fields
    regulation_types = RegulationType.objects.all().order_by('name')
    jurisdictions = Regulator.objects.values_list('jurisdiction', flat=True).distinct().order_by('jurisdiction')
    industry_sectors = IndustrySector.objects.all().order_by('name')
    regulators = Regulator.objects.all().order_by('name')

    context = {
        'query': query,
        'regulation_types': regulation_types,
        'jurisdictions': jurisdictions,
        'industry_sectors': industry_sectors,
        'regulators': regulators,
        'page_obj': page_obj,
    }

    return render(request, 'regulations/regulation_list.html', context)


def regulation_detail(request, pk):
    regulation = get_object_or_404(Regulation, pk=pk)
    return render(request, 'regulations/regulation_detail.html', {'regulation': regulation})

def regulation_detail_pdf(request, pk):
    regulation = get_object_or_404(Regulation, pk=pk)
    template_path = 'regulations/regulation_detail_pdf.html'
    context = {'regulation': regulation}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="regulation_{regulation.title}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Regulator

def regulator_list(request):
    # Extract filters from GET request
    query = request.GET.get('q', '')

    # Filter queryset based on GET parameters
    regulators = Regulator.objects.all()

    if query:
        regulators = regulators.filter(name__icontains=query)

    # Pagination
    paginator = Paginator(regulators, 10)  # Show 10 regulators per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
    }

    return render(request, 'regulators/regulator_list.html', context)

def regulator_detail(request, pk):
    regulator = get_object_or_404(Regulator, pk=pk)
    return render(request, 'regulators/regulator_detail.html', {'regulator': regulator})
