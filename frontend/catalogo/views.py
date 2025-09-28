from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from . utils import get_headers

API_URL = "http://api:8000/api/"

def login(request):
    if(request.method == "POST"):
        email = request.POST.get("email")
        senha = request.POST.get("password")
        CONTAINER_API = API_URL + 'token/'
        
        try:
            response = requests.post(CONTAINER_API, json={
                "username": email,
                "password": senha,
            })

            if response.status_code == 200:
                data = response.json()
                token = data['access']
                if token:
                    request.session['api_access'] = token
                    return redirect('catalogo:dashboard')
                else:
                    return render(request, 'catalogo/pages/login/index.html', {
                        'error': 'Token não recebido da API.'
                    })
            else:
                error = response.json()
                return render(request, 'catalogo/pages/login/index.html', {
                    'error': f"{error.get('detail', 'Erro desconhecido')}"
                })
        except Exception as e:
            raise e

    return render(request, 'catalogo/pages/login/index.html')

def logout(request):
    if 'api_access' in request.session:
        del request.session['api_access']

    return redirect('catalogo:login')

def dashboard(request):
    CONTAINER_API_CURSOS = API_URL + 'cursos/?ativo=true'
    CONTAINER_API_DISCIPLINAS = API_URL + 'disciplinas/?ativo=true'
    token = request.session.get('api_access')
    headers = get_headers(token)
    params = {"ativo": "true"}
    context = {}
    
    response = requests.get(CONTAINER_API_CURSOS, headers=headers, params=params)

    try:
       if response.status_code == 200:
        context["cursos"] = response.json()
       else:
           return redirect('catalogo:login')
    except Exception:
        context = {"error": "Não foi possível decodificar o JSON da API"}
    
    
    response = requests.get(CONTAINER_API_DISCIPLINAS, headers=headers, params=params)

    try:
       if response.status_code == 200:
        context["disciplinas"] = response.json()
       else:
           return redirect('catalogo:login')
    except Exception:
        context = {"error": "Não foi possível decodificar o JSON da API"}

    context = {"logout": bool(token), **context}
    return render(request, 'catalogo/pages/dashboard/index.html', context)


def perfis(request):
    CONTAINER_API = API_URL + 'perfis/'
    token = request.session.get('api_access')
    headers = get_headers(token)
    try:
        response = requests.get(CONTAINER_API, headers=headers)
    
        if response.status_code in (200, 201):
            data = response.json()
        else:
            return redirect('catalogo:login')
    except Exception as e:
        return render(request, 'catalogo/pages/perfis/index.html')
    return render(request, 'catalogo/pages/perfis/index.html', context=data)

def perfis_buscar(request):
    CONTAINER_API = API_URL + 'perfis/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    ativo = True if request.GET.get('ativo') == 'on' else False
    codigo = request.GET.get('codigo')
    search = request.GET.get('search')

    params = {}
    if ativo is not None:
        params['ativo'] = ativo
    if codigo:
        params['codigo'] = codigo
    if search:
        params['search'] = search

    try:
        response = requests.get(CONTAINER_API, headers=headers, params=params)
        print(response.status_code)
    
        if response.status_code in (200, 201):
            data = response.json()
        else:
            return redirect('catalogo:login')
    except Exception as e:
        return render(request, 'catalogo/pages/perfis/index.html')
    return render(request, 'catalogo/pages/perfis/index.html', context=data)

def perfil_detalhe(request, id):
    CONTAINER_API = API_URL + f'perfis/{id}/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    try:
        response = requests.get(CONTAINER_API, headers=headers)
        if response.status_code in (401, 403):
            return redirect('catalogo:login')
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/perfis/perfil/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception:
        data = {"error": "Erro desconhecido."}
        render(request, 'catalogo/pages/perfis/perfil/index.html')
    
    return render(request, 'catalogo/pages/perfis/perfil/index.html', context=data)

def editar_perfil(request, id):
    CONTAINER_API = API_URL + f'perfis/{id}/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    try:
        response = requests.get(CONTAINER_API, headers=headers)
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/perfis/editar_perfil/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception:
        data = {"error": "Erro desconhecido."}
        render(request, 'catalogo/pages/perfis/editar_perfil/index.html')
        
    if request.method == "POST":
        ativo = True if request.POST.get('ativo') == 'on' else False
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')

        try:
            response = requests.patch(CONTAINER_API, json={
                "ativo": ativo,
                "nome": nome,
                "tipo": tipo,
            }, headers=headers)

            if response.status_code in (401, 403):
                return redirect('catalogo:login')

            if response.status_code in (200, 201):
                data = response.json()
                return redirect('catalogo:perfis')
            else:
                data = {"error": response.json().get('detail', 'Erro desconhecido')}
                return render(request, 'catalogo/pages/perfis/editar_perfil/index.html', context=data)
            
        except Exception:
            data = {'error': "Erro ao acessar API"}
            return render(request, 'catalogo/pages/perfis/editar_perfil/index.html', context=data)
    else:
        return render(request, 'catalogo/pages/perfis/editar_perfil/index.html', context=data)

def criar_perfil(request):
    CONTAINER_API = API_URL + 'perfis/'
    token = request.session.get('api_access')
    headers = get_headers(token)
        
    if request.method == "POST":
        ativo = True if request.POST.get('ativo') == 'on' else False
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        tipo = request.POST.get('tipo')

        try:
            response = requests.post(CONTAINER_API, json={
                "ativo": ativo,
                "tipo": tipo,
                "nome": nome,
                "email": email,
                "password": senha,

            }, headers=headers)

            if response.status_code in (200, 201):
                data = response.json()
                return redirect('catalogo:perfis')
            else:
                data = {"error": response.json().get('detail', 'Erro desconhecido')}
                return render(request, 'catalogo/pages/perfis/novo_perfil/index.html', context=data)
            
        except Exception:
            data = {'error': "Erro ao acessar API"}
            return render(request, 'catalogo/pages/perfis/novo_perfil/index.html', context=data)
        
    return render(request, 'catalogo/pages/perfis/novo_perfil/index.html')
        
def inativar_perfil(request, id):
    CONTAINER_API = API_URL + f'perfis/{id}/inativar/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    response = requests.patch(CONTAINER_API, json={"ativo": False}, headers=headers)

    if response.status_code in (200, 204):
        return redirect('catalogo:perfis')
    else:
        return render(request, 'catalogo/pages/perfis/index.html', {
            'error': 'Erro ao inativar curso'
        })

def ativar_perfil(request, id):
    CONTAINER_API = API_URL + f'perfis/{id}/ativar/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    response = requests.patch(CONTAINER_API, json={"ativo": False}, headers=headers)

    if response.status_code in (200, 204):
        return redirect('catalogo:perfis')
    else:
        return render(request, 'catalogo/pages/perfis/index.html', {
            'error': 'Erro ao ativar curso'
        })


def cursos(request):
    CONTAINER_API = API_URL + 'cursos/'
    token = request.session.get('api_access')
    headers = get_headers(token)
    try:
        response = requests.get(CONTAINER_API, headers=headers)
        
        if response.status_code in (401, 403):
            return redirect('catalogo:login')
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/cursos/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception as e:
        return render(request, 'catalogo/pages/cursos/index.html')
    return render(request, 'catalogo/pages/cursos/index.html', context=data)

def cursos_resumo(request):
    return HttpResponse('Olá Mundo!')
     
def criar_curso(request):
    CONTAINER_API = API_URL + 'cursos/'
    token = request.session.get('api_access')
    headers = get_headers(token)
        
    if request.method == "POST":
        ativo = True if request.POST.get('ativo') == 'on' else False
        nome = request.POST.get('nome')
        sigla = request.POST.get('sigla')
        descricao = request.POST.get('descricao')
        carga_horaria = request.POST.get('carga-horaria')

        try:
            response = requests.post(CONTAINER_API, json={
                "ativo": ativo,
                "sigla": sigla,
                "nome": nome,
                "descricao": descricao,
                "carga_horaria_total": carga_horaria
            }, headers=headers)

            if response.status_code in (200, 201):
                data = response.json()
                return redirect('catalogo:dashboard')
            else:
                data = {"error": response.json().get('detail', 'Erro desconhecido')}
                return render(request, 'catalogo/pages/cursos/novo_curso/index.html', context=data)
            
        except Exception:
            data = {'error': "Erro ao acessar API"}
            return render(request, 'catalogo/pages/cursos/novo_curso/index.html', context=data)
        
    return render(request, 'catalogo/pages/cursos/novo_curso/index.html')

def editar_curso(request, id):
    CONTAINER_API = API_URL + f'cursos/{id}/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    try:
        response = requests.get(CONTAINER_API, headers=headers)
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/cursos/editar_curso/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception:
        data = {"error": "Erro desconhecido."}
        render(request, 'catalogo/pages/cursos/editar_curso/index.html')
        
    if request.method == "POST":
        ativo = True if request.POST.get('ativo') == 'on' else False
        nome = request.POST.get('nome')
        sigla = request.POST.get('sigla')
        descricao = request.POST.get('descricao')
        carga_horaria = request.POST.get('carga-horaria')

        try:
            response = requests.put(CONTAINER_API, json={
                "ativo": ativo,
                "sigla": sigla,
                "nome": nome,
                "descricao": descricao,
                "carga_horaria_total": carga_horaria
            }, headers=headers)

            if response.status_code in (200, 201):
                data = response.json()
                return redirect('catalogo:cursos')
            else:
                data = {"error": response.json().get('detail', 'Erro desconhecido')}
                return render(request, 'catalogo/pages/cursos/editar_curso/index.html', context=data)
            
        except Exception:
            data = {'error': "Erro ao acessar API"}
            return render(request, 'catalogo/pages/cursos/editar_curso/index.html', context=data)
    else:
        return render(request, 'catalogo/pages/cursos/editar_curso/index.html', context=data)
            
def curso_detalhe(request, id):
    CONTAINER_API = API_URL + f'cursos/{id}/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    try:
        response = requests.get(CONTAINER_API, headers=headers)
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/cursos/curso/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception:
        data = {"error": "Erro desconhecido."}
        render(request, 'catalogo/pages/cursos/curso/index.html')
    
    return render(request, 'catalogo/pages/cursos/curso/index.html', context=data)

def inativar_curso(request, id):
    CONTAINER_API = API_URL + f'cursos/{id}/inativar/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    response = requests.patch(CONTAINER_API, json={"ativo": False}, headers=headers)

    if response.status_code in (200, 204):
        return redirect('catalogo:cursos')
    else:
        return render(request, 'catalogo/pages/cursos/index.html', {
            'error': 'Erro ao inativar curso'
        })

def ativar_curso(request, id):
    CONTAINER_API = API_URL + f'cursos/{id}/ativar/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    response = requests.patch(CONTAINER_API, json={"ativo": False}, headers=headers)

    if response.status_code in (200, 204):
        return redirect('catalogo:cursos')
    else:
        return render(request, 'catalogo/pages/cursos/index.html', {
            'error': 'Erro ao ativar curso'
        })
    


def disciplinas(request):
    CONTAINER_API = API_URL + 'disciplinas/'
    token = request.session.get('api_access')
    headers = get_headers(token)
    try:
        response = requests.get(CONTAINER_API, headers=headers)
        
        if response.status_code in (401, 403):
            return redirect('catalogo:login')
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/disciplinas/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception as e:
        return render(request, 'catalogo/pages/disciplinas/index.html')
    return render(request, 'catalogo/pages/disciplinas/index.html', context=data)
     
def criar_disciplina(request):
    CONTAINER_API = API_URL + 'disciplinas/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    CONTAINER_API_CURSO = API_URL + 'cursos/?ativo=true'
    token = request.session.get('api_access')
    headers = get_headers(token)
    params = {"ativo": "true"}

    response = requests.get(CONTAINER_API_CURSO, headers=headers, params=params)

    try:
       if response.status_code == 200:
        data =  response.json()
       else:
           return redirect('catalogo:login')
    except Exception:
        data = {"error": "Não foi possível decodificar o JSON da API"}
        
    if request.method == "POST":
        ativo = True if request.POST.get('ativo') == 'on' else False
        nome = request.POST.get('nome')
        sigla = request.POST.get('sigla')
        carga_horaria = request.POST.get('carga-horaria')
        curso_id = request.POST.get('curso')

        try:
            response = requests.post(CONTAINER_API, json={
                "ativo": ativo,
                "sigla": sigla,
                "nome": nome,
                "carga_horaria": carga_horaria,
                "curso_id": curso_id,
            }, headers=headers)

            if response.status_code in (200, 201):
                data = response.json()
                return redirect('catalogo:dashboard')
            else:
                data = {"error": response.json().get('detail', 'Erro desconhecido')}
                return render(request, 'catalogo/pages/disciplinas/nova_disciplina/index.html', context=data)
            
        except Exception:
            data = {'error': "Erro ao acessar API"}
            return render(request, 'catalogo/pages/disciplinas/nova_disciplina/index.html', context=data)
        
    return render(request, 'catalogo/pages/disciplinas/nova_disciplina/index.html',context=data)

def editar_disciplina(request, id):
    CONTAINER_API = API_URL + f'disciplinas/{id}/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    try:
        response = requests.get(CONTAINER_API, headers=headers)
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/disciplinas/editar_disciplina/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception:
        data = {"error": "Erro desconhecido."}
        render(request, 'catalogo/pages/disciplinas/editar_disciplina/index.html')
        
    if request.method == "POST":
        ativo = True if request.POST.get('ativo') == 'on' else False
        nome = request.POST.get('nome')
        sigla = request.POST.get('sigla')
        carga_horaria = request.POST.get('carga-horaria')

        try:
            response = requests.patch(CONTAINER_API, json={
                "ativo": ativo,
                "sigla": sigla,
                "nome": nome,
                "carga_horaria_total": carga_horaria,
            }, headers=headers)

            if response.status_code in (200, 201):
                data = response.json()
                return redirect('catalogo:disciplinas')
            else:
                data = {"error": response.json().get('detail', 'Erro desconhecido')}
                return render(request, 'catalogo/pages/disciplinas/editar_disciplina/index.html', context=data)
            
        except Exception:
            data = {'error': "Erro ao acessar API"}
            return render(request, 'catalogo/pages/disciplinas/editar_disciplina/index.html', context=data)
    else:
        return render(request, 'catalogo/pages/disciplinas/editar_disciplina/index.html', context=data)
            
def disciplina_detalhe(request, id):
    CONTAINER_API = API_URL + f'disciplinas/{id}/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    try:
        response = requests.get(CONTAINER_API, headers=headers)
        if response.status_code in (200, 201):
            data = response.json()
        else:
            error = response.json()
            return render(request, 'catalogo/pages/disciplinas/disciplina/index.html', {
                'error': f"{error.get('detail', 'Erro desconhecido')}"
            })
    except Exception:
        data = {"error": "Erro desconhecido."}
        render(request, 'catalogo/pages/disciplinas/disciplina/index.html')
    
    return render(request, 'catalogo/pages/disciplinas/disciplina/index.html', context=data)

def inativar_disciplina(request, id):
    CONTAINER_API = API_URL + f'disciplinas/{id}/inativar/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    response = requests.patch(CONTAINER_API, json={"ativo": False}, headers=headers)

    if response.status_code in (200, 204):
        return redirect('catalogo:disciplinas')
    else:
        return render(request, 'catalogo/pages/disciplinas/index.html', {
            'error': 'Erro ao inativar disciplina'
        })

def ativar_disciplina(request, id):
    CONTAINER_API = API_URL + f'disciplinas/{id}/ativar/'
    token = request.session.get('api_access')
    headers = get_headers(token)

    response = requests.patch(CONTAINER_API, json={"ativo": False}, headers=headers)

    if response.status_code in (200, 204):
        return redirect('catalogo:disciplinas')
    else:
        return render(request, 'catalogo/pages/disciplinas/index.html', {
            'error': 'Erro ao ativar curso'
        })