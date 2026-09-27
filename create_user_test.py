import sender_stand_request
import data

# esta función cambia los valores en el parámetro "firstName"
def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

# Función de prueba positiva
def positive_assert(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 201
    assert response.json()["authToken"] != ""

    user_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + response.json()[
        "authToken"]

    assert user_table_response.text.count(str_user) == 1

def negative_assert(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, " \
                                         "la longitud debe ser de 2 a 15 caracteres."

# Función de prueba negativa
# La respuesta contiene el siguiente mensaje de error: "No se han enviado todos los parámetros requeridos"
def negative_assert_no_firstname(user_body):
    # Guarda el resultado de llamar a la función a la variable "response"
    response = sender_stand_request.post_new_user(user_body)
    # Comprueba si la respuesta contiene el código 400
    assert response.status_code == 400
    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400
    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

#1
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")
#2
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")
#3
def test_create_user_1_letter_in_first_name_get_failed_response():
    negative_assert ("A")
#4
def test_create_user_16_letter_in_first_name_get_failed_response():
    negative_assert("Aaaaaaaaaaaaaaaa")
#5
def test_create_user_with_blank_spaces_in_first_name_get_failed_response():
    negative_assert("A a")
#6
def test_create_user_with_special_characters_in_first_name_get_failed_response():
    negative_assert("A&")
#7
def test_create_user_with_numbers_in_first_name_get_failed_response():
    negative_assert("A2")
#8
def test_create_user_no_first_name_get_error_response():
    negative_assert_no_firstname(data.user_body_no_first_name)

#9
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)
#10
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400

def test_get_health_returns_200_and_status_ok():
    response = sender_stand_request.get_health()
    assert response.status_code == 200
    assert response.json()["status"] == "ok"