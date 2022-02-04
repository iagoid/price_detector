Este é um projeto de web scraping realizado utilizando Django, ele realiza de uma maneira muito simples a raspagem de dados dos sites disponíveis e as retorna para a tela.

Nele existe um sistema de processo em segundo plano que chama a função de WebScraping a cerca de cada 5 minutos, e a função de WebScraping que indexa itens cujas informações são mais antigas que 15 minutos. Ou seja o preço mostrado vai atrasado em seu preço mostrado no site em no máximo 20 minutos.

Python 3.10.2               
beautifulsoup4-4.10.0            ---     pip install beautifulsoup4
Django 4.1.dev20220121161031     ---     pip install django
html5lib==1.1                    ---     pip install html5lib