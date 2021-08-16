# shortUrlBackEnd


O shortUrlBackEnd é um projeto que tem como o objetivo fazer o encurtamento de url's, utilizando as tecnologias: mongodb, python e flask.

O banco de dados está no mongoDB Atlas, por isso para seu funcionamento é de suma importância que o .env esteja configurado corretamente.

Também possui no projeto uma endpoints para criação de usuario e autenticação, temos apenas 1 login já cadastrado podendo assim criar mais utilizando o endpoint de criação,
o login já criado é o seguinte:
{
	"username": "admin",
	"password": "admin"
}


## Endpoints


|METODO|URL|PARAMETROS|SOBRE|
| --------- |----------- | ------ | --------|
| GET|/<string:encurtada> | Não há | Utilizado para fazer o redirecionamento para a url desejada |
| POST |/url | {"url": "url_qualquer", "shortUrl": "shortUrl qualquer", "expirateDate": 7 } | Utilizada para fazer a criação de novas urls encurtadas. Os parametros shortUrl e expirateDate são opcionais |
| GET|/url/<int:pages> | Não há | Retorna todas as url's com paginação|
| POST|/login | {"username":"admin", "password":"admin"} | Cria um novo login|
| POST |/login/autenticate | {"username":"admin", "password":"admin"} | Autentica um usuário |


## Como executar

Para executar o projeto é necessário ter em sua maquina o python e pip.

Para instalar as dependencias, execute o seguinte comando no cmd: 

```bash
pip install -r requirements.txt
```

Para executar o projeto, execute o seguinte comando no cmd:

```bash
Flask run
```

## Rotina

O projeto possui um arquivo chamado "expirationDate.py" esse arquivo é responsável por alterar o status das url's para 0(inativas) nas url's que possua as datas já expiradas, para que ele funciona corretamente deverá configurar esse script em um cron ou algum progama de agendamento de tarefas de sua preferência para que ele execute todos os dias, mantendo assim todas as url's expiradas como inativas. 
