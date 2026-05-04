from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Cliente, Veiculo, Processo, Endereco

from datetime import datetime

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    total_veiculos = Veiculo.query.count()
    total_processos = Processo.query.count()
    total_pendencias = 0 # Atualizar quando o modelo de pendências/status for criado
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
            cpf__cnpj_anterior=request.form.get('veiculo_cpf_cnpj_anterior', '')
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
        processo = Processo(
            cliente_id=request.form.get('cliente_id') or None,
            veiculo_id=request.form.get('veiculo_id') or None
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
        processo.cliente_id = request.form.get('cliente_id') or None
        processo.veiculo_id = request.form.get('veiculo_id') or None
        db.session.commit()
        return redirect(url_for('home.processos'))
        
    clientes = Cliente.query.all()
    veiculos = Veiculo.query.all()
    return render_template('processos/form.html', clientes=clientes, veiculos=veiculos, processo=processo)