# People Analytics

## Setup initial

```bash
❯ python3 -m venv .wnea
❯ source .wnea/bin/activate
❯ sudo apt-get install libpq-dev python3-dev python3-venv
❯ pip install -r requirements.txt
```

## Rodando o projeto

Instale o projeto com:

```bash
❯ python manage.py migrate
❯ python manage.py populate
❯ python manage.py runserver
```

## Headcount

### URL

```http
    GET /headcount/line_chart/
```

#### Parâmetros

| Parâmetro   | Tipo     | Descrição                                    |
| :---------- | :------- | :------------------------------------------- |
| `init_date` | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd |
| `end_date`  | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd |

#### Resposta

```http
  GET http://localhost:8000/headcount/line_chart/?init_date=2022-01-01&end_date=2023-01-01
```

```json
{
  "xAxis": {
    "type": "category",
    "data": [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
      "Jan"
    ]
  },
  "yAxis": {
    "type": "value"
  },
  "series": {
    "type": "stacked_line",
    "series": [
      {
        "name": 2022,
        "type": "line",
        "data": [[45, 44, 37, 43, 48, 43, 43, 44, 36, 54, 37, 36]]
      },
      {
        "name": 2023,
        "type": "line",
        "data": [[0]]
      }
    ]
  },
  "title": "Headcount por Ano",
  "grid": 6,
  "color": ["#D4DDE2", "#A3B6C2"]
}
```

### URL

```http
  GET /headcount/category_charts/
```

#### Parâmetros

| Parâmetro   | Tipo     | Descrição                                            |
| :---------- | :------- | :--------------------------------------------------- |
| `init_date` | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd         |
| `end_date`  | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd         |
| `category`  | `string` | **Obrigatório**. Qualquer campos de category da base |

#### Resposta

```http
  GET http://localhost:8000/headcount/category_charts/?init_date=2022-12-01&end_date=2022-12-31&category=TI
```

```json
{
  "xAxis": {
    "type": "value",
    "show": true,
    "max": {}
  },
  "yAxis": {
    "type": "category",
    "data": ["East Calvinfurt", "Alexanderton", "East Jenniferview", "Cookfurt"]
  },
  "series": {
    "type": "horizontal_stacked",
    "series": [
      {
        "name": "Colaboradores",
        "data": [4, 2, 4, 2],
        "type": "bar"
      }
    ]
  },
  "title": "Empresa",
  "grid": 6,
  "color": ["#2896DC"],
  "is%": false
}
```

## Turnover:

### URL

```http
  GET /turnover/line_chart/
```

#### Parâmetros

| Parâmetro   | Tipo     | Descrição                                    |
| :---------- | :------- | :------------------------------------------- |
| `init_date` | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd |
| `end_date`  | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd |

#### Resposta

```http
  GET http://localhost:8000/turnover/line_chart/?init_date=2022-01-01&end_date=2022-12-31
```

```json
{
  "xAxis": {
    "type": "category",
    "data": [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec"
    ]
  },
  "yAxis": {
    "type": "value"
  },
  "series": {
    "type": "stacked_line",
    "series": [
      {
        "name": 2022,
        "type": "line",
        "data": [
          [
            0.76, 0.98, 1.16, 1.05, 1.06, 1.05, 0.91, 0.95, 0.89, 0.74, 0.84,
            0.83
          ]
        ]
      }
    ]
  },
  "title": "Taxa de Turnover por Ano (%)",
  "grid": 6,
  "color": ["#D4DDE2", "#A3B6C2"]
}
```

### URL

```http
  GET /turnover/category_charts/
```

#### Parâmetros

| Parâmetro   | Tipo     | Descrição                                            |
| :---------- | :------- | :--------------------------------------------------- |
| `init_date` | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd         |
| `end_date`  | `string` | **Obrigatório**. Campo do formato yyyy-MM-dd         |
| `category`  | `string` | **Obrigatório**. Qualquer campos de category da base |

#### Resposta

```json
{
  "xAxis": {
    "type": "value",
    "show": true,
    "max": {}
  },
  "yAxis": {
    "type": "category",
    "data": ["Empresa 4", "Empresa 3", "Empresa 1", "Empresa 2"]
  },
  "series": {
    "type": "horizontal_stacked",
    "series": [
      {
        "name": "Colaboradores",
        "data": [97, 92.9, 91.3, 89.8],
        "type": "bar"
      }
    ]
  },
  "title": "Empresa",
  "grid": 6,
  "color": ["#2896DC"],
  "is%": false
}
```
