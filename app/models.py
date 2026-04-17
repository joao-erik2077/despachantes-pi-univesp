from app import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    vencimento_cnh = db.Column(db.Date, nullable=False)
    nome_pai = db.Column(db.String(50), nullable=False)
    nome_mae = db.Column(db.String(50), nullable=False)
    cpf__cnpj = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(50), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'))

    veiculos = db.relationship('Veiculo', backref='cliente', lazy=True)
    processos = db.relationship('Processo', backref='cliente', lazy=True)

class Veiculo(db.Model):
    __tablename__ = 'veiculo'
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(50), nullable=False)
    renavam = db.Column(db.String(50), nullable=False)
    chassis = db.Column(db.String(50), nullable=False)
    grupo = db.Column(db.String(50), nullable=False)
    placa_anterior = db.Column(db.String(50), nullable=False)
    proprietario_anterior = db.Column(db.String(50), nullable=False)
    cpf__cnpj_anterior = db.Column(db.String(50), nullable=False)
    marca__modelo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    combustivel = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    ano_fabricacao = db.Column(db.String(50), nullable=False)
    ano_modelo = db.Column(db.String(50), nullable=False)
    cilindradas = db.Column(db.String(50), nullable=False)
    potencia = db.Column(db.String(50), nullable=False)
    passageiros = db.Column(db.String(50), nullable=False)
    proprietario_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    processos = db.relationship('Processo', backref='cliente', lazy=True)

class Processo(db.Model):
    __tablename__ = 'processo'
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))

class DocumentoDigitalizado(db.Model):
    __tablename__ = 'documento_digitalizado'
    id = db.Column(db.Integer, primary_key=True)

class Endereco(db.Model):
    __tablename__ = 'endereco'
    id = db.Column(db.Integer, primary_key=True)
    pais = db.Column(db.String(50), nullable=False)
    unidade_federacao = db.Column(db.String(50), nullable=False)
    municipio = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    logradouro = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(50), nullable=False)

    clientes = db.relationship('Cliente', backref='endereco', lazy=True)