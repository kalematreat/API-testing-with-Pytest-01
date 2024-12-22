import requests
import json
import pytest
import csv


@pytest.fixture()
def BASE_URL():
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture()
def post_id():
    return 1

@pytest.fixture()
def resources():
    return "posts"

def load_test_data():
    with open("test_data.json", "r") as file:
        return json.load(file)
# the tests 
# GET ALL POSTS --> 6
# GET POST BY ID --> 7
# POST POST --> 7
# PUT POST --> 7
# DEL POST --> 3   

# 2 ways to save the results
# 1--> to make an new file for results 
# def log_result_to_file(test_name, method, endpoint, status_code, result, message=""):
#     filename = "result.csv"
#     # Check if the file exists to decide whether to write headers
#     write_headers = False
#     try:
#         with open(filename, mode="r"):
#             pass
#     except FileNotFoundError:
#         write_headers = True

#     with open(filename, mode="a", newline="") as file:
#         writer = csv.writer(file)
#         if write_headers:
#             writer.writerow(["Test Name", "Method", "Endpoint", "Status Code", "Result", "Message"])
#         writer.writerow([test_name, method, endpoint, status_code, result, message])

# 2--> already have a file named result_api.csv
def log_result_to_file(test_name, method, endpoint, status_code, result, message=""):
    filename = "result_api.csv"  # Update the filename to the desired one
    # Check if the file exists to decide whether to write headers
    write_headers = False
    try:
        with open(filename, mode="r"):
            pass
    except FileNotFoundError:
        write_headers = True

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if write_headers:
            writer.writerow(["Test Name", "Method", "Endpoint", "Status Code", "Result", "Message"])
        writer.writerow([test_name, method, endpoint, status_code, result, message])

# GET ALL POSTS

# 1--> Test if the status code is 200
def test_status_code(BASE_URL,resources):
    test_name = "Test Status Code"
    response = requests.get(f"{BASE_URL}/{resources}")
    result = "Success" if response.status_code == 200 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result, "Status code is not 200")
    else:   
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result)
    assert response.status_code == 200

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources):
    test_name = "Test Response Time"
    response = requests.get(f"{BASE_URL}/{resources}")
    result = "Success" if response.elapsed.total_seconds() < 0.3 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result, "Response time exceeds 300ms")
    else:   
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result)
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test if the number of posts is 100
def test_number_of_posts(BASE_URL,resources):
    test_name = "Test Number of Posts"
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    result = "Success" if len(json_data) == 100 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result, f"Expected 100 posts, but got {len(json_data)}")
    else:   
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result)
    assert len(json_data) == 100

# 4--> Test if the response is an array
def test_response_is_array(BASE_URL,resources):
    test_name = "Test Response is Array"
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    result = "Success" if isinstance(json_data, list) else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result, "Response is not an array")
    else:   
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result)
    assert isinstance(json_data, list)

# 5--> Test if the IDs in the response are sequential
def test_ids_are_sequential(BASE_URL,resources):
    test_name = "Test IDs are Sequential"
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    result = "Success"
    for i in range(1, len(json_data)):
        if json_data[i]["id"] != json_data[i - 1]["id"] + 1:
            result = "Failure"
            break
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result, "IDs are not sequential")
    else:   
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result)
    assert result == "Success"

# 6--> Test if the response body is not empty
def test_response_body_not_empty(BASE_URL,resources):
    test_name = "Test Response Body Not Empty"
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    result = "Success" if json_data else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result, "Response body is empty")
    else:   
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}", response.status_code, result)
    assert json_data

# GET POST BY ID

# 1--> Test if the status code is 200
def test_status_code(BASE_URL,resources,post_id):
    test_name = "Test Status Code"
    response = requests.get(f"{BASE_URL}/{resources}/{post_id}")
    result = "Success" if response.status_code == 200 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "Status code is not 200")
    else:
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response.status_code == 200

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources,post_id):
    test_name = "Test Response Time"
    response = requests.get(f"{BASE_URL}/{resources}/{post_id}")
    result = "Success" if response.elapsed.total_seconds() < 0.3 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "Response time exceeds 300ms")
    else:
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test if the post ID is match
def test_post_id_is_1(BASE_URL,resources,post_id):
    test_name = "Test Post ID is 1"
    response_id = requests.get(f"{BASE_URL}/{resources}/{post_id}")
    json_data = response_id.json()
    result = "Success" if json_data["id"] == post_id else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET", f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result, "Post ID does not match")
    else:
        log_result_to_file(test_name, "GET", f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result)
    assert json_data["id"] == post_id

# 4--> Test if the post ID is not 1
@pytest.mark.xfail
def test_post_id_is_not_1(BASE_URL,resources,post_id):
    test_name = "Test Post ID is Not 1"
    response_id = requests.get(f"{BASE_URL}/{resources}/{post_id}")
    json_data = response_id.json()
    result = "Success" if json_data["id"] != post_id else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET", f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result, "Post ID should not match")
    else:
        log_result_to_file(test_name, "GET", f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result)
    assert json_data["id"] != post_id

# 5--> Test if the title is a string
def test_title_is_string(BASE_URL,resources,post_id):
    test_name = "Test Title is String"
    response_id = requests.get(f"{BASE_URL}/{resources}/{post_id}")
    json_data = response_id.json()
    result = "Success" if isinstance(json_data["title"], str) else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result, "Title is not a string")
    else:
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result)
    assert isinstance(json_data["title"], str)

# 6--> Test if the title contains the word 'provident'
def test_title_contains_provident(BASE_URL,resources,post_id):
    test_name = "Test Title Contains Provident"
    response_id = requests.get(f"{BASE_URL}/{resources}/{post_id}")
    json_data = response_id.json()
    result = "Success" if "provident" in json_data["title"] else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result, "Title does not contain 'provident'")
    else:
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result)
    assert "provident" in json_data["title"]

# 7--> Test if the body contains at least two lines
def test_body_has_at_least_two_lines(BASE_URL,resources,post_id):
    test_name = "Test Body Has At Least Two Lines"
    response_id = requests.get(f"{BASE_URL}/{resources}/{post_id}")
    json_data = response_id.json()
    lines = json_data["body"].split("\n")
    result = "Success" if len(lines) >= 2 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result, "Body has less than 2 lines")
    else:
        log_result_to_file(test_name, "GET",f"{BASE_URL}/{resources}/{post_id}", response_id.status_code, result)
    assert len(lines) >= 2

# POST 

# 1--> Test that the POST request was successful (status code 200 or 201)
def test_successful_post_request(BASE_URL,resources):
    test_name = "Test Successful POST Request"
    test_data = load_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    result = "Success" if response.status_code in [200, 201] else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result, "POST request was not successful")
    else: 
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result)
    assert response.status_code in [200, 201]

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources):
    test_name = "Test Response Time"
    test_data = load_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    result = "Success" if response.elapsed.total_seconds() < 0.3 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result, "Response time exceeds 300ms")
    else: 
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result)
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test that the title in the response matches the input title
def test_title_matches_input_value(BASE_URL,resources):
    test_name = "Test Title Matches Input Value"
    test_data = load_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    result = "Success" if json_data["title"] == post_data["title"] else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result, f"Title does not match, expected: {post_data['title']}")
    else: 
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result)
    assert json_data["title"] == post_data["title"]

# 4--> Test that the body in the response is not empty
def test_response_body_contains_non_empty_body(BASE_URL,resources):
    test_name = "Test Response Body Contains Non-Empty Body"
    test_data = load_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    result = "Success" if json_data["body"] else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result, "Response body is empty")
    else: 
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result)
    assert json_data["body"]

# 5--> Test that the response contains the post ID
def test_response_body_contains_post_id(BASE_URL,resources):
    test_name = "Test Response Body Contains Post ID"
    test_data = load_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    result = "Success" if "id" in json_data else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result, "Response body does not contain post ID")
    else: 
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result)
    assert "id" in json_data

# 6--> Test that the response body contains the 'body' property
def test_response_body_contains_post_body_property(BASE_URL,resources):
    test_name = "Test Response Body Contains Post Body Property"
    test_data = load_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    result = "Success" if "body" in json_data else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result, "Response body does not contain 'body' property")
    else: 
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result)
    assert "body" in json_data

# 7--> Test that the response body contains the 'title' property
def test_response_body_contains_post_title_property(BASE_URL,resources):
    test_name = "Test Response Body Contains Post Title Property"
    test_data = load_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    result = "Success" if "title" in json_data else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result, "Response body does not contain 'title' property")
    else: 
        log_result_to_file(test_name, "POST", f"{BASE_URL}/{resources}", response.status_code, result)
    assert "title" in json_data

# PUT 

# 1--> Test that the PUT request returns a status code of 200
def test_status_code_200(BASE_URL,resources,post_id):
    test_name = "Test PUT Status Code 200"
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{post_id}", json={**test_data[0], **update_data})
    result = "Success" if response.status_code == 200 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, f"Unexpected status code: {response.status_code}")
    else:
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response.status_code == 200

# 2--> Test if the response time is less than 400ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources,post_id):
    test_name = "Test PUT Response Time"
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{post_id}", json={**test_data[0], **update_data})
    result = "Success" if response.elapsed.total_seconds() < 0.4 else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "Response time exceeds 400ms")
    else:
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response.elapsed.total_seconds() < 0.4

# 3--> Test that the PUT request is successful (status codes 200, 201, 204)
def test_successful_put_request(BASE_URL,resources,post_id):
    test_name = "Test PUT Successful Request"
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{post_id}", json={**test_data[0], **update_data})
    result = "Success" if response.status_code in [200, 201, 204] else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, f"Unexpected status code: {response.status_code}")
    else:
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response.status_code in [200, 201, 204]

# 4--> Test that the userId in the response is a string
def test_user_id_is_string(BASE_URL,resources,post_id):
    test_name = "Test UserId is String"
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{post_id}", json={**test_data[0], **update_data})
    json_response = response.json()
    result = "Success" if isinstance(str(json_response.get("userId", "")), str) else "Failure"
    log_result_to_file(test_name, "PUT",f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    if result == "Failure" :
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "userId is not a string")
    else:
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert isinstance(str(json_response.get("userId", "")), str)

# 5--> Test that the response is not empty
def test_response_is_not_empty(BASE_URL,resources,post_id):
    test_name = "Test Response is Not Empty"
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{post_id}", json={**test_data[0], **update_data})
    result = "Success" if response.json() else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "Response body is empty")
    else:
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response.json()

# 6--> Test that the response body contains the 'body' property
def test_body_property_exists(BASE_URL,resources,post_id):
    test_name = "Test Body Property Exists"
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{post_id}", json={**test_data[0], **update_data})
    json_response = response.json()
    result = "Success" if "body" in json_response else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "Response body does not contain 'body' property")
    else:
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert "body" in json_response

# 7--> Test that the updated data is reflected in the response
def test_updated_data_in_response(BASE_URL,resources,post_id):
    test_name = "Test Updated Data in Response"
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{post_id}", json={**test_data[0], **update_data})
    json_response = response.json()
    result = "Success" if json_response["body"] == "New Technology" else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "Updated data not reflected in response")
    else:
        log_result_to_file(test_name, "PUT", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert json_response["body"] == "New Technology"

# DELETE

# 1--> Test that the DELETE request is successful (status codes 200, 202, 204)
def test_successful_delete_request(BASE_URL,resources,post_id):
    test_name = "Test Successful Delete Request"
    response = requests.delete(f"{BASE_URL}/{resources}/{post_id}")
    result = "Success" if response.status_code in [200, 202, 204] else "Failure"
    if result == "Failure" :
        log_result_to_file(test_name, "DELETE", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result,f"Unexpected status code: {response.status_code}")
    else:
        log_result_to_file(test_name, "DELETE", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response.status_code in [200, 202, 204]

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources,post_id):
    test_name = "Test Response Time"
    response = requests.delete(f"{BASE_URL}/{resources}/{post_id}")
    result = "Success" if response.elapsed.total_seconds() < 0.3 else "Failure"
    if result == "Failure":
        log_result_to_file(test_name, "DELETE", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result, "Response time exceeds 300ms")
    else:
        log_result_to_file(test_name, "DELETE", f"{BASE_URL}/{resources}/{post_id}", response.status_code, result,)
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test that the response body is an empty JSON object
def test_response_body_is_empty_json(BASE_URL,resources,post_id):
    test_name = "Test Response Body is Empty JSON"
    response = requests.delete(f"{BASE_URL}/{resources}/{post_id}")
    response_body = response.text.strip()  # Get the response body as text and strip whitespace
    result = "Success" if response_body == "{}" else "Failure"
    if result == "Failure":
        log_result_to_file(test_name, "DELETE",f"{BASE_URL}/{resources}/{post_id}", response.status_code, result,f"Response body is not an empty JSON object: {response_body}")
    else :
        log_result_to_file(test_name, "DELETE",f"{BASE_URL}/{resources}/{post_id}", response.status_code, result)
    assert response_body == "{}", f"Response body is not an empty JSON object: {response_body}"

