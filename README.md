# Descrição do projeto
Neste projeto, temos três versões de uma automação web RPA, desenvolvida em Python com o Framework Open Source da BotCity e gerenciada pelo BotCity Orquestrador, que realiza consulta de CEP no site dos Correios do Brasil. Cada uma das versões encontra-se em uma branch diferentes, são elas:
- [1ª versão](https://github.com/morgannadev/rpa-consulta-cep-em-lote/tree/projeto-inicial): Branch "projeto-inicial". Nessa versão, a automação consulta apenas um CEP que está fixo no código;
- [2ª versão](https://github.com/morgannadev/rpa-consulta-cep-em-lote/tree/projeto-com-parametro): Branch "projeto-com-parametro". Nessa versão, a automação consulta CEPs enviados via parâmetro no Orquestrador;
- [3ª versão](https://github.com/morgannadev/rpa-consulta-cep-em-lote/tree/projeto-para-executar-em-lote): Branch "projeto-para-executar-em-lote". Nessa versão, a automação consulta CEPs em lote, enviados por um CSV pelo Orquestrador.

Você pode seguir o passo a passo do desenvolvimento [nesta live](https://www.youtube.com/watch?v=45ZqN-DkWos) que ficou gravada e disponível no YouTube.

# Preparar o ambiente
Para executar este projeto, você deverá fazer a etapa de [pré-requisitos desta documentação](https://documentation.botcity.dev/pt/getting-started/prerequisites/), que basicamente são os itens abaixo.

## Pré-requisitos:
- [Conta BotCity](https://developers.botcity.dev/app/signup);
- [BotCity Studio SDK](https://documentation.botcity.dev/pt/getting-started/botcity-studio-sdk/);
- [Python 3.7 ou superior](https://www.python.org/downloads/);
- Ter uma IDE instalada, por exemplo: [Visual Studio Code](https://code.visualstudio.com/download) ou [PyCharm](https://www.jetbrains.com/pycharm/download/).

Ao instalar o BotCity Studio SDK, caso aconteça algum problema, você pode usar a ferramenta de diagnóstico para validar o que pode ter acontecido. Para acessar essa ferramenta, verifique [este link](https://documentation.botcity.dev/pt/getting-started/botcity-studio-sdk/#ferramenta-de-diagnostico) da documentação.

# Antes de executar
Atenção aos passos que deve seguir após fazer o fork e clone do projeto em seu computador.

## 01. Crie ambiente virtual (opcional)
Você pode utilizar ambiente virtual com o Python, se preferir. E para criá-lo, execute o seguinte comando:
```
python -m venv venv
```

Após a criação, é necessário ativá-lo. Para isso, execute o comando abaixo:
```
venv\Scripts\activate
```

## 02. Instale as dependências do `requirements.txt`
Para fazer a instalação das dependências do projeto, você deve executar no terminal da sua IDE o comando abaixo, a partir da pasta do projeto:
```
pip install --upgrade -r requirements.txt
```

## 03. Valide permissionamento
Para executar no seu computador ou máquina virtual, garanta que você tem permissão para rodar scripts, códigos etc.

# Para executar local
Se você quiser testar primeiramente no seu computador ou máquina virtual, você deverá:

## 01. Comente os códigos que usam o `execution`
Quando estamos executando o robô localmente, não temos uma tarefa criada. Sendo assim, precisamos comentar os códigos que tenham relação com isso para evitar erros. Identifique no código as chamadas pela instância do `maestro`, exemplos:
```
...
# execution = maestro.get_execution()
...
maestro.alert(
    task_id=execution.task_id,
    title="Iniciando a tarefa",
    message=f"Iniciando a tarefa de consulta do CEP {cep} nos Correios",
    alert_type=AlertType.INFO
)
```

## 02. Execute o robô
Você pode executar clicando no botão de play ou de execução da sua IDE favorita, ou ainda executar o comando abaixo no seu terminal:
```
python bot.py
```

# Para executar no BotCity Orquestrador
Quando estamos executando o robô no Orquestrador, a tarefa será criada, então não precisamos deixar os códigos do item anterior comentados. Tire os comentários para que os códigos possam ser executados corretamente.

Lembre-se de seguir as orientações da [documentação](https://documentation.botcity.dev/pt/tutorials/orchestrating-your-automation/) para fazer o deploy da sua automação no Orquestrador e executar com apoio do Runner.

Também deixo como sugestão você realizar o curso (gratuito e em Português, com certificado) sobre [Orquestração de Python RPA](https://developers.botcity.dev/academy/orchestration), com orientações sobre como utilizar, como configurar as funcionalidades e acompanhar o gerenciamento da sua automação no dia-a-dia.

# Para criar o Execution Log no BotCity Orquestrador
Siga as orientações da documentação: funcionalidade [Logs de Execução](https://documentation.botcity.dev/pt/maestro/features/logs/) e como utilizar o [SDK](https://documentation.botcity.dev/pt/maestro/maestro-sdk/log/).

# Para criar o Datapool no BotCity Orquestrador
Siga as oriantações da documentação: funcionalidade [Datapool](https://documentation.botcity.dev/pt/maestro/features/datapool/) e como utilizar o [SDK](https://documentation.botcity.dev/pt/maestro/maestro-sdk/datapool/).

# Próximos passos
Há diversas possibilidades de melhorias neste projeto e deixo à disponibilidade da comunidade para explorarmos essas melhorias e implementarmos. Algumas sugestões:
- Refatorar o código para melhor separação de responsabilidades;
- Especificar os erros de maneira mais clara para gerenciamento via Orquestrador;
- Entre outros.

Fiquem à vontade de mandar sugestões e correções pelas issues do projeto.
