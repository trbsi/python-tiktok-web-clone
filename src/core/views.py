from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from app import settings
from src.core.utils import reverse_lazy_with_query


@require_GET
def legal_documents(request: HttpRequest) -> HttpResponse:
    document = request.GET.get('document')
    dir = Path(f'{settings.BASE_DIR}/static/legal_documents')
    files = []
    for file in dir.iterdir():
        if not file.is_file() or file.suffix != '.pdf':
            continue

        if document and document.lower() in file.name.lower():
            return redirect(f'/static/legal_documents/{file.name}')

        file_name = (
            file.name
            .replace('_', ' ')
            .replace('-', ' ')
            .replace('.pdf', '')
            .title())
        files.append({'file': file.name, 'name': file_name})

    return render(request, 'legal_documents.html', {'legal_documents': files})


@require_GET
def terms_of_use(request: HttpRequest) -> HttpResponse:
    return redirect(
        reverse_lazy_with_query(route_name='legal_documents', query_params={'document': 'terms_of_service'})
    )


@require_GET
def privacy_policy(request: HttpRequest) -> HttpResponse:
    return redirect(
        reverse_lazy_with_query(route_name='legal_documents', query_params={'document': 'privacy_policy'})
    )


@require_GET
def landing_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing_page.html')
