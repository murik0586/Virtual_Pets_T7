# **Кейс 8. Виртуальный питомец**
_____________________________________________
Сложность: повышенная
Вам предстоит разработать сервис виртуального питомца.
Это должен быть HTTP-сервер с RESTful API, который принимает
запросы и умеет выполнять следующие операции:
• создаёт питомца с указанием показателя жизни (число) и
клички;
• даёт возможность совершать действия с питомцем: покормить,
погладить, дать вкусняшку и погулять;
• показывает текущую статистику по питомцу.
Питомец имеет:
• имя — изначально берётся из запроса при создании ✔;
• показатель жизни — изначально берётся из запроса при
создании ✔;
• показатель счастья — изначально 2 ✔;
• показатель голода — изначально 2 ✔.
С питомцем можно совершить следующие действия:
• покормить (-2 к голоду);
• погладить (+1 к счастью, +1 к голоду);
• дать вкусняшку (+2 к счастью, -1 к голоду);
• погулять (+1 к счастью, +3 к голоду);
• игнорировать (-1 к счастью, +1 к голоду).
Если после какого-либо действия голод превышает 5, то у питомца
отнимается 1 очко жизни. Если после предыдущего действия уже
уменьшалась жизнь, то отнимается на 1 очко больше, чем отнималось в
прошлый раз.
Если показатель жизни достигает 0, то питомец исчезает. Если после
какого-либо действия счастье питомца достигает 0, то питомец исчезает


__________________________________________________________________
Структура проекта:

Пакеты ->
    entity -> (Сущности: Питомцы)
    test -> Тесты