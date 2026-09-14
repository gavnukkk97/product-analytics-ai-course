---
title: "Иерархия метрик VS Пирамида метрик."
source: https://medium.com/@elenest/%D0%B8%D0%B5%D1%80%D0%B0%D1%80%D1%85%D0%B8%D1%8F-%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA-vs-%D0%BF%D0%B8%D1%80%D0%B0%D0%BC%D0%B8%D0%B4%D0%B0-%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA-8eeda61fdefe
author: Elena Seregina
modules: [M1.5, M5.1]
downloaded: 2026-09-14
---

# Иерархия метрик VS Пирамида метрик.

*Автор: Elena Seregina*  
*Источник: https://medium.com/@elenest/%D0%B8%D0%B5%D1%80%D0%B0%D1%80%D1%85%D0%B8%D1%8F-%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA-vs-%D0%BF%D0%B8%D1%80%D0%B0%D0%BC%D0%B8%D0%B4%D0%B0-%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA-8eeda61fdefe*

## Иерархия метрик VS Пирамида метрик. А также что такое North Star Metrics (метрики Всевластия) — учим матчасть

[![Image 1: Elena Seregina](https://miro.medium.com/v2/resize:fill:32:32/1*2AhEhzDIrl1TVBWzcaU-kg.jpeg)](https://medium.com/@elenest?source=post_page---byline--8eeda61fdefe-----------------------------------------)

5 min read

Apr 20, 2019

Сейчас очень популярно работать с данными и метриками. В том числе строить иерархии метрик. Однако “Пирамида метрик”, “Иерархия метрик”, “North Star Metrics” — не просто слова. Это названия мощных методик. И если Вы их неправильно понимаете, или пытаетесь придумать заново, вероятнее всего Вы тратите время не достаточно эффективно.

Press enter or click to view image in full size

![Image 2](https://miro.medium.com/v2/resize:fit:700/1*fGRzRyfBjkg_WFs5XKuwbw.jpeg)

Конспект моей лекции во ВШЭ одной из студенток (февраль 2019)

## Иерархия Метрик

**Кто придумал?** Бессмысленно спорить. Ребенок примерно в 9–14 месяцев решает, что ходить прямо — круто, и идет. Менеджер digital-продукта примерено через то же время работы с аналитикой понимает, что следует привести метрики в порядок и делает это. Так появляется его **Иерархия Метрик**. Она есть **почти**во всех продуктах, где старший возраст дэшборда более года.

> **Иерархия Метрик есть почти во всех продуктах, где старший возраст дэшборда более года.**

![Image 3](https://miro.medium.com/v2/resize:fit:600/1*Ml9fDKR0QmitxiYbiqvdWg.jpeg)

**Кроме шуток**. В допещерные времена (в случае Аналитики в России речь идет о временах 5–10 лет назад) **Иерархию Метрик**делали только в технически развитых конторах (например, Яндекс) и только для флагманских продуктов (например, для Поиска). Зачем?

Дело в том, что если у Интернет-магазина игрушек например какая-нибудь **кнопочка** после релиза **изменит свою конверсию с 0,12% на 0,11%** вряд ли кто-то что-нибудь заметит в плане не только месячной, но и даже годовой выручки. А вот в Amazon заметят, причем быстро. А там еще акционеры. И будет совсем больно.

Именно поэтому в массовых продуктах, где **любой релиз — это огромные риски**, есть **приемка релизов**. Нельзя просто так взять и выкатить в продакшен. Ребята из Яндекса про это уже рассказывали наружу (есть на Youtube). Я не говорю ничего нового. Для приемки релизов придумали и создали **Иерархию Метрик.**

Зачем? **Иерархия Метрик позволяет**

1.   локализовать причины изменений на графиках важных метрик (“**расследовать аномалии**”)
2.   **не выкатывать изменения, которые могут навредить всей компании**(правило: метрики верхнего уровня не должны просесть, даже если целевая метрика релиза выросла).

**Иерархия Метрик — это больше, чем древовидная структура метрик.**В 2012 году я впервые услышала об **Иерархии Метрик**на втором потоке ШМЯ (Школы Менеджеров Яндекса) от большого ученого (математика) и руководителя качества Поиска на тот момент — Дениса Расковалова. Честно скажу, но даже мое физтеховское образование не помогло. **За 10–15 минут понять эту тему глубоко не удалось.**

Многие сейчас пропагандируют **Иерархию Метрик.**Но это просто **древовидные структуры**. “Вот смотрите LTV, он зависит от Retention, определим между ними связь”. Я смею утверждать, что это немного не то. Таким образом выстроенная Иерархия Метрик **— не более, чем мыслеобраз.** Хотя для Интернет-магазина игрушек — уже не плохо.

> Древовидные структуры метрик — не более, чем мыслеобраз. Чтобы это стало Иерархией метрик, надо применить научный подход и анализ данных.

Если вы уже как Amazon или движетесь в его сторону, придется применить **научный подход к построению Иерархии Метрик.**Сразу признаюсь, никогда не делала **Иерархию Метрик**как у Дениса**.**Но её построение означает, что вы не просто обозначите связи между дублирующими друг друга по смыслу и не выдерживающими критики метриками, а как минимум

1) **докажете эти связи по данным**,

2)**изучите чувствительность метрик,**

3) **сделаете ревью метрик** (глазами людей, которые умеют писать и проверять формулы).

## Пирамида Метрик

**Кто придумал?**Я придумала **Пирамиду Метрик** в 2017 году и была довольна собой. Пока не погуглила. Оказалось, **к парадигме “Пирамида метрик” приходят многие (читай все) аналитики.**Ровно так же, как примерно к двум годам ребенок начинает собирать пирамидку из 3–5 колец.

Press enter or click to view image in full size

![Image 4](https://miro.medium.com/v2/resize:fit:700/1*9V3cvWZjfoamoBvIixzbYw.png)

Разнообразные “пирамиды метрик” глазами Google

Что такое **Пирамида Метрик?**

**Пирамида Метрик — это Иерархия и Классификация метрик.**

Если продукт — не Amazon, то **иерархия**значит _хотя бы обозначить_ связи между метриками или создать некую древовидную структуру. Так как это **редко дает значимые эффекты для порядка в аналитике или управлении изменениями** на основе данных, то **мы добавляем классификацию.**

## Get Elena Seregina’s stories in your inbox

Join Medium for free to get updates from this writer.

Remember me for faster sign in

**Зачем нужна классификация?**

Во-первых, классификация помогает **убрать гиперфокусировку команды на одном из множества процессов**. Во время аудита метрик и дэшбордов мы можем выяснить, что команда думает только об изменении микроэкономических показателей или только об интерфейсе.

Press enter or click to view image in full size

![Image 5](https://miro.medium.com/v2/resize:fit:700/1*HHhhoo0pMws53b0G5eDOEw.png)

мой воркшоп по аналитике на ProductSense 2019

Во-вторых, классификация помогает **создать базовую иерархию**, так как слои **Пирамиды Метрик** выставлены в иерархическом порядке.

Press enter or click to view image in full size

![Image 6](https://miro.medium.com/v2/resize:fit:700/1*7JF0nlLFZCvUDOlo-qskMQ.png)

переписка в чате аналитиков Лёши Никушина

В-третьих, классификация здорово помогает **очертить зоны ответственности** за рост показателей, **грамотно выбрать KPI и собрать дэшборды каждой команде в компании**, не заставляя их растить некую бессмысленную для всех подряд Метрику Всевластия.

Есть и другие бенефиты, но пока остановимся на трех.

Press enter or click to view image in full size

![Image 7](https://miro.medium.com/v2/resize:fit:700/1*pIcxKRFnx3sdsS-Km0CynA.png)

> **Количество метрик на дэшборде зависит от необходимой скорости реагирования на их изменения, команды заказчиков и стадии развития бизнеса.**

Press enter or click to view image in full size

![Image 8](https://miro.medium.com/v2/resize:fit:700/1*K9pOtxgN5k2xzHOahd_jwQ.png)

## North Start Metrics (метрики Всевластия)

**North Start Metric (NSM)** — это метрика Всевластия, или такая крутая метрика, глядя на которую Вы неминуемо придете к успеху. Есть хорошая статья про NSM на VC — [https://vc.ru/flood/26005-north-star-metric](https://vc.ru/flood/26005-north-star-metric)

На самом деле, несмотря на то, что NSM — отчасти утопия, **для конкретной фичи или задачи можно найти не просто хорошую, а очень хорошую метрику** (NSM, метрику Всевластия). У меня были такие кейсы в практике.

Но что важно знать про **NSM. Метрика Всевластия — это гипотеза**, начиная от того, что её можно найти и формализовать, и заканчивая тем, что это Вам поможет. Если все круто, и Вам однажды хорошо помогла одна метрика, NSM, главное не превратить работу всей компании **BDSM по росту NSM**. Что лично я и наблюдала, активно занимаясь консультациями по аналитике в некоторых ИТ-компаниях .

> Если … Вам однажды круто помогла одна метрика, **NSM**,**главное не превратить работу всей компании в BDSM по росту NSM**.

## Как North Start Metric связана с пирамидой метрик и иерархией метрик?

Как Вы наверное уже догадались, прежде всего и практические только словом “метрика”. NSM можно найти с помощью любой системы метрик. Хотя скажу по секрету, это не самый простой и успешный путь.

Делать Иерархию или Пирамиду метрик вокруг NSM можно, но надо понимать, что это уже другие Иерархии или Пирамиды. Пирамида метрик помогает не допустить возникновения гиперфокуса, который несет опасность для развития компании. Пирамида метрик вокруг NSM работает наоборот.

> **Пирамида метрик помогает не допустить возникновения гиперфокуса, который несет опасность для развития компании. Пирамида метрик вокруг NSM работает наоборот.**

**Большое спасибо за внимание. Я в соцсетях**:

**Фейсбук:**[https://www.facebook.com/elenesta](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbXhweF92OHpndUQ0YnBEUFpDLUo5ZUkxTjMxQXxBQ3Jtc0tsSDBlRm5JdDJwRjdtekJBTG9mWWRCTmpXU0llaGRsQ0d1d1UtNVBpc1JkQnJJZlprUTBJdm1nMzRwckJwaWRlbkVhNDhuc1gtSGFmWUttTG91YzVEQ09zSDZCRXhvRVE1Z1pfaVRDOGVEOGZ5RTQ1MA&q=https%3A%2F%2Fwww.facebook.com%2Felenesta)

**Telegram:**[https://t.me/close2sense](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbGY1ZUFkN1RGaXdWd1AzUURVMEhrcllfalhPQXxBQ3Jtc0trWWt6Z2FxamNfQnZ0a3NYS3V5U0dQUGUtZ0dnUXhiRmdkTGtpTHVtOS1CNG4yRlBEU1VQZ1VMRWZWY2FOS2dZNzNGa3NZV0dod0Y3ZXNlcU9CYXlJM0hIZnNPbWZmYjZQakFOYmVjOXp0WGxuTW9LYw&q=https%3A%2F%2Ft.me%2Fclose2sense)

**Instagram:**[https://www.instagram.com/elenest007/](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbWVzb2kxNEwxVDBVMnJocVRpOGNienZIbjZsUXxBQ3Jtc0trZUd6Zmo0YjIzTlNNZzNYakR0cDFBMWZFTEc5dVdUVzkxaE9vZ1hvU2RpUmNseEVsRU1neElSZFo2bWZzODR2bUxrLWlxc2FuSXM0akxna2VyZEI1czROT24xOTc1bFNubU9tdlNUM0hYd0IwRGhoSQ&q=https%3A%2F%2Fwww.instagram.com%2Felenest007%2F)

**Youtube:**[https://www.youtube.com/channel/UCTiC4Ldq7umTQuJ9237tqyQ](https://www.youtube.com/channel/UCTiC4Ldq7umTQuJ9237tqyQ)

**Сайт:**[http://datalatte.ru/](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa19lMldodU5XWmFXMjlpNUVnYWRnLUxuYndoZ3xBQ3Jtc0tsQjBsdll3aWVRWTVQeUZDNnNMZ1pTQUdNNE8yamJHS0NVN28tU2dqNzdfSXh0VFprUlNvTlFGcWEwOU5iVHhSM1ZybnNBRzYzZkdCeTBTb0NYcG93bDJfOWhjR0dxemR2RkFsR3A4SFQ2V3V5YjNyTQ&q=http%3A%2F%2Fdatalatte.ru%2F)

**Узнай всё про Пирамиду метрик и Стратегическую аналитику:**[https://datalatte.ru/#education](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbnFLaGcxalpMUW5mdkkyRzVCMEZmYWl3NlpHd3xBQ3Jtc0tuVlJ1YmtrZ3pOa280MWVta01GT005SnNJZHZ2bW5GWnlrR1d6ZVpTMTYzZ1R4ZWpMaGhsYkJJbDd0M1I4SUZ3WnU1Qm0yemxnTHJReEJaeFBoVXVrYzFVT0tBOFRSY2xEZHl4aThsRG0wZVEyVmV4MA&q=https%3A%2F%2Fdatalatte.ru%2F%23education)

—

Продолжение в статье [https://medium.com/@elenest/metrics-frameworks-d7c800f91246](https://medium.com/@elenest/metrics-frameworks-d7c800f91246)
