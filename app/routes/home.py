from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Cliente, Veiculo, Processo, Endereco

from datetime import datetime

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

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
    
    return render_template('clientes/form.html')

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
        
    return render_template('veiculos/form.html')

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
    return render_template('processos/form.html', clientes=clientes, veiculos=veiculos)