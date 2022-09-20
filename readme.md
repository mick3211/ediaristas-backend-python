# Projeto e-diaristas TreinaWeb

Sistema administrativo utilizando django e mySQL

#### Clonar o repositório

`https://github.com/mick3211/Sistema-administrativo-Multistack-TreinaWeb.git`

#### Instalar dependências

`pip install -r requirements.txt`

#### Alterar configurações do BD no arquivo `settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_bd',
        'HOST': 'host_do_bd',
        'PORT': porta_bd,
        'USER': 'usuario_bd',
        'PASSWORD': 'senha_bd'
    }
}
```

#### Migrar banco de dados

`python manage.py migrate`

#### Iniciar servidor

`python manage.py runserver`
