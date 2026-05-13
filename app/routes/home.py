from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import db, Cliente, Veiculo, Processo, Endereco

from datetime import datetime

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/api/clientes/buscar')
def api_clientes_buscar():
    nome = request.args.get('nome', '')
    if not nome or len(nome) < 3:
        return jsonify([])
        
    clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{nome}%')).limit(10).all()
    resultado = []
    for c in clientes:
        resultado.append({
            'id': c.id,
            'nome': c.nome,
            'cpf_cnpj': c.cpf__cnpj,
            'rg': c.rg,
            'data_nascimento': c.data_nascimento.strftime('%Y-%m-%d') if c.data_nascimento else '',
            'vencimento_cnh': c.vencimento_cnh.strftime('%Y-%m-%d') if c.vencimento_cnh else '',
            'email': c.email,
            'telefone': c.telefone,
            'nome_pai': c.nome_pai,
            'nome_mae': c.nome_mae,
            'cep': c.endereco.cep if c.endereco else '',
            'logradouro': c.endereco.logradouro if c.endereco else '',
            'numero': c.endereco.numero if c.endereco else '',
            'bairro': c.endereco.bairro if c.endereco else '',
            'municipio': c.endereco.municipio if c.endereco else '',
            'unidade_federacao': c.endereco.unidade_federacao if c.endereco else ''
        })
    return jsonify(resultado)

@bp.route('/')
def index():
    total_veiculos = Veiculo.query.count()
    total_processos = Processo.query.count()
    total_pendencias = Processo.query.filter_by(status='Pendente').count()
    return render_template('index.html', 
                           total_veiculos=total_veiculos, 
                           total_processos=total_processos, 
                           total_pendencias=total_pendencias)

@bp.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes/index.html', clientes=clientes)

@bp.route('/clientes/novo', methods=['GET', 'POST'])
def cliente_novo():
    if request.method == 'POST':
        # Salva o Endereço primeiro
        endereco = Endereco(
            cep=request.form.get('cep'),
            logradouro=request.form.get('logradouro'),
            numero=request.form.get('numero'),
            bairro=request.form.get('bairro'),
            municipio=request.form.get('municipio'),
            unidade_federacao=request.form.get('unidade_federacao'),
            pais=request.form.get('pais', 'Brasil')
        )
        db.session.add(endereco)
        db.session.flush()

        # Converte strings de data
        dt_nasc = datetime.strptime(request.form.get('data_nascimento'), '%Y-%m-%d').date()
        dt_venc = datetime.strptime(request.form.get('vencimento_cnh'), '%Y-%m-%d').date()

        # Salva o Cliente
        cliente = Cliente(
            nome=request.form.get('nome'),
            cpf__cnpj=request.form.get('cpf__cnpj'),
            rg=request.form.get('rg'),
            data_nascimento=dt_nasc,
            vencimento_cnh=dt_venc,
            email=request.form.get('email'),
            telefone=request.form.get('telefone'),
            nome_pai=request.form.get('nome_pai'),
            nome_mae=request.form.get('nome_mae'),
            endereco_id=endereco.id
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('home.clientes'))
    
    return render_template('clientes/form.html', cliente=None)

@bp.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        # Atualiza o Endereço
        if cliente.endereco:
            cliente.endereco.cep = request.form.get('cep')
            cliente.endereco.logradouro = request.form.get('logradouro')
            cliente.endereco.numero = request.form.get('numero')
            cliente.endereco.bairro = request.form.get('bairro')
            cliente.endereco.municipio = request.form.get('municipio')
            cliente.endereco.unidade_federacao = request.form.get('unidade_federacao')
            cliente.endereco.pais = request.form.get('pais', 'Brasil')

        # Converte strings de data
        cliente.data_nascimento = datetime.strptime(request.form.get('data_nascimento'), '%Y-%m-%d').date()
        cliente.vencimento_cnh = datetime.strptime(request.form.get('vencimento_cnh'), '%Y-%m-%d').date()

        # Atualiza o Cliente
        cliente.nome = request.form.get('nome')
        cliente.cpf__cnpj = request.form.get('cpf__cnpj')
        cliente.rg = request.form.get('rg')
        cliente.email = request.form.get('email')
        cliente.telefone = request.form.get('telefone')
        cliente.nome_pai = request.form.get('nome_pai')
        cliente.nome_mae = request.form.get('nome_mae')

        db.session.commit()
        return redirect(url_for('home.clientes'))
        
    return render_template('clientes/form.html', cliente=cliente)

def _salvar_ou_atualizar_cliente(form):
    cliente_nome = form.get('cliente_nome')
    if not cliente_nome:
        return None

    def parse_date(d_str):
        if not d_str: return datetime.now().date()
        try: return datetime.strptime(d_str, '%Y-%m-%d').date()
        except: return datetime.now().date()

    cliente = Cliente.query.filter_by(nome=cliente_nome).first()
    
    if not cliente:
        endereco = Endereco(
            cep=form.get('endereco_cep', ''),
            logradouro=form.get('endereco_logradouro', ''),
            numero=form.get('endereco_numero', ''),
            bairro=form.get('endereco_bairro', ''),
            municipio=form.get('endereco_municipio', ''),
            unidade_federacao=form.get('endereco_uf', ''),
            pais='Brasil'
        )
        db.session.add(endereco)
        db.session.flush()

        cliente = Cliente(
            nome=cliente_nome,
            cpf__cnpj=form.get('cliente_cpf_cnpj', ''),
            rg=form.get('cliente_rg', ''),
            data_nascimento=parse_date(form.get('cliente_nascimento')),
            vencimento_cnh=parse_date(form.get('cliente_vencimento_cnh')),
            email=form.get('cliente_email', ''),
            telefone=form.get('cliente_telefone', ''),
            nome_pai=form.get('cliente_pai', ''),
            nome_mae=form.get('cliente_mae', ''),
            endereco_id=endereco.id
        )
        db.session.add(cliente)
        db.session.flush()
    else:
        cliente.cpf__cnpj = form.get('cliente_cpf_cnpj', cliente.cpf__cnpj)
        cliente.rg = form.get('cliente_rg', cliente.rg)
        cliente.data_nascimento = parse_date(form.get('cliente_nascimento'))
        cliente.vencimento_cnh = parse_date(form.get('cliente_vencimento_cnh'))
        cliente.email = form.get('cliente_email', cliente.email)
        cliente.telefone = form.get('cliente_telefone', cliente.telefone)
        cliente.nome_pai = form.get('cliente_pai', cliente.nome_pai)
        cliente.nome_mae = form.get('cliente_mae', cliente.nome_mae)
        
        if not cliente.endereco:
            cliente.endereco = Endereco(pais='Brasil')
            db.session.add(cliente.endereco)
            db.session.flush()

        cliente.endereco.cep = form.get('endereco_cep', cliente.endereco.cep)
        cliente.endereco.logradouro = form.get('endereco_logradouro', cliente.endereco.logradouro)
        cliente.endereco.numero = form.get('endereco_numero', cliente.endereco.numero)
        cliente.endereco.bairro = form.get('endereco_bairro', cliente.endereco.bairro)
        cliente.endereco.municipio = form.get('endereco_municipio', cliente.endereco.municipio)
        cliente.endereco.unidade_federacao = form.get('endereco_uf', cliente.endereco.unidade_federacao)
        
    return cliente.id

@bp.route('/veiculos')
def veiculos():
    veiculos = Veiculo.query.all()
    return render_template('veiculos/index.html', veiculos=veiculos)

@bp.route('/veiculos/novo', methods=['GET', 'POST'])
def veiculo_novo():
    if request.method == 'POST':
        # Pode criar ou usar o cliente selecionado
        veiculo = Veiculo(
            placa=request.form.get('veiculo_placa', ''),
            renavam=request.form.get('veiculo_renavam', ''),
            chassis=request.form.get('veiculo_chassi', ''),
            marca__modelo=request.form.get('veiculo_marca_modelo', ''),
            tipo=request.form.get('veiculo_tipo', ''),
            especie=request.form.get('veiculo_especie', ''),
            cor=request.form.get('veiculo_cor', ''),
            combustivel=request.form.get('veiculo_combustivel', ''),
            categoria=request.form.get('veiculo_categoria', ''),
            grupo=request.form.get('veiculo_grupo', ''),
            ano_fabricacao=request.form.get('veiculo_ano_fab', ''),
            ano_modelo=request.form.get('veiculo_ano_mod', ''),
            cilindradas=request.form.get('veiculo_cilindradas', ''),
            potencia=request.form.get('veiculo_potencia', ''),
            passageiros=request.form.get('veiculo_passageiros', ''),
            placa_anterior=request.form.get('veiculo_placa_anterior', ''),
            proprietario_anterior=request.form.get('veiculo_proprietario_anterior', ''),
            cpf__cnpj_anterior=request.form.get('veiculo_cpf_cnpj_anterior', ''),
            proprietario_id=_salvar_ou_atualizar_cliente(request.form)
        )
        db.session.add(veiculo)
        db.session.commit()
        return redirect(url_for('home.veiculos'))
        
    return render_template('veiculos/form.html', veiculo=None)

@bp.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def veiculo_editar(id):
    veiculo = Veiculo.query.get_or_404(id)
    if request.method == 'POST':
        veiculo.placa = request.form.get('veiculo_placa', '')
        veiculo.renavam = request.form.get('veiculo_renavam', '')
        veiculo.chassis = request.form.get('veiculo_chassi', '')
        veiculo.marca__modelo = request.form.get('veiculo_marca_modelo', '')
        veiculo.tipo = request.form.get('veiculo_tipo', '')
        veiculo.especie = request.form.get('veiculo_especie', '')
        veiculo.cor = request.form.get('veiculo_cor', '')
        veiculo.combustivel = request.form.get('veiculo_combustivel', '')
        veiculo.categoria = request.form.get('veiculo_categoria', '')
        veiculo.grupo = request.form.get('veiculo_grupo', '')
        veiculo.ano_fabricacao = request.form.get('veiculo_ano_fab', '')
        veiculo.ano_modelo = request.form.get('veiculo_ano_mod', '')
        veiculo.cilindradas = request.form.get('veiculo_cilindradas', '')
        veiculo.potencia = request.form.get('veiculo_potencia', '')
        veiculo.passageiros = request.form.get('veiculo_passageiros', '')
        veiculo.placa_anterior = request.form.get('veiculo_placa_anterior', '')
        veiculo.proprietario_anterior = request.form.get('veiculo_proprietario_anterior', '')
        veiculo.cpf__cnpj_anterior = request.form.get('veiculo_cpf_cnpj_anterior', '')
        veiculo.proprietario_id = _salvar_ou_atualizar_cliente(request.form)
        
        db.session.commit()
        return redirect(url_for('home.veiculos'))
        
    return render_template('veiculos/form.html', veiculo=veiculo)

@bp.route('/processos')
def processos():
    processos = Processo.query.all()
    return render_template('processos/index.html', processos=processos)

@bp.route('/processos/novo', methods=['GET', 'POST'])
def processo_novo():
    if request.method == 'POST':
        def parse_date(d_str):
            if not d_str: return None
            try: return datetime.strptime(d_str, '%Y-%m-%d').date()
            except: return None
            
        processo = Processo(
            cliente_id=request.form.get('cliente_id') or None,
            veiculo_id=request.form.get('veiculo_id') or None,
            descricao=request.form.get('descricao', ''),
            data_inicio=parse_date(request.form.get('data_inicio')),
            data_solucionado=parse_date(request.form.get('data_solucionado'))
        )
        db.session.add(processo)
        db.session.commit()
        return redirect(url_for('home.processos'))
        
    clientes = Cliente.query.all()
    veiculos = Veiculo.query.all()
    return render_template('processos/form.html', clientes=clientes, veiculos=veiculos, processo=None)

@bp.route('/processos/editar/<int:id>', methods=['GET', 'POST'])
def processo_editar(id):
    processo = Processo.query.get_or_404(id)
    if request.method == 'POST':
        def parse_date(d_str):
            if not d_str: return None
            try: return datetime.strptime(d_str, '%Y-%m-%d').date()
            except: return None

        processo.cliente_id = request.form.get('cliente_id') or None
        processo.veiculo_id = request.form.get('veiculo_id') or None
        processo.descricao = request.form.get('descricao', '')
        processo.data_inicio = parse_date(request.form.get('data_inicio'))
        processo.data_solucionado = parse_date(request.form.get('data_solucionado'))
        db.session.commit()
        return redirect(url_for('home.processos'))
        
    clientes = Cliente.query.all()
    veiculos = Veiculo.query.all()
    return render_template('processos/form.html', clientes=clientes, veiculos=veiculos, processo=processo)

@bp.route('/processos/status/<int:id>', methods=['POST'])
def processo_alterar_status(id):
    processo = Processo.query.get_or_404(id)
    novo_status = request.form.get('status')
    if novo_status in ['Em Andamento', 'Pendente', 'Finalizado']:
        processo.status = novo_status
        db.session.commit()
    return redirect(url_for('home.processos'))

@bp.route('/clientes/excluir/<int:id>', methods=['POST'])
def cliente_excluir(id):
    cliente = Cliente.query.get_or_404(id)
    if cliente.endereco:
        db.session.delete(cliente.endereco)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('home.clientes'))

@bp.route('/veiculos/excluir/<int:id>', methods=['POST'])
def veiculo_excluir(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('home.veiculos'))

@bp.route('/processos/excluir/<int:id>', methods=['POST'])
def processo_excluir(id):
    processo = Processo.query.get_or_404(id)
    db.session.delete(processo)
    db.session.commit()
    return redirect(url_for('home.processos'))