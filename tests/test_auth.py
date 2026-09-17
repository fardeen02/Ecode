		
def test_register_user(client):
	response = client.post(
	    "/api/auth/register",
		json = {
		   "username": "Test_User",
		   "email": "test@example.com",
		   "password": "SecurePassword@4321",
		   "preferred_language": "java"
		}
	)
	
	assert response.status_code == 201
	
	data = response.get_json()
	
	assert data["message"] == f"User: Test_User is registered successfully"
	assert data["user"]["email"] == "test@example.com"
	
def test_missing_request_body(client):
	response = client.post(
		"/api/auth/register",
	)
		
	assert response.status_code == 415
	
def test_missing_username(client):
	response = client.post(
	    "/api/auth/register",
        json = {
		"email": "test@example.com",
		"password": "SecurePassword@4321",
		"preferred_language": "java"
		}		
	)
	
	assert response.status_code == 400
	
def test_missing_email(client):
	response = client.post(
	    "/api/auth/register",
		json = {
		   "username": "Test_User",
		   "password": "SecurePassword@4321",
		   "preferred_language": "java"
		}
	)
	
	assert response.status_code == 400

def test_missing_password(client):
	response = client.post(
	    "/api/auth/register",
		json = {
		   "username": "Test_User",
		   "email": "test@example.com",
		   "preferred_language": "java"
		}
	)
	
	assert response.status_code == 400

def test_missing_preferred_language(client):
	response = client.post(
	    "/api/auth/register",
		json = {
		   "username": "Test_User",
		   "email": "test@example.com",
		   "password": "SecurePassword@4321"
		}
	)
	
	assert response.status_code == 400

def test_register_duplicate_email(client):
    user = {
	    "username": "Test_User",
        "email": "duplicate@example.com",
		"password": "SecurePassword@4321",
		"preferred_language": "java"
    }

    first_response = client.post(
        "/api/auth/register",
        json=user
    )

    second_response = client.post(
        "/api/auth/register",
        json=user
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_register_duplicate_username(client):
    user = {
        "username": "Test_User",
        "email": "duplicate@example.com",
		"password": "SecurePassword@4321",
		"preferred_language": "java"
    }

    first_response = client.post(
        "/api/auth/register",
        json=user
    )

    second_response = client.post(
        "/api/auth/register",
        json=user
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_login_success(client):
	client.post(
	    "/api/auth/register",
		json={
		   "username": "Test_User",
		   "email": "test@example.com",
		   "password": "SecurePassword@4321",
		   "preferred_language": "python"
		}
	)
	
	response = client.post(
	    "/api/auth/login",
		json={
		   "username": "Test_User",
		   "password": "SecurePassword@4321"
		}
	)
	
	assert response.status_code == 200
	
	data = response.get_json()
	
	assert data["message"] == "Login successful"
	assert "access_token" in data
	assert data["user"]["username"] == "Test_User"

def test_login_username_missing(client):
	client.post(
	    "/api/auth/register",
		json={
		   "username": "Test_User",
		   "email": "test@example.com",
		   "password": "SecurePassword@4321",
		   "preferred_language": "python"
		}
	)
	
	response = client.post(
	    "/api/auth/login",
		json={
		   "password": "SecurePassword@4321"
		}
	)
	
	assert response.status_code == 400
	

def test_login_password_missing(client):
	client.post(
	    "/api/auth/register",
		json={
		   "username": "Test_User",
		   "email": "test@example.com",
		   "password": "SecurePassword@4321",
		   "preferred_language": "python"
		}
	)
	
	response = client.post(
	    "/api/auth/login",
		json={
		   "username": "Test_User"
		}
	)
	
	assert response.status_code == 400



	