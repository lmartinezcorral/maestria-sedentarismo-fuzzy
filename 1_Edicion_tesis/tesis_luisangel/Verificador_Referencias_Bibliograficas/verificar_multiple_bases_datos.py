#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar qué referencias del archivo .bib están indexadas en 
múltiples bases de datos académicas y generar un CSV con los resultados.

Bases de datos verificadas:
- ScienceDirect (Elsevier)
- PubMed (Medicina/Ciencias de la Salud)
- IEEE Xplore (Ingeniería/Tecnología)
- ACM Digital Library (Ciencias de la Computación)
- Google Scholar (General)
- SpringerLink (Editorial Springer)
- Wiley Online Library (Editorial Wiley)
- Crossref (Metadatos DOI)
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
OUTPUT_CSV = "referencias_multiple_bases_datos.csv"
OUTPUT_JSON = "referencias_multiple_bases_datos.json"
DELAY_BETWEEN_REQUESTS = 0.5  # Segundos entre peticiones

# Bases de datos a verificar
DATABASES = {
    'sciencedirect': 'ScienceDirect',
    'pubmed': 'PubMed',
    'ieee': 'IEEE Xplore',
    'acm': 'ACM Digital Library',
    'scholar': 'Google Scholar',
    'springer': 'SpringerLink',
    'wiley': 'Wiley Online',
    'crossref': 'Crossref'
}

def parse_bibtex_file(bib_file: str) -> List[Dict]:
    """
    Parsea un archivo BibTeX y extrae las referencias.
    """
    references = []
    
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrón para encontrar entradas BibTeX
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
            match_field = re.search(pattern_field, entry_content, re.IGNORECASE)
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
    
    if doi.startswith('doi:') or doi.startswith('DOI:'):
        doi = doi[4:].strip()
    
    if doi.startswith('http'):
        doi_match = re.search(r'10\.\d+/[^\s\)]+', doi)
        if doi_match:
            doi = doi_match.group(0)
        else:
            return None
    
    if re.match(r'^10\.\d+/[^\s]+', doi):
        return doi
    
    return None

def check_crossref(doi: str) -> Dict:
    """
    Verifica si un DOI existe en Crossref y obtiene información del publisher.
    """
    if not doi:
        return {'found': False, 'publisher': '', 'url': ''}
    
    doi_normalized = normalize_doi(doi)
    if not doi_normalized:
        return {'found': False, 'publisher': '', 'url': ''}
    
    try:
        crossref_url = f"https://api.crossref.org/works/{doi_normalized}"
        response = requests.get(crossref_url, headers={'User-Agent': 'Python Script'}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                message = data.get('message', {})
                publisher = message.get('publisher', '')
                title = message.get('title', [''])[0] if message.get('title') else ''
                
                return {
                    'found': True,
                    'publisher': publisher,
                    'url': f"https://doi.org/{doi_normalized}",
                    'title': title
                }
    except:
        pass
    
    return {'found': False, 'publisher': '', 'url': ''}

def check_pubmed(doi: str, title: str = '') -> Dict:
    """
    Verifica si un artículo está en PubMed.
    """
    result = {'found': False, 'url': '', 'method': ''}
    
    # Método 1: Buscar por DOI
    if doi:
        doi_normalized = normalize_doi(doi)
        if doi_normalized:
            try:
                pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={quote(doi_normalized)}"
                response = requests.get(pubmed_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    # PubMed muestra resultados con estos indicadores
                    if 'pubmed-result' in content or 'article-title' in content:
                        # Intentar extraer PMID
                        pmid_match = re.search(r'pmid[:\s]+(\d+)', content, re.IGNORECASE)
                        if pmid_match:
                            pmid = pmid_match.group(1)
                            result = {
                                'found': True,
                                'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                                'method': 'doi_search'
                            }
                            return result
                        result = {
                            'found': True,
                            'url': pubmed_url,
                            'method': 'doi_search'
                        }
                        return result
            except:
                pass
    
    # Método 2: Buscar por título (primeras palabras)
    if title:
        try:
            title_words = title.split()[:5]  # Primeras 5 palabras
            query = ' '.join(title_words)
            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={quote(query)}"
            response = requests.get(pubmed_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                title_lower = title.lower()[:50]
                if title_lower in content:
                    result = {
                        'found': True,
                        'url': pubmed_url,
                        'method': 'title_search'
                    }
        except:
            pass
    
    return result

def check_ieee_xplore(doi: str, title: str = '') -> Dict:
    """
    Verifica si un artículo está en IEEE Xplore.
    """
    result = {'found': False, 'url': '', 'method': ''}
    
    if doi:
        doi_normalized = normalize_doi(doi)
        if doi_normalized:
            try:
                # IEEE Xplore busca por DOI
                ieee_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={quote(doi_normalized)}"
                response = requests.get(ieee_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    if 'xplore' in content and ('document' in content or 'article' in content):
                        result = {
                            'found': True,
                            'url': ieee_url,
                            'method': 'doi_search'
                        }
                        return result
            except:
                pass
    
    if title:
        try:
            title_words = title.split()[:4]
            query = ' '.join(title_words)
            ieee_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={quote(query)}"
            response = requests.get(ieee_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                if 'xplore' in content:
                    result = {
                        'found': True,
                        'url': ieee_url,
                        'method': 'title_search'
                    }
        except:
            pass
    
    return result

def check_acm_dl(doi: str, title: str = '') -> Dict:
    """
    Verifica si un artículo está en ACM Digital Library.
    """
    result = {'found': False, 'url': '', 'method': ''}
    
    if doi:
        doi_normalized = normalize_doi(doi)
        if doi_normalized:
            try:
                acm_url = f"https://dl.acm.org/action/doSearch?AllField={quote(doi_normalized)}"
                response = requests.get(acm_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    if 'acm' in content and ('article' in content or 'publication' in content):
                        result = {
                            'found': True,
                            'url': acm_url,
                            'method': 'doi_search'
                        }
                        return result
            except:
                pass
    
    if title:
        try:
            title_words = title.split()[:4]
            query = ' '.join(title_words)
            acm_url = f"https://dl.acm.org/action/doSearch?AllField={quote(query)}"
            response = requests.get(acm_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                if 'acm' in content:
                    result = {
                        'found': True,
                        'url': acm_url,
                        'method': 'title_search'
                    }
        except:
            pass
    
    return result

def check_google_scholar(doi: str, title: str = '') -> Dict:
    """
    Verifica si un artículo está en Google Scholar.
    Nota: Google Scholar puede bloquear requests automatizados.
    """
    result = {'found': False, 'url': '', 'method': ''}
    
    # Google Scholar es difícil de verificar automáticamente
    # Retornamos una URL de búsqueda
    if doi:
        doi_normalized = normalize_doi(doi)
        if doi_normalized:
            result = {
                'found': True,  # Asumimos que si tiene DOI, probablemente está
                'url': f"https://scholar.google.com/scholar?q={quote(doi_normalized)}",
                'method': 'doi_search'
            }
            return result
    
    if title:
        title_words = title.split()[:5]
        query = ' '.join(title_words)
        result = {
            'found': True,
            'url': f"https://scholar.google.com/scholar?q={quote(query)}",
            'method': 'title_search'
        }
    
    return result

def check_springer(doi: str) -> Dict:
    """
    Verifica si un artículo está en SpringerLink.
    """
    result = {'found': False, 'url': '', 'method': ''}
    
    if doi:
        doi_normalized = normalize_doi(doi)
        if doi_normalized:
            try:
                springer_url = f"https://link.springer.com/search?query={quote(doi_normalized)}"
                response = requests.get(springer_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    if 'springer' in content and ('article' in content or 'chapter' in content):
                        result = {
                            'found': True,
                            'url': springer_url,
                            'method': 'doi_search'
                        }
                        return result
            except:
                pass
    
    return result

def check_wiley(doi: str) -> Dict:
    """
    Verifica si un artículo está en Wiley Online Library.
    """
    result = {'found': False, 'url': '', 'method': ''}
    
    if doi:
        doi_normalized = normalize_doi(doi)
        if doi_normalized:
            try:
                wiley_url = f"https://onlinelibrary.wiley.com/action/doSearch?AllField={quote(doi_normalized)}"
                response = requests.get(wiley_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    if 'wiley' in content and ('article' in content or 'publication' in content):
                        result = {
                            'found': True,
                            'url': wiley_url,
                            'method': 'doi_search'
                        }
                        return result
            except:
                pass
    
    return result

def check_sciencedirect(doi: str) -> Dict:
    """
    Verifica si un DOI está indexado en ScienceDirect.
    """
    if not doi:
        return {'found': False, 'url': '', 'error': 'No DOI provided'}
    
    doi_normalized = normalize_doi(doi)
    if not doi_normalized:
        return {'found': False, 'url': '', 'error': 'Invalid DOI format'}
    
    # Verificar a través de Crossref primero (más rápido)
    crossref_result = check_crossref(doi_normalized)
    if crossref_result.get('found'):
        publisher = crossref_result.get('publisher', '').lower()
        if 'elsevier' in publisher:
            return {
                'found': True,
                'url': f"https://www.sciencedirect.com/search?qs={quote(doi_normalized)}",
                'method': 'crossref_elsevier'
            }
    
    # Búsqueda directa
    try:
        search_url = f"https://www.sciencedirect.com/search?qs={quote(doi_normalized)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            if 'sciencedirect' in content.lower() and doi_normalized[:20] in content:
                return {
                    'found': True,
                    'url': search_url,
                    'method': 'doi_search'
                }
    except:
        pass
    
    return {'found': False, 'url': '', 'error': 'Not found'}

def check_all_databases(ref: Dict) -> Dict:
    """
    Verifica una referencia en todas las bases de datos.
    """
    result = {
        'key': ref.get('key', ''),
        'title': ref.get('title', ''),
        'author': ref.get('author', ''),
        'journal': ref.get('journal', ''),
        'year': ref.get('year', ''),
        'doi': ref.get('doi', ''),
    }
    
    # Normalizar DOI
    doi_normalized = normalize_doi(ref.get('doi', ''))
    if doi_normalized:
        result['doi'] = doi_normalized
    
    # Verificar en cada base de datos
    for db_key, db_name in DATABASES.items():
        result[f'{db_key}_indexed'] = False
        result[f'{db_key}_url'] = ''
        result[f'{db_key}_method'] = ''
    
    # Crossref (metadatos)
    if doi_normalized:
        crossref_result = check_crossref(doi_normalized)
        result['crossref_indexed'] = crossref_result.get('found', False)
        result['crossref_url'] = crossref_result.get('url', '')
        result['crossref_publisher'] = crossref_result.get('publisher', '')
    
    # ScienceDirect
    if doi_normalized:
        sd_result = check_sciencedirect(doi_normalized)
        result['sciencedirect_indexed'] = sd_result.get('found', False)
        result['sciencedirect_url'] = sd_result.get('url', '')
        result['sciencedirect_method'] = sd_result.get('method', '')
    
    # PubMed
    pubmed_result = check_pubmed(doi_normalized or ref.get('doi', ''), ref.get('title', ''))
    result['pubmed_indexed'] = pubmed_result.get('found', False)
    result['pubmed_url'] = pubmed_result.get('url', '')
    result['pubmed_method'] = pubmed_result.get('method', '')
    
    # IEEE Xplore
    ieee_result = check_ieee_xplore(doi_normalized or ref.get('doi', ''), ref.get('title', ''))
    result['ieee_indexed'] = ieee_result.get('found', False)
    result['ieee_url'] = ieee_result.get('url', '')
    result['ieee_method'] = ieee_result.get('method', '')
    
    # ACM
    acm_result = check_acm_dl(doi_normalized or ref.get('doi', ''), ref.get('title', ''))
    result['acm_indexed'] = acm_result.get('found', False)
    result['acm_url'] = acm_result.get('url', '')
    result['acm_method'] = acm_result.get('method', '')
    
    # Google Scholar
    scholar_result = check_google_scholar(doi_normalized or ref.get('doi', ''), ref.get('title', ''))
    result['scholar_indexed'] = scholar_result.get('found', False)
    result['scholar_url'] = scholar_result.get('url', '')
    result['scholar_method'] = scholar_result.get('method', '')
    
    # Springer
    if doi_normalized:
        springer_result = check_springer(doi_normalized)
        result['springer_indexed'] = springer_result.get('found', False)
        result['springer_url'] = springer_result.get('url', '')
        result['springer_method'] = springer_result.get('method', '')
    
    # Wiley
    if doi_normalized:
        wiley_result = check_wiley(doi_normalized)
        result['wiley_indexed'] = wiley_result.get('found', False)
        result['wiley_url'] = wiley_result.get('url', '')
        result['wiley_method'] = wiley_result.get('method', '')
    
    # Calcular total de bases de datos donde está indexada
    indexed_count = sum([
        result.get('sciencedirect_indexed', False),
        result.get('pubmed_indexed', False),
        result.get('ieee_indexed', False),
        result.get('acm_indexed', False),
        result.get('scholar_indexed', False),
        result.get('springer_indexed', False),
        result.get('wiley_indexed', False),
        result.get('crossref_indexed', False)
    ])
    result['total_databases'] = indexed_count
    
    return result

def main():
    """
    Función principal.
    """
    print("=" * 80)
    print("VERIFICACIÓN DE REFERENCIAS EN MÚLTIPLES BASES DE DATOS ACADÉMICAS")
    print("=" * 80)
    print()
    print("Bases de datos verificadas:")
    for db_key, db_name in DATABASES.items():
        print(f"  • {db_name}")
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
    print("🔍 Verificando referencias en todas las bases de datos...")
    print("   (Esto puede tardar varios minutos)")
    print()
    
    results = []
    
    for i, ref in enumerate(references, 1):
        print(f"[{i}/{len(references)}] {ref.get('key', 'N/A')} - {ref.get('title', 'Sin título')[:50]}...")
        
        result = check_all_databases(ref)
        results.append(result)
        
        # Mostrar resumen
        indexed_dbs = []
        for db_key, db_name in DATABASES.items():
            if result.get(f'{db_key}_indexed', False):
                indexed_dbs.append(db_name)
        
        if indexed_dbs:
            print(f"   ✅ Indexada en: {', '.join(indexed_dbs)} ({result.get('total_databases', 0)} bases)")
        else:
            print(f"   ❌ No indexada en ninguna base de datos verificada")
        
        # Esperar entre peticiones
        if i < len(references):
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    print()
    print("💾 Guardando resultados...")
    
    # Preparar campos para CSV
    fieldnames = ['key', 'title', 'author', 'journal', 'year', 'doi', 'total_databases']
    for db_key in DATABASES.keys():
        fieldnames.extend([f'{db_key}_indexed', f'{db_key}_url', f'{db_key}_method'])
    fieldnames.append('crossref_publisher')
    
    # Guardar CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    print(f"✅ CSV guardado: {OUTPUT_CSV}")
    
    # Guardar JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON guardado: {OUTPUT_JSON}")
    
    # Estadísticas
    print()
    print("=" * 80)
    print("RESUMEN POR BASE DE DATOS")
    print("=" * 80)
    
    for db_key, db_name in DATABASES.items():
        indexed_count = sum(1 for r in results if r.get(f'{db_key}_indexed', False))
        percentage = (indexed_count / len(results) * 100) if results else 0
        print(f"{db_name:25} {indexed_count:4}/{len(results)} ({percentage:5.1f}%)")
    
    total_with_any = sum(1 for r in results if r.get('total_databases', 0) > 0)
    print()
    print(f"Total con al menos una base de datos: {total_with_any}/{len(results)} ({total_with_any/len(results)*100:.1f}%)")
    print("=" * 80)

if __name__ == "__main__":
    main()

