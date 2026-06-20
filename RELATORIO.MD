# Relatório Técnico – ASP.NET Core MVC, Entity Framework Core e SQLite

## Introdução

Este relatório apresenta uma análise da base tecnológica utilizada no projeto da biblioteca, composta por **ASP.NET Core MVC**, **Entity Framework Core (EF Core)** e **SQLite**. O objetivo é explicar como essas tecnologias funcionam e quais são suas vantagens e limitações para o desenvolvimento da aplicação.

---

# Injeção de Dependência (Dependency Injection)

A **Injeção de Dependência (DI)** é um recurso do ASP.NET Core que permite fornecer automaticamente os objetos que uma classe precisa para funcionar.

Na prática, os Controllers precisam acessar serviços como o banco de dados. Em vez de criar esses objetos manualmente, o ASP.NET Core os entrega automaticamente quando necessário.

## Qual problema ela resolve?

A DI reduz o acoplamento entre as classes, tornando o sistema mais organizado, fácil de manter e mais simples de testar.

## Ciclos de vida dos serviços

### Transient

* Cria uma nova instância sempre que o serviço é solicitado.
* Indicado para serviços simples e sem estado.

### Scoped

* Cria uma instância por requisição HTTP.
* Durante uma mesma requisição, todos os componentes utilizam a mesma instância.
* É o ciclo de vida recomendado para o DbContext do Entity Framework.

### Singleton

* Cria apenas uma instância para toda a aplicação.
* Todos os usuários compartilham o mesmo objeto.

## Por que o banco de dados não deve ser Singleton?

O DbContext não foi projetado para ser compartilhado por vários usuários simultaneamente. Utilizá-lo como Singleton pode causar conflitos de acesso, inconsistências de dados e problemas de concorrência. Por isso, o ciclo de vida Scoped é a opção mais segura.

---

# Entity Framework Core e ORM

O **Entity Framework Core** é uma ferramenta ORM (*Object Relational Mapping*).

Uma ORM faz o mapeamento entre classes C# e tabelas do banco de dados, permitindo que os desenvolvedores trabalhem com objetos em vez de escrever comandos SQL manualmente.

## Vantagens da ORM

* Aumenta a produtividade da equipe.
* Reduz a quantidade de código SQL.
* Facilita a manutenção do sistema.
* Diminui a ocorrência de erros.
* Torna o desenvolvimento mais rápido.

## O que é Code-First?

A abordagem **Code-First** utiliza as classes do sistema como base para criar o banco de dados.

Fluxo:

1. Criação das classes em C#.
2. Geração das Migrations.
3. Criação ou atualização do banco de dados.

Dessa forma, o código se torna a principal referência da estrutura do banco.

## Como funcionam as Migrations?

As Migrations registram todas as alterações realizadas na estrutura do banco de dados ao longo do desenvolvimento.

Sempre que uma classe é criada ou modificada, uma Migration pode ser gerada para refletir essa mudança no banco.

## O que acontece ao executar `dotnet ef database update`?

Quando esse comando é executado, o Entity Framework:

1. Consulta a tabela `__EFMigrationsHistory`.
2. Verifica quais Migrations já foram aplicadas.
3. Compara com as Migrations existentes no projeto.
4. Aplica apenas as alterações que ainda não existem no banco.

Isso garante que a estrutura do banco permaneça sincronizada com o código da aplicação.

---

# SQLite: Vantagens e Limitações

O SQLite é um banco de dados leve que armazena todas as informações em um único arquivo `.db`.

## Vantagens do SQLite

* Não exige instalação de servidor.
* Fácil configuração.
* Baixo consumo de recursos.
* Simples de transportar e fazer backup.
* Ideal para desenvolvimento, testes e protótipos.

Essas características tornam o SQLite uma excelente opção para projetos em fase inicial.

## Principal limitação: concorrência

O maior problema do SQLite aparece quando muitas pessoas tentam gravar dados ao mesmo tempo.

Diferente de bancos como PostgreSQL e SQL Server, o SQLite possui limitações de concorrência e pode bloquear operações de escrita enquanto outra gravação está sendo executada.

Isso pode causar:

* Lentidão.
* Filas de processamento.
* Bloqueios temporários.
* Queda de desempenho em sistemas com muitos usuários.

Para um cenário de aproximadamente 10.000 acessos simultâneos, essa limitação pode se tornar um problema significativo.

## Quando migrar para PostgreSQL ou SQL Server?

A migração deve ser considerada quando:

* O número de usuários aumentar significativamente.
* Houver muitas gravações simultâneas.
* O sistema se tornar crítico para o negócio.
* For necessária maior escalabilidade.
* Houver necessidade de recursos avançados de segurança e desempenho.

Nesses cenários, bancos robustos como PostgreSQL ou SQL Server oferecem melhor suporte à concorrência, maior confiabilidade e melhor desempenho.

---

# Conclusão

A combinação de **ASP.NET Core MVC**, **Entity Framework Core** e **SQLite** é uma excelente escolha para desenvolvimento e validação inicial do sistema. A Injeção de Dependência melhora a organização do código, o Entity Framework Core acelera o desenvolvimento através do modelo Code-First e das Migrations, e o SQLite oferece simplicidade e rapidez para ambientes de testes.

Entretanto, caso o sistema cresça e passe a atender milhares de usuários simultaneamente, será recomendada a migração para um banco de dados mais robusto, como PostgreSQL ou SQL Server, garantindo melhor desempenho, escalabilidade e confiabilidade.
