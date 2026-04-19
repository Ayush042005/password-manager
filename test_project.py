import cryptography
import pytest
from project import generate_password, check_password_strength, validate_service_name

def test_generate_password():
    # tests default parameters
    pwd = generate_password()
    assert len(pwd) == 16
    assert any(c.isupper() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd)

    # tests custom length
    pwd = generate_password(length=20)
    assert len(pwd) == 20
    
    # test without symbols
    pwd = generate_password(use_symbols=False)
    assert not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd)
    
    # Test without numbers
    pwd = generate_password(use_numbers=False)
    assert not any(c.isdigit() for c in pwd)
    
    # testing minimum length validation
    with pytest.raises(ValueError):
        generate_password(length=3)

def test_check_password_strength():
    # very weak password
    result = check_password_strength("abc")
    assert result["score"] < 30
    assert result["rating"] == "Weak"
    
    # weak password
    result = check_password_strength("password")
    assert result["rating"] in ["Weak", "Medium"]
    
    # medium password
    result = check_password_strength("Pass1234")
    assert result["score"] >= 40
    
    # strong password
    result = check_password_strength("MyP@ssw0rd123")
    assert result["score"] >= 60
    assert result["rating"] in ["Strong", "Very Strong"]
    
    # very strong password
    result = check_password_strength("MyV3ry$tr0ng&P@ssw0rd!")
    assert result["score"] >= 80
    assert result["rating"] == "Very Strong"
    
    # empty password
    result = check_password_strength("")
    assert result["score"] == 0
    assert result["rating"] == "Invalid"

def test_validate_service_name():
    # valid names
    assert validate_service_name("Google") == True
    assert validate_service_name("My Bank Account") == True
    assert validate_service_name("gmail-2023") == True
    assert validate_service_name("test_service") == True
    
    # invalid names
    assert validate_service_name("") == False
    assert validate_service_name("   ") == False
    assert validate_service_name("service@email") == False
    assert validate_service_name("a" * 51) == False  # Too long
    assert validate_service_name("service!name") == False  # Special char
