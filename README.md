# test_task_2
Ещё одно маленькое тестовое задание

###
1. В коллекции пользователей 'Account' лежат документы вида:

{
  'number': '7800000000000',
  'name': 'Пользователь №',
  'sessions': [
    {
      'created_at': ISODate(
      '2016-01-01T00:00:00'
      ),
      'session_id': '6QBnQhFGgDgC2FDfGwbgEaLbPMMBofPFVrVh9Pn2quooAcgxZc',
      'actions': [
        {
          'type': 'read',
          'created_at': ISODate(
          '2016-01-01T01:20:01'
          )
        },
        {
          'type': 'read',
          'created_at': ISODate(
          '2016-01-01T01:21:13'
          )
        },
        {
          'type': 'create',
          'created_at': ISODate(
          '2016-01-01T01:33:59'
          )
        }
      ]
    }
  ]
}

Необходимо написать агрегационный запрос, который по каждому пользователю выведет последнее действие

и общее количество для каждого из типов 'actions'. Итоговые данные должны представлять собой

список документов вида:

{
  'number': '7800000000000',
  'actions': [
    {
      'type': 'create',
      'last': 'created_at'
      :
      ISODate(
      '2016-01-01T01:33:59'
      ),
      'count': 12
    },
    {
      'type': 'read',
      'last': 'created_at'
      :
      ISODate(
      '2016-01-01T01:21:13'
      ),
      'count': 12
    },
    {
      'type': 'update',
      'last': null,
      'count': 0
    },
    {
      'type': 'delete',
      'last': null,
      'count': 0
    }
  ]
}
