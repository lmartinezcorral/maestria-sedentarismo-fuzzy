#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar qué referencias del archivo .bib están indexadas en ScienceDirect
y generar un CSV con los resultados.
"""

import re
import csv
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote, urlencode

# Configuración
BIB_FILE = "referencias.bib"
OUTPUT_CSV = "referencias_sciencedirect.csv"
OUTPUT_JSON = "referencias_sciencedirect.json"
DELAY_BETWEEN_REQUESTS = 1  # Segundos entre peticiones para no sobrecargar el servidor


def parse_bibtex_file(bib_file: str) -> List[Dict]:
    """
    Parsea un archivo BibTeX y extrae las referencias.
    """
    references = []

    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patrón para encontrar entradas BibTeX
    pattern = r'@(\w+)\{([^,]+),\s*([^}]+)\}'

    # Encontrar todas las entradas
    entries = re.finditer(r'@(\w+)\{([^,]+),', content)

    for match in entries:
        entry_type = match.group(1)
        entry_key = match.group(2)

        # Encontrar el contenido de la entrada
        start_pos = match.end()
        brace_count = 1
        pos = start_pos

        while pos < len(content) and brace_count > 0:
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
            pos += 1

        entry_content = content[start_pos:pos-1]

        # Extraer campos
        ref = {
            'key': entry_key,
            'type': entry_type,
            'title': '',
            'author': '',
            'journal': '',
            'year': '',
            'doi': '',
            'url': ''
        }

        # Extraer campos comunes
        for field in ['title', 'author', 'journal', 'year', 'doi', 'url']:
            pattern_field = rf'{field}\s*=\s*\{{([^}}]+)\}}'
            match_field = re.search(
                pattern_field, entry_content, re.IGNORECASE)
            if match_field:
                ref[field] = match_field.group(1).strip()

        # Limpiar campos
        for key in ref:
            if isinstance(ref[key], str):
                ref[key] = ref[key].replace('{', '').replace('}', '').strip()

        references.append(ref)

    return references


def normalize_doi(doi: str) -> Optional[str]:
    """
    Normaliza un DOI a su formato estándar.
    """
    if not doi:
        return None

    doi = doi.strip()

    # Remover prefijos comunes
    if doi.startswith('doi:'):
        doi = doi[4:].strip()
    if doi.startswith('DOI:'):
        doi = doi[4:].strip()

    # Extraer DOI de URLs
    if doi.startswith('http'):
        doi_match = re.search(r'10\.\d+/[^\s\)]+', doi)
        if doi_match:
            doi = doi_match.group(0)
        else:
            return None

    # Verificar formato válido
    if re.match(r'^10\.\d+/[^\s]+', doi):
        return doi

    return None


def check_doi_in_sciencedirect(doi: str) -> Dict:
    """
    Verifica si un DOI está indexado en ScienceDirect.
    Usa múltiples métodos para mayor confiabilidad.
    """
    if not doi:
        return {'found': False, 'url': '', 'error': 'No DOI provided'}

    doi_normalized = normalize_doi(doi)
    if not doi_normalized:
        return {'found': False, 'url': '', 'error': 'Invalid DOI format'}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    # Método 1: Búsqueda directa en ScienceDirect
    search_url = f"https://www.sciencedirect.com/search?qs={quote(doi_normalized)}"

    try:
        response = requests.get(
            search_url, headers=headers, timeout=15, allow_redirects=True)

        if response.status_code == 200:
            content = response.text

            # Buscar indicadores de artículo encontrado
            # ScienceDirect muestra resultados con estos patrones
            patterns = [
                r'data-doi=["\']' + re.escape(doi_normalized) + r'["\']',
                r'href=["\'][^"\']*sciencedirect[^"\']*' +
                re.escape(doi_normalized.replace('/', r'[/_]')),
                r'article-title[^>]*>.*?' + re.escape(doi_normalized[:20]),
            ]

            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    # Intentar extraer URL del artículo
                    url_match = re.search(
                        r'href=["\'](https://www\.sciencedirect\.com/science/article/[^"\']+)["\']', content)
                    if url_match:
                        return {
                            'found': True,
                            'url': url_match.group(1),
                            'method': 'doi_search'
                        }
                    return {
                        'found': True,
                        'url': search_url,
                        'method': 'doi_search'
                    }
    except requests.exceptions.RequestException as e:
        pass

    # Método 2: Verificar a través de Crossref (muchos artículos de ScienceDirect están en Crossref)
    try:
        crossref_url = f"https://api.crossref.org/works/{doi_normalized}"
        crossref_response = requests.get(
            crossref_url, headers={'User-Agent': 'Python Script'}, timeout=10)

        if crossref_response.status_code == 200:
            data = crossref_response.json()
            if data.get('status') == 'ok':
                message = data.get('message', {})
                # Verificar si el publisher es Elsevier (ScienceDirect es de Elsevier)
                publisher = message.get('publisher', '').lower()
                if 'elsevier' in publisher:
                    # Construir URL probable de ScienceDirect
                    title = message.get('title', [''])[
                        0] if message.get('title') else ''
                    return {
                        'found': True,
                        'url': f"https://www.sciencedirect.com/search?qs={quote(doi_normalized)}",
                        'method': 'crossref_elsevier'
                    }
    except:
        pass

    # Método 3: Búsqueda por DOI en el sitio de ScienceDirect usando diferentes formatos
    try:
        # Intentar diferentes formatos de URL
        test_urls = [
            f"https://www.sciencedirect.com/science/article/pii/{doi_normalized.replace('/', '_')}",
            f"https://www.sciencedirect.com/science/article/abs/pii/{doi_normalized.replace('/', '_')}",
        ]

        for test_url in test_urls:
            test_response = requests.head(
                test_url, headers=headers, timeout=10, allow_redirects=True)
            if test_response.status_code == 200 and 'sciencedirect.com' in test_response.url:
                return {
                    'found': True,
                    'url': test_response.url,
                    'method': 'direct_url'
                }
    except:
        pass

    return {
        'found': False,
        'url': '',
        'error': 'Not found in ScienceDirect'
    }


def search_sciencedirect_by_title(title: str, author: str = '') -> Dict:
    """
    Busca un artículo en ScienceDirect usando título y autor.
    """
    if not title:
        return {'found': False, 'url': '', 'error': 'No title provided'}

    # Construir query de búsqueda
    query = title[:100]  # Limitar longitud
    if author:
        query = f"{author} {title}"[:100]

    search_url = f"https://www.sciencedirect.com/search?qs={quote(query)}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(search_url, headers=headers, timeout=10)

        if response.status_code == 200:
            content = response.text.lower()
            title_lower = title.lower()[:50]  # Primeros 50 caracteres

            # Buscar el título en los resultados
            if title_lower in content:
                return {
                    'found': True,
                    'url': search_url,
                    'method': 'title_search'
                }
            else:
                return {
                    'found': False,
                    'url': '',
                    'error': 'Title not found in search results'
                }
        else:
            return {
                'found': False,
                'url': '',
                'error': f'HTTP {response.status_code}'
            }

    except requests.exceptions.RequestException as e:
        return {
            'found': False,
            'url': '',
            'error': str(e)
        }


def check_reference_in_sciencedirect(ref: Dict) -> Dict:
    """
    Verifica si una referencia está indexada en ScienceDirect.
    """
    result = {
        'key': ref.get('key', ''),
        'title': ref.get('title', ''),
        'author': ref.get('author', ''),
        'journal': ref.get('journal', ''),
        'year': ref.get('year', ''),
        'doi': ref.get('doi', ''),
        'indexed': False,
        'url': '',
        'method': '',
        'error': ''
    }

    # Normalizar DOI si existe
    doi_normalized = normalize_doi(ref.get('doi', ''))
    if doi_normalized:
        result['doi'] = doi_normalized

    # Intentar primero con DOI (más confiable)
    if doi_normalized:
        doi_result = check_doi_in_sciencedirect(doi_normalized)
        result['indexed'] = doi_result.get('found', False)
        result['url'] = doi_result.get('url', '')
        result['method'] = doi_result.get('method', '')
        result['error'] = doi_result.get('error', '')

        if result['indexed']:
            return result

    # Si no se encontró con DOI, intentar con título
    if ref.get('title') and not result['indexed']:
        title_result = search_sciencedirect_by_title(
            ref['title'], ref.get('author', ''))
        result['indexed'] = title_result.get('found', False)
        if not result['url']:
            result['url'] = title_result.get('url', '')
        if not result['method']:
            result['method'] = title_result.get('method', '')
        if not result['error']:
            result['error'] = title_result.get('error', '')

    return result


def main():
    """
    Función principal.
    """
    print("=" * 70)
    print("VERIFICACIÓN DE REFERENCIAS EN SCIENCEDIRECT")
    print("=" * 70)
    print()

    # Verificar que el archivo .bib existe
    bib_path = Path(BIB_FILE)
    if not bib_path.exists():
        print(f"❌ Error: No se encontró el archivo {BIB_FILE}")
        return

    print(f"📚 Leyendo referencias de {BIB_FILE}...")

    # Parsear referencias
    try:
        references = parse_bibtex_file(BIB_FILE)
        print(f"✅ Se encontraron {len(references)} referencias")
    except Exception as e:
        print(f"❌ Error al parsear el archivo .bib: {e}")
        return

    print()
    print("🔍 Verificando referencias en ScienceDirect...")
    print("   (Esto puede tardar varios minutos)")
    print()

    results = []

    for i, ref in enumerate(references, 1):
        print(f"[{i}/{len(references)}] Verificando: {ref.get('key', 'N/A')} - {ref.get('title', 'Sin título')[:50]}...")

        result = check_reference_in_sciencedirect(ref)
        results.append(result)

        if result['indexed']:
            print(f"   ✅ Indexada en ScienceDirect")
        else:
            print(f"   ❌ No indexada ({result.get('error', 'No encontrada')})")

        # Esperar entre peticiones para no sobrecargar el servidor
        if i < len(references):
            time.sleep(DELAY_BETWEEN_REQUESTS)

    print()
    print("💾 Guardando resultados...")

    # Guardar CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        if results:
            fieldnames = ['key', 'title', 'author', 'journal', 'year', 'doi',
                          'indexed', 'url', 'method', 'error']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    print(f"✅ CSV guardado: {OUTPUT_CSV}")

    # Guardar JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON guardado: {OUTPUT_JSON}")

    # Estadísticas
    indexed_count = sum(1 for r in results if r['indexed'])
    not_indexed_count = len(results) - indexed_count

    print()
    print("=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print(f"Total de referencias: {len(results)}")
    print(
        f"✅ Indexadas en ScienceDirect: {indexed_count} ({indexed_count/len(results)*100:.1f}%)")
    print(
        f"❌ No indexadas: {not_indexed_count} ({not_indexed_count/len(results)*100:.1f}%)")
    print("=" * 70)


if __name__ == "__main__":
    main()
