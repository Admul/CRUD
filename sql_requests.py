## INSERT ##
def sql_insert(car_object):
    return f"INSERT INTO cars (name, country, auto_kpp) VALUES ('{car_object['name']}', '{car_object['country']}', '{car_object['auto_kpp']}')"

## RETRIEVE ##
def sql_get():
    return "SELECT * FROM cars"

def sql_retrieve(car_id):
    return f"SELECT * FROM cars WHERE id={car_id}"

## UPDATE ##
def sql_update(car_id, car_object):
    key = list(car_object.keys())[0]
    value = car_object[key]
    return f"UPDATE cars SET {key}='{value}' WHERE id={car_id}"

## DELETE ##
def sql_delete(car_id):
    return f"DELETE FROM cars WHERE id={car_id}"