# Painel de Chamados - Agidesk

Este projeto visa criar um painel web local para o setor de suporte da empresa, integrado com a API do Agidesk. O painel fornecerá informações detalhadas sobre os chamados, como quantidade de chamados, status, responsáveis, e métricas de tempo.

## Funcionalidades

### Principais
- **Quantidade de Chamados**: Exibir o número total de chamados abertos.
- **Chamados com Responsável**: Mostrar quantos chamados já têm um responsável atribuído.
- **Chamados sem Responsável**: Mostrar quantos chamados ainda não têm um responsável atribuído.
- **Chamados Abertos no Dia**: Exibir o número de chamados abertos no dia atual.
- **Filtrar Chamados por Responsável**: Permitir a filtragem de chamados por responsável.
- **Chamados Mais Antigos**: Listar os chamados que estão abertos há mais tempo.

### Secundárias
- **Status dos Chamados**: Exibir o status atual de cada chamado (aberto, em andamento, resolvido, etc.).
- **Detalhes do Chamado**: Mostrar detalhes específicos de cada chamado, como descrição, data de abertura, responsável, etc.
- **Atualização Automática**: Atualizar automaticamente o painel em intervalos regulares para refletir as mudanças mais recentes.

## Tech Stack

### Backend
- **Python**: Linguagem principal para o desenvolvimento do backend.
- **Flask**: Framework web para criar a aplicação e gerenciar rotas.
- **Requests**: Biblioteca para fazer requisições HTTP à API do Agidesk.

### Frontend
- **HTML/CSS**: Para a estrutura e estilização da interface do usuário.
- **JavaScript**: Para interatividade e atualizações dinâmicas.
- **Bootstrap** (Opcional): Para facilitar o design responsivo e componentes UI.

### Ferramentas de Desenvolvimento
- **Git**: Controle de versão.
- **Postman**: Para testar requisições à API do Agidesk.

## Estrutura do Projeto
painel-agidesk/
│
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── models.py (Opcional)
│ └── services/
│   └── agidesk_service.py
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── chamados.html
│ └── filtros.html
│
├── static/
│ ├── css/
│ ├── js/
│ └── images/
│
├── config.py
├── requirements.txt
└── run.py

## Requisitos da API do Agidesk

- **Autenticação**: Verificar se a API do Agidesk requer autenticação (e.g., API Key, OAuth).
- **Endpoints**: Identificar os endpoints necessários para obter as informações dos chamados.
  - Listar chamados.
  - Detalhes de um chamado específico.
  - Filtrar chamados por responsável.
  - Obter métricas de tempo.

## Passos para Implementação

1. **Configuração do Ambiente**:
   - Instalar Python e Flask.
   - Criar um ambiente virtual.
   - Instalar dependências (`requests`, `flask`, etc.).

2. **Integração com a API do Agidesk**:
   - Criar um serviço (`agidesk_service.py`) para fazer requisições à API.
   - Implementar funções para buscar chamados, filtrar por responsável, etc.

3. **Desenvolvimento do Backend**:
   - Criar rotas no Flask para exibir as informações no painel.
   - Implementar lógica para processar os dados da API e passar para o frontend.

4. **Desenvolvimento do Frontend**:
   - Criar templates HTML para exibir as informações.
   - Adicionar interatividade com JavaScript (e.g., filtros, atualizações dinâmicas).

5. **Testes**:
   - Testar a integração com a API.
   - Verificar a exibição correta dos dados no painel.
   - Testar funcionalidades como filtros e atualizações automáticas.

6. **Implantação**:
   - Configurar o aplicativo para rodar localmente.

## Considerações Finais

- **Segurança**: Garantir que as credenciais da API (se houver) sejam armazenadas de forma segura.
- **Performance**: Otimizar as requisições à API para evitar lentidão no painel.
- **Documentação**: Manter a documentação do código e do projeto atualizada.