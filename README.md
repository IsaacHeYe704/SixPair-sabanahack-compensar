# Vivian
## ¿Quiên es Vivian?
Vivian es un nuevo miembro de la familia Compensar, la nueva agente virtual será capaz de aprender de ti para recomendar y agendar los mejores servicios de Compensar de acuerdo a tus necesidades.

Con una simple pregunta escrita o por voz, Vivian será capaz de decirte a que sede de Compensar ir, a cuantos de tus amigos puedes invitar, cual sera el precio de acuerdo a tu categoria, y cual es el mejor horario para ti.

## Funcionamiento
Para este primer prototipo simplificado, utilizamos modelos de lenguaje de terceros para extraer caracteristicas relevantes en el texto que le envías a Vivian.
Posteriormente tomamos la lista de servicios de compensar con la sede donde ofrecen sus servicios, el costo, la capacidad de personas que pueden acceder al servicio, la ubicación del usuario, la categoria y la cantidad de recomendaciones que vamos a realizar.
Nuestro modelo realiza una representación vectorial de tus necesidades y las compara con las caracteristicas de los servicios que ofrece Compensar, filtramos de acuerdo a la sede más cercana y al tipo de servicio que quieras acceder, por ejemplo, deporte o recreación.
Finalmente utilizamos nuevamente un modelo de lenguaje natural para llevar las recomendaciones a un lenguaje propio de Vivian, un miembro más de la familia.

## Alcance
Con Vivian buscamos que sea una herramienta de gran utilidad para facilitar la comunicación entre el usuario y la empresa. En el futuro se busca que Vivian sea capaz de agendar reservas de servicios, monitoriar nuestra salud con ayuda de relojes inteligentes de terceros, resolver preguntas respecto a tramites o servicios de la caja de compensación, realizar tures virtuales, y más. Con esto buscamos que Vivian siempre este con el usuario y para el usuario, como un miembro más de cada familia.
